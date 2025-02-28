# Browser-Use Agent Scheduler

This application runs browser-use agents on a schedule using Python's APScheduler and Google's Generative AI (Gemini).

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
GOOGLE_API_KEY=your_google_api_key_here
```

To get a Google API key:
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key and paste it in your `.env` file

## Usage

Run the scheduler:
```bash
python scheduler.py
```

The agent will run every 15 minutes. You can modify the schedule and task in `scheduler.py`.

## Configuration

The application uses Google's Gemini Pro model with the following configuration:
- Model: gemini-pro
- Temperature: 0.7 (can be adjusted in scheduler.py)
- System messages are converted to human messages 