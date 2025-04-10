# Jira Test Cycle Percentage Tracker

This Python script tracks and reports on Jira test cycle completion percentages. It generates daily reports and visualizations to help track testing progress over time.

## Features

- Retrieves test cycles from Jira
- Calculates completion percentages based on test case status
- Generates CSV reports with detailed statistics
- Creates interactive HTML visualizations using Plotly
- Tracks historical data over configurable time periods

## Prerequisites

- Python 3.8 or higher
- Jira account with API access
- Required Python packages (see requirements.txt)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kishanatoffice/jira-testcycle-daily-percentage.git
   cd jira-testcycle-daily-percentage
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```

4. Configure your Jira credentials in the `.env` file:
   - `JIRA_URL`: Your Jira instance URL
   - `JIRA_TOKEN`: Your Jira API token
   - `JIRA_PROJECT_KEY`: Your Jira project key

## Usage

Run the script:
```bash
python jira_testcycle_tracker.py
```

The script will:
1. Connect to your Jira instance
2. Retrieve test cycles from the last 7 days
3. Calculate completion percentages
4. Generate reports in the `reports` directory:
   - CSV report with detailed statistics
   - HTML visualization of completion trends

## Output

The script generates two types of reports:
1. CSV Reports (`reports/testcycle_report_YYYY-MM-DD.csv`):
   - Test cycle details
   - Completion percentages
   - Test case counts
   - Status breakdown

2. HTML Visualizations (`reports/testcycle_visualization_YYYY-MM-DD.html`):
   - Interactive completion trend charts
   - Daily progress visualization
   - Status distribution plots

## Configuration

Optional environment variables in `.env`:
- `DAYS_TO_TRACK`: Number of days to look back (default: 7)

## Error Handling

The script includes comprehensive error handling for:
- Jira connection issues
- Missing environment variables
- Invalid data formats
- File I/O operations

## Contributing

Feel free to submit issues and enhancement requests!