# Browser-Use Agent Scheduler

This application runs browser-use agents on a schedule using Python's APScheduler.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

3. Create a `.env` file with your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

Run the scheduler:
```bash
python scheduler.py
```

The agent will run every 15 minutes. You can modify the schedule and task in `scheduler.py`. 