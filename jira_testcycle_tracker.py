#!/usr/bin/env python3
"""
Jira Test Cycle Percentage Tracker
This script connects to Jira, retrieves test cycles, and calculates completion percentages.
"""

import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from jira import JIRA
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

class JiraTestCycleTracker:
    def __init__(self):
        """Initialize the Jira connection and configuration."""
        self.jira_url = os.getenv('JIRA_URL')
        self.jira_token = os.getenv('JIRA_TOKEN')
        self.project_key = os.getenv('JIRA_PROJECT_KEY')
        
        if not all([self.jira_url, self.jira_token, self.project_key]):
            print("Error: Missing required environment variables.")
            sys.exit(1)
            
        try:
            self.jira = JIRA(
                server=self.jira_url,
                token_auth=self.jira_token
            )
        except Exception as e:
            print(f"Error connecting to Jira: {str(e)}")
            sys.exit(1)

    def get_test_cycles(self, days_back=7):
        """
        Retrieve test cycles from the specified date range.
        
        Args:
            days_back (int): Number of days to look back for test cycles
            
        Returns:
            list: List of test cycles with their details
        """
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        jql_query = f'project = {self.project_key} AND issuetype = "Test Cycle" AND created >= "{start_date}" ORDER BY created DESC'
        
        try:
            test_cycles = self.jira.search_issues(jql_query, maxResults=50)
            return test_cycles
        except Exception as e:
            print(f"Error retrieving test cycles: {str(e)}")
            return []

    def calculate_completion_percentage(self, test_cycle):
        """
        Calculate the completion percentage for a test cycle.
        
        Args:
            test_cycle: Jira issue object representing a test cycle
            
        Returns:
            float: Completion percentage
        """
        try:
            total_tests = 0
            completed_tests = 0
            
            # Get all test cases linked to this cycle
            links = test_cycle.fields.issuelinks
            for link in links:
                if hasattr(link, 'outwardIssue') and link.outwardIssue.fields.issuetype.name == 'Test Case':
                    total_tests += 1
                    status = link.outwardIssue.fields.status.name
                    if status in ['Done', 'Closed', 'Passed']:
                        completed_tests += 1
            
            return (completed_tests / total_tests * 100) if total_tests > 0 else 0
        except Exception as e:
            print(f"Error calculating completion percentage: {str(e)}")
            return 0

    def generate_report(self, days_back=7):
        """
        Generate a report of test cycle completion percentages.
        
        Args:
            days_back (int): Number of days to include in the report
            
        Returns:
            tuple: (DataFrame with report data, HTML string of the plot)
        """
        test_cycles = self.get_test_cycles(days_back)
        
        data = []
        for cycle in test_cycles:
            completion_percentage = self.calculate_completion_percentage(cycle)
            data.append({
                'Test Cycle': cycle.fields.summary,
                'Created Date': cycle.fields.created,
                'Status': cycle.fields.status.name,
                'Completion Percentage': completion_percentage
            })
        
        if not data:
            return None, None
        
        df = pd.DataFrame(data)
        df['Created Date'] = pd.to_datetime(df['Created Date'])
        df = df.sort_values('Created Date')
        
        # Create visualization
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Created Date'],
            y=df['Completion Percentage'],
            mode='lines+markers',
            name='Completion %',
            line=dict(color='#2E86C1', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Test Cycle Completion Percentages Over Time',
            xaxis_title='Date',
            yaxis_title='Completion Percentage (%)',
            template='plotly_white',
            hovermode='x unified'
        )
        
        # Save plot as HTML and image
        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        fig.write_image("test_cycle_trend.png")
        
        return df, plot_html

    def save_report(self, df, plot_html):
        """
        Save the report to files.
        
        Args:
            df (DataFrame): Report data
            plot_html (str): HTML string of the plot
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save DataFrame to CSV
        csv_filename = f'test_cycle_report_{timestamp}.csv'
        df.to_csv(csv_filename, index=False)
        
        # Save plot HTML
        html_filename = f'test_cycle_report_{timestamp}.html'
        with open(html_filename, 'w') as f:
            f.write(f"""
            <html>
            <head>
                <title>Test Cycle Completion Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1 {{ color: #2E86C1; }}
                    .container {{ max-width: 1200px; margin: 0 auto; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Test Cycle Completion Report</h1>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    {plot_html}
                </div>
            </body>
            </html>
            """)

def main():
    """Main function to run the Jira test cycle tracker."""
    tracker = JiraTestCycleTracker()
    
    try:
        print("Generating test cycle report...")
        df, plot_html = tracker.generate_report()
        
        if df is not None and plot_html is not None:
            tracker.save_report(df, plot_html)
            print("Report generated successfully!")
            print(f"Average completion percentage: {df['Completion Percentage'].mean():.2f}%")
        else:
            print("No test cycles found in the specified date range.")
            
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()