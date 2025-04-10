# Jira Test Cycle Percentage Tracker

A Python script to track and visualize test cycle completion percentages from Jira. This tool helps teams monitor their testing progress by generating daily reports with completion percentages and trends.

## Features

- Connect to Jira using API authentication
- Retrieve test cycles based on configurable JQL
- Calculate completion percentages for test cycles
- Generate HTML reports with interactive charts using Plotly
- Export data to CSV files (optional)
- Configurable settings via JSON configuration file

## Prerequisites

- Python 3.7 or higher
- Jira account with API access
- Required Python packages (install via pip):
  - requests
  - pandas
  - plotly
  - jira

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kishanatoffice/jira-testcycle-daily-percentage.git
cd jira-testcycle-daily-percentage
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a local configuration file:
```bash
cp config.json config.local.json
```

4. Edit `config.local.json` with your Jira credentials and settings:
```json
{
    "jira": {
        "server": "https://your-jira-instance.com",
        "email": "your.email@company.com",
        "api_token": "your-api-token",
        "test_cycle_jql": "project = 'Your Project' AND issuetype = 'Test Cycle'"
    },
    "reporting": {
        "output_dir": "reports",
        "save_csv": true
    }
}
```

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Connect to your Jira instance
2. Retrieve test cycles based on the configured JQL
3. Calculate completion percentages
4. Generate an HTML report with interactive charts
5. Save data to CSV if enabled in configuration

## Output

- HTML reports are generated in the configured output directory
- Reports include:
  - Daily completion percentages for each test cycle
  - Trend analysis over time
  - Interactive charts for data visualization
- Optional CSV export of raw data

## Configuration Options

### Jira Settings
- `server`: Your Jira instance URL
- `email`: Your Jira account email
- `api_token`: Your Jira API token
- `test_cycle_jql`: JQL query to identify test cycles

### Reporting Settings
- `output_dir`: Directory for generated reports
- `save_csv`: Enable/disable CSV export

## Security Notes

- Never commit `config.local.json` with your credentials
- Use environment variables for sensitive data in production
- Keep your API token secure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.