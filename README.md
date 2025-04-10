# Jira Test Cycle Tracker

This tool tracks and analyzes test cycle completion percentages in Jira, generating daily reports and visualizations.

## Features

- Retrieves test cycle information from Jira
- Calculates daily completion percentages
- Generates CSV reports with detailed statistics
- Creates interactive HTML visualizations
- Tracks historical test cycle progress

## Prerequisites

- Python 3.8 or higher
- Jira account with API access
- API token from Jira

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kishanatoffice/jira-testcycle-daily-percentage.git
cd jira-testcycle-daily-percentage
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your Jira credentials and settings:
```
JIRA_URL=https://your-domain.atlassian.net
JIRA_TOKEN=your_jira_api_token
JIRA_PROJECT_KEY=YOUR_PROJECT
DAYS_TO_TRACK=7
```

## Usage

Run the script:
```bash
python jira_testcycle_tracker.py
```

The script will:
1. Connect to your Jira instance
2. Retrieve test cycle data
3. Calculate completion percentages
4. Generate reports in the `output` directory:
   - `test_cycle_report.csv`: Detailed statistics in CSV format
   - `test_cycle_visualization.html`: Interactive visualization
   - `test_cycle_trend.png`: Static trend chart

## Output Directory Structure

```
output/
├── test_cycle_report.csv
├── test_cycle_visualization.html
└── test_cycle_trend.png
```

## Security Notes

- Never commit your `.env` file or any files containing sensitive credentials
- Use environment variables for sensitive information
- Keep your API tokens secure

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.