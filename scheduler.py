from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from playwright.async_api import BrowserContext
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
import asyncio
import logging
import os

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
    """Run the browser-use agent with the specified task."""
    try:
        initial_actions = [
            {'open_tab': {'url': 'https://x.com/home'}},
            {'scroll_down': {'amount': 1000}},
        ]
        # Initialize the agent with your task
        agent = Agent(
            task=(
                "Navigate to the search page at https://x.com/search?q=suno%20music&src=typed_query&f=live "
                "and wait for it to fully load. Once the page is loaded,"
                "click on a post that was not created by sontl. Like the relevant post by clicking the heart-shaped "
                "\"Like\" button, then click the \"Comment\" button (message icon) to open the comment modal. "
                "Write a short, relevant comment based on the post and comments, mimicking a real human response, "
                "and ensure to answer in the language of the post. Finally, click the \"Reply\" button to submit "
                "your comment and complete the task."
            ),  # Customize this with your specific task
            llm=ChatGoogleGenerativeAI(
                model="gemini-2.0-pro-exp-02-05",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.7,
                convert_system_message_to_human=True
            ),
            browser=browser,
            use_vision=True,
            save_conversation_path="logs/conversation",
            initial_actions=initial_actions
        )
        
        # Run the agent and get the result
        result = await agent.run()
        
        # Log the result
        logger.info(f"Agent execution completed. Result: {result}")
        
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
        
        # Add job to run every 15 minutes
        scheduler.add_job(
            run_agent_wrapper,
            CronTrigger(minute='*/13'),  # Run every 15 minutes
            name='browser_agent_job',
            max_instances=1,
            coalesce=True,
            misfire_grace_time=None
        )
        
        logger.info("Scheduler started. Agent will run every 13 minutes.")
        scheduler.start()
        run_agent_wrapper()
        
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
    except Exception as e:
        logger.error(f"Error in scheduler: {e}", exc_info=True)

if __name__ == "__main__":
    main() 