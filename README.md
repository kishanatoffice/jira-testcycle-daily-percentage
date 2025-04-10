# Jira Test Cycle Daily Percentage Tracker

This tool tracks and visualizes the completion percentage of Jira test cycles on a daily basis. It generates reports in both HTML (interactive charts) and CSV formats.

## Features

- Connects to Jira using API authentication
- Retrieves test cycle data using customizable JQL queries
- Calculates completion percentages for test cases linked to test cycles
- Generates interactive visualizations using Plotly
- Supports CSV export for further analysis
- Configurable through a JSON configuration file

## Prerequisites

- Python 3.7 or higher
- Jira account with API access
- Required Python packages (install using pip):
  ```bash
  pip install -r requirements.txt
  ```

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/kishanatoffice/jira-testcycle-daily-percentage.git
   cd jira-testcycle-daily-percentage
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `config.json` to create your configuration:
   ```bash
   cp config.json config.local.json
   ```

4. Edit `config.local.json` with your Jira settings:
   - Update the Jira server URL
   - Add your email and API token
   - Configure your project key and JQL query
   - Adjust reporting settings if needed

## Configuration

The `config.json` file contains the following settings:

```json
{
    "jira": {
        "server": "https://your-domain.atlassian.net",
        "email": "your-email@example.com",
        "api_token": "your-api-token",
        "project_key": "YOUR_PROJECT",
        "test_cycle_jql": "project = YOUR_PROJECT AND issuetype = 'Test Cycle'",
        "max_results": 50
    },
    "reporting": {
        "output_directory": "reports",
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
2. Retrieve test cycle data
3. Calculate completion percentages
4. Generate reports in the specified output directory

## Output

- HTML report with interactive charts (`reports/test_cycle_report.html`)
- CSV file with raw data (`reports/test_cycle_data.csv`) if enabled

## Security Notes

- Never commit your actual Jira credentials to version control
- Use environment variables or a local config file for sensitive data
- Keep your API token secure and rotate it periodically

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.