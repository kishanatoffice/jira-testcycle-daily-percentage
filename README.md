# Jira Test Cycle Daily Percentage Tracker

A tool for tracking and visualizing Jira test cycle completion percentages on a daily basis.

## Features

- Daily tracking of test cycle completion percentages
- Automated data collection from Jira
- Customizable visualization options
- Configurable reporting settings

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kishanatoffice/jira-testcycle-daily-percentage.git
   cd jira-testcycle-daily-percentage
   ```

2. Configure your settings:
   - Copy `config.json` to `config.local.json`
   - Update the configuration with your Jira credentials and preferences

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The `config.json` file contains all necessary settings:

- Jira settings (baseUrl, credentials, project key)
- Reporting preferences (output path, date format)
- Visualization options (chart type, colors)

## Usage

Run the tool:
```bash
python main.py
```

## Security Note

Never commit your actual Jira credentials to the repository. Use environment variables or a local configuration file for sensitive data.

## License

MIT License