import json
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from jira import JIRA
from dotenv import load_dotenv
from tqdm import tqdm

def load_config():
    """Load configuration from config.json file."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("config.json file not found. Please create one based on the template.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in config.json file.")

def connect_to_jira(config):
    """Establish connection to Jira."""
    load_dotenv()  # Load environment variables from .env file
    
    jira_email = os.getenv('JIRA_EMAIL') or config['jira']['email']
    jira_token = os.getenv('JIRA_TOKEN') or config['jira']['api_token']
    jira_server = config['jira']['server']
    
    try:
        return JIRA(server=jira_server, basic_auth=(jira_email, jira_token))
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Jira: {str(e)}")

def get_test_cycle_data(jira, config):
    """Retrieve test cycle data from Jira."""
    project_key = config['jira']['project_key']
    test_cycle_jql = config['jira'].get('test_cycle_jql', f'project = {project_key} AND issuetype = "Test Cycle"')
    
    try:
        test_cycles = jira.search_issues(test_cycle_jql, maxResults=config['jira'].get('max_results', 50))
        return test_cycles
    except Exception as e:
        raise Exception(f"Failed to fetch test cycle data: {str(e)}")

def calculate_completion_percentage(test_cycle, jira):
    """Calculate completion percentage for a test cycle."""
    total_tests = 0
    completed_tests = 0
    
    # Get all test cases linked to the test cycle
    test_cases = jira.search_issues(f'issue in linkedIssues("{test_cycle.key}") AND issuetype = "Test Case"')
    
    total_tests = len(test_cases)
    if total_tests == 0:
        return 0
    
    for test_case in test_cases:
        status = test_case.fields.status.name.lower()
        if status in ['passed', 'failed', 'blocked']:  # Consider these statuses as completed
            completed_tests += 1
    
    return (completed_tests / total_tests) * 100

def generate_report(test_cycles_data, config):
    """Generate visualization report."""
    df = pd.DataFrame(test_cycles_data)
    
    # Create line plot
    fig = go.Figure()
    
    for cycle_name in df['cycle_name'].unique():
        cycle_data = df[df['cycle_name'] == cycle_name]
        fig.add_trace(go.Scatter(
            x=cycle_data['date'],
            y=cycle_data['percentage'],
            name=cycle_name,
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title='Test Cycle Completion Percentage Over Time',
        xaxis_title='Date',
        yaxis_title='Completion Percentage',
        yaxis_range=[0, 100]
    )
    
    # Save the plot
    output_dir = config['reporting'].get('output_directory', 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    fig.write_html(f'{output_dir}/test_cycle_report_{timestamp}.html')
    
    if config['reporting'].get('save_csv', True):
        df.to_csv(f'{output_dir}/test_cycle_data_{timestamp}.csv', index=False)

def main():
    try:
        # Load configuration
        config = load_config()
        
        # Connect to Jira
        jira = connect_to_jira(config)
        
        # Get test cycles
        test_cycles = get_test_cycle_data(jira, config)
        
        # Process test cycles
        test_cycles_data = []
        print("Processing test cycles...")
        for test_cycle in tqdm(test_cycles):
            percentage = calculate_completion_percentage(test_cycle, jira)
            
            test_cycles_data.append({
                'cycle_name': test_cycle.fields.summary,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'percentage': percentage
            })
        
        # Generate report
        generate_report(test_cycles_data, config)
        print("Report generated successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())