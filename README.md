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

### Running Directly
Run the scheduler directly (will stop when terminal closes):
```bash
python scheduler.py
```

### Running as a Background Service (Linux)

1. Create a systemd service file:
```bash
sudo nano /etc/systemd/system/browser-agent.service
```

2. Add the following content (adjust paths according to your setup):
```ini
[Unit]
Description=Browser Agent Scheduler
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/project/venv/bin"
ExecStart=/path/to/your/project/venv/bin/python scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Start and enable the service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Start the service
sudo systemctl start browser-agent

# Enable service to start on boot
sudo systemctl enable browser-agent
```

4. Managing the service:
```bash
# Check status
sudo systemctl status browser-agent

# Stop the service
sudo systemctl stop browser-agent

# Restart the service
sudo systemctl restart browser-agent

# View logs
sudo journalctl -u browser-agent -f
```

## Configuration

The application uses Google's Gemini Pro model with the following configuration:
- Model: gemini-pro
- Temperature: 0.7 (can be adjusted in scheduler.py)
- System messages are converted to human messages 

The agent will run every 5 minutes by default. You can modify the schedule and tasks in `scheduler.py`. 