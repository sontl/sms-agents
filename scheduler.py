from langchain_openai import ChatOpenAI
from browser_use import Agent
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
import asyncio
import logging

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

# Load environment variables
load_dotenv()

async def run_agent():
    """Run the browser-use agent with the specified task."""
    try:
        # Initialize the agent with your task
        agent = Agent(
            task="Your task description here",  # Customize this with your specific task
            llm=ChatOpenAI(model="gpt-4"),  # You can change the model as needed
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
            CronTrigger(minute='*/15'),  # Run every 15 minutes
            name='browser_agent_job',
            max_instances=1,
            coalesce=True,
            misfire_grace_time=None
        )
        
        logger.info("Scheduler started. Agent will run every 15 minutes.")
        scheduler.start()
        
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
    except Exception as e:
        logger.error(f"Error in scheduler: {e}", exc_info=True)

if __name__ == "__main__":
    main() 