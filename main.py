#!/usr/bin/env python3

import json
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from jira import JIRA
from tqdm import tqdm
from dotenv import load_dotenv

def load_config(config_path="config.local.json"):
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        with open("config.json", 'r') as f:
            return json.load(f)

def connect_to_jira(config):
    """Establish connection to Jira."""
    return JIRA(
        server=config['jira']['server'],
        basic_auth=(config['jira']['email'], config['jira']['api_token'])
    )

def get_test_cycles(jira, config):
    """Retrieve test cycles from Jira."""
    test_cycles = []
    start_at = 0
    
    while True:
        issues = jira.search_issues(
            config['jira']['test_cycle_jql'],
            startAt=start_at,
            maxResults=config['jira']['max_results']
        )
        
        if not issues:
            break
            
        test_cycles.extend(issues)
        start_at += len(issues)
        
        if len(issues) < config['jira']['max_results']:
            break
    
    return test_cycles

def calculate_completion_percentage(test_cycle):
    """Calculate completion percentage for a test cycle."""
    total_tests = 0
    completed_tests = 0
    
    # Get all test cases linked to the test cycle
    links = test_cycle.fields.issuelinks
    for link in links:
        if hasattr(link, 'outwardIssue') and link.outwardIssue.fields.issuetype.name == 'Test Case':
            total_tests += 1
            status = link.outwardIssue.fields.status.name
            if status in ['Done', 'Closed', 'Passed']:
                completed_tests += 1
    
    if total_tests == 0:
        return 0
    
    return (completed_tests / total_tests) * 100

def generate_html_report(data, output_path):
    """Generate an interactive HTML report using Plotly."""
    fig = go.Figure()
    
    for cycle_name in data['test_cycle'].unique():
        cycle_data = data[data['test_cycle'] == cycle_name]
        
        fig.add_trace(go.Scatter(
            x=cycle_data['date'],
            y=cycle_data['completion_percentage'],
            name=cycle_name,
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title='Test Cycle Completion Progress',
        xaxis_title='Date',
        yaxis_title='Completion Percentage',
        yaxis_range=[0, 100],
        showlegend=True
    )
    
    fig.write_html(output_path)

def main():
    # Load configuration
    config = load_config()
    
    # Create output directory if it doesn't exist
    os.makedirs(config['reporting']['output_directory'], exist_ok=True)
    
    # Connect to Jira
    print("Connecting to Jira...")
    jira = connect_to_jira(config)
    
    # Get test cycles
    print("Retrieving test cycles...")
    test_cycles = get_test_cycles(jira, config)
    
    # Calculate completion percentages
    print("Calculating completion percentages...")
    data = []
    
    for test_cycle in tqdm(test_cycles):
        percentage = calculate_completion_percentage(test_cycle)
        
        data.append({
            'test_cycle': test_cycle.fields.summary,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'completion_percentage': percentage,
            'status': test_cycle.fields.status.name,
            'key': test_cycle.key
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Generate reports
    output_dir = config['reporting']['output_directory']
    
    # Save HTML report
    html_path = os.path.join(output_dir, 'test_cycle_report.html')
    print(f"Generating HTML report: {html_path}")
    generate_html_report(df, html_path)
    
    # Save CSV if enabled
    if config['reporting'].get('save_csv', True):
        csv_path = os.path.join(output_dir, 'test_cycle_data.csv')
        print(f"Saving CSV data: {csv_path}")
        df.to_csv(csv_path, index=False)
    
    print("Done! Reports have been generated successfully.")

if __name__ == "__main__":
    main()