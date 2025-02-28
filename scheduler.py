from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
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

def get_random_task():
    """Return a random task configuration with initial actions."""
    tasks = [
        {
            "task": ("Navigate to Facebook, go to your profile page, and create a new post. Write an inspiring quote about "
                    "life and music, something that reflects on how melody brings joy to our existence. Make sure to add "
                    "relevant hashtags like #music #suno #singmesong. After writing, click the Post button."),
            "initial_actions": [
                {'open_tab': {'url': 'https://facebook.com'}}
            ]
        },
        {
            "task": ("Go to X/Twitter and create a new tweet. Share a thoughtful reflection about how songs can heal the soul "
                    "and bring people together. Include hashtags like #MusicHeals #SingMeSong. After composing your tweet, "
                    "post it."),
            "initial_actions": [
                {'open_tab': {'url': 'https://x.com'}}
            ]
        },
        {
            "task": ("Visit Facebook and create a new post about the transformative power of music. Share how melodies can "
                    "change our mood and uplift our spirits. Include a famous quote about music from a renowned musician or "
                    "composer. Add hashtags like #MusicIsLife #Melodies #SingMeSong."),
            "initial_actions": [
                {'open_tab': {'url': 'https://facebook.com'}}
            ]
        },
        {
            "task": ("Navigate to X/Twitter and compose a tweet about the connection between nature's rhythms and music. "
                    "Reflect on how the sounds of nature inspire musical creativity. Use hashtags like #NatureMusic "
                    "#MusicalInspiration #SingMeSong."),
            "initial_actions": [
                {'open_tab': {'url': 'https://x.com'}}
            ]
        },
        {
            "task": ("Navigate to Facebook and create a new post about the transformative power of music. Share how melodies can "
                    "change our mood and uplift our spirits. Include a famous quote about music from a renowned musician or "
                    "composer. Add hashtags like #MusicIsLife #Melodies #SingMeSong."),
            "initial_actions": [
                {'open_tab': {'url': 'https://facebook.com'}}
            ]
        }, 
        {
            "task": ("Navigate to X/Twitter and compose a tweet about the connection between nature's rhythms and music. "
                    "Reflect on how the sounds of nature inspire musical creativity. Use hashtags like #NatureMusic "
                    "#MusicalInspiration #SingMeSong."),
            "initial_actions": [
                {'open_tab': {'url': 'https://x.com'}}
            ]
        },
        {
            "task": ("Navigate to Facebook and like a post  ."),
            "initial_actions": [
                {'open_tab': {'url': 'https://facebook.com'}}
            ]
        },
        {
            "task": ("Navigate to X/Twitter and like a post."),
            "initial_actions": [
                {'open_tab': {'url': 'https://x.com'}}
            ]
        },
        {
            "task": ("Navigate to Facebook and comment on a post."),
            "initial_actions": [
                {'open_tab': {'url': 'https://facebook.com'}}
            ]
        },
        {
            "task": ("Navigate to X/Twitter and comment on a post."),
            "initial_actions": [
                {'open_tab': {'url': 'https://x.com'}}
            ]
        }
    ]
    return random.choice(tasks)

# Basic configuration
config = BrowserConfig(
    headless=True,
    disable_security=True,
    chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)

browser = Browser(config=config)

# Load environment variables
load_dotenv()

async def run_agent():
    """Run the browser-use agent with a randomly selected task."""
    try:
        # Get a random task configuration
        task_config = get_random_task()
        
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
        
        # Run the agent and get the result
        result = await agent.run()
        
        # Log the result
        logger.info(f"Agent execution completed with task: {task_config['task'][:100]}...")
        logger.info(f"Result: {result}")
        
    except Exception as e:
        logger.error(f"Error running agent: {e}", exc_info=True)

def run_agent_wrapper():
    """Wrapper function to run the async agent in the scheduler."""
    asyncio.run(run_agent())

def main():
    """Main function to set up and start the scheduler."""
    try:
        # Create scheduler
        scheduler = BlockingScheduler()
        
        # Add job to run every 10 minutes
        scheduler.add_job(
            run_agent_wrapper,
            CronTrigger(minute='*/10'),  # Run every 10 minutes
            name='browser_agent_job',
            max_instances=1,
            coalesce=True,
            misfire_grace_time=None
        )
        
        logger.info("Scheduler started. Agent will run every 10 minutes.")
        scheduler.start()
        # run_agent_wrapper()
        
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
    except Exception as e:
        logger.error(f"Error in scheduler: {e}", exc_info=True)

if __name__ == "__main__":
    main() 