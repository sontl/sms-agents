from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig
from playwright.async_api import BrowserContext
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
import asyncio
import logging
import os
import random

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
x_com_cookies = "/Users/sontl/Downloads/x.com.cookies.json"
facebook_cookies = "/Users/sontl/Downloads/www.facebook.com.cookies.json"
def get_random_task():
    """Return a random task configuration with initial actions."""
    tasks = [
        {
            "task": ("Navigate to Facebook, go to your profile page, and create a new post. Write an inspiring quote about "
                    "life and music, something that reflects on how melody brings joy to our existence. Make sure to add "
                    "relevant hashtags like #music #suno #singmesong. After writing, click the Post button."),
            "initial_actions": [
                {'open_tab': {'url': 'https://facebook.com'}}
            ],
            "cookies_file": facebook_cookies
        },
        {
            "task": ("Go to X/Twitter and create a new tweet. Share a thoughtful reflection about how songs can heal the soul "
                    "and bring people together. Include hashtags like #MusicHeals #SingMeSong. After composing your tweet, "
                    "post it."),
            "initial_actions": [
                {'open_tab': {'url': 'https://x.com'}}
            ],
            "cookies_file": x_com_cookies
        },
        {
            "task": ("Visit Facebook and create a new post about the transformative power of music. Share how melodies can "
                    "change our mood and uplift our spirits. Include a famous quote about music from a renowned musician or "
                    "composer. Add hashtags like #MusicIsLife #Melodies #SingMeSong."),
            "initial_actions": [
                {'open_tab': {'url': 'https://facebook.com'}}
            ],
            "cookies_file": facebook_cookies
        },
        {
            "task": ("Navigate to X/Twitter and compose a tweet about the connection between nature's rhythms and music. "
                    "Reflect on how the sounds of nature inspire musical creativity. Use hashtags like #NatureMusic "
                    "#MusicalInspiration #SingMeSong."),
            "initial_actions": [
                {'open_tab': {'url': 'https://x.com'}}
            ],
            "cookies_file": x_com_cookies
        },
        {
            "task": ("Navigate to Facebook and create a new post about the transformative power of music. Share how melodies can "
                    "change our mood and uplift our spirits. Include a famous quote about music from a renowned musician or "
                    "composer. Add hashtags like #MusicIsLife #Melodies #SingMeSong."),
            "initial_actions": [
                {'open_tab': {'url': 'https://facebook.com'}}
            ],
            "cookies_file": facebook_cookies
        }, 
        {
            "task": ("Navigate to X/Twitter and compose a tweet about the connection between nature's rhythms and music. "
                    "Reflect on how the sounds of nature inspire musical creativity. Use hashtags like #NatureMusic "
                    "#MusicalInspiration #SingMeSong."),
            "initial_actions": [
                {'open_tab': {'url': 'https://x.com'}}
            ],
            "cookies_file": x_com_cookies
        },
        {
            "task": ("Navigate to Facebook and like a post  ."),
            "initial_actions": [
                {'open_tab': {'url': 'https://facebook.com'}}
            ],
            "cookies_file": facebook_cookies
        },
        {
            "task": ("Navigate to X/Twitter and like a post."),
            "initial_actions": [
                {'open_tab': {'url': 'https://x.com'}}
            ],
            "cookies_file": x_com_cookies
        },
        {
            "task": ("Navigate to Facebook and comment on a post. Comment something positive and inspiring and something that is related to the post. Short and human like."),
            "initial_actions": [
                {'open_tab': {'url': 'https://facebook.com'}}
            ],
            "cookies_file": facebook_cookies
        },
        {
            "task": ("Navigate to X/Twitter and comment on a post. Comment something positive and inspiring and something that is related to the post. Short and human like."),
            "initial_actions": [
                {'open_tab': {'url': 'https://x.com'}}
            ],
            "cookies_file": x_com_cookies
        }
    ]
    return random.choice(tasks)

async def cleanup_browser(agent):
    """Safely cleanup browser resources."""
    try:
        if agent and hasattr(agent, 'browser') and agent.browser:
            if hasattr(agent.browser, 'context') and agent.browser.context:
                await agent.browser.context.close()
            if hasattr(agent.browser, 'playwright') and agent.browser.playwright:
                await agent.browser.playwright.stop()
    except Exception as e:
        logger.error(f"Error during browser cleanup: {e}")

async def run_agent():
    """Run the browser-use agent with a randomly selected task."""
    agent = None

    try:
        # Get a random task configuration
        task_config = get_random_task()
        
        # Create a timeout for the entire operation
        timeout = 8 * 60  # 8 minutes timeout
        
        # Basic configuration
        context_config = BrowserContextConfig(
            cookies_file=task_config["cookies_file"],
            wait_for_network_idle_page_load_time=3.0,
            browser_window_size={'width': 1280, 'height': 1100},
            locale='en-US',
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            highlight_elements=True,
            viewport_expansion=500,
            #chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        )

        # Initialize browser with context config
        config = BrowserConfig(
                    headless=False,
                    disable_security=True,
                    # Comment the next 3 lines to make it work
                    new_context_config=context_config
                )

        browser = Browser(config=config)
        
        # Initialize the agent with the random task
        agent = Agent(
            task=task_config["task"],
            llm=ChatGoogleGenerativeAI(
                model="gemini-2.0-pro-exp-02-05",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.7,
                convert_system_message_to_human=True
            ),
            browser=browser,
            use_vision=True,
            save_conversation_path="logs/conversation",
            initial_actions=task_config["initial_actions"]
        )
        
        # Run the agent with timeout
        try:
            result = await asyncio.wait_for(agent.run(), timeout=timeout)
            logger.info(f"Agent execution completed with task: {task_config['task'][:100]}...")
            logger.info(f"Result: {result}")
        except asyncio.TimeoutError:
            logger.error(f"Task timed out after {timeout} seconds")
        finally:
            # Always cleanup browser resources
            await cleanup_browser(agent)
        
    except Exception as e:
        logger.error(f"Error running agent: {e}", exc_info=True)
        # Ensure browser cleanup on error
        if agent:
            await cleanup_browser(agent)

def run_agent_wrapper():
    """Wrapper function to run the async agent in the scheduler."""
    try:
        # Create new event loop for each run
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the agent
        loop.run_until_complete(run_agent())
        
        # Clean up
        loop.close()
    except Exception as e:
        logger.error(f"Error in agent wrapper: {e}", exc_info=True)

def main():
    """Main function to set up and start the scheduler."""
    try:
        # Create scheduler
        scheduler = BlockingScheduler()
        
        # Add job to run every 15 minutes
        scheduler.add_job(
            run_agent_wrapper,
            CronTrigger(minute='*/5'),  # Run every 15 minutes
            name='browser_agent_job',
            max_instances=1,
            coalesce=True,
            misfire_grace_time=300  # 5 minutes grace time
        )
        
        logger.info("Scheduler started. Agent will run every 15 minutes.")
        scheduler.start()
        #run_agent_wrapper()
        
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
    except Exception as e:
        logger.error(f"Error in scheduler: {e}", exc_info=True)

if __name__ == "__main__":
    main() 