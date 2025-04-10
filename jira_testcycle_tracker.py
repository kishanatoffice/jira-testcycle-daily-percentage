#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JiraTestCycleTracker:
    def __init__(self):
        """Initialize the Jira Test Cycle Tracker with configuration from environment variables."""
        self._load_config()
        self._setup_jira_session()
        self._ensure_reports_directory()

    def _load_config(self):
        """Load configuration from environment variables."""
        load_dotenv()
        
        # Required configuration
        self.jira_url = os.getenv('JIRA_URL')
        self.jira_token = os.getenv('JIRA_TOKEN')
        self.project_key = os.getenv('JIRA_PROJECT_KEY')
        
        # Optional configuration
        self.days_to_track = int(os.getenv('DAYS_TO_TRACK', '7'))
        
        if not all([self.jira_url, self.jira_token, self.project_key]):
            raise ValueError("Missing required environment variables. Please check .env file.")

    def _setup_jira_session(self):
        """Set up the Jira session with authentication."""
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.jira_token}',
            'Content-Type': 'application/json'
        })

    def _ensure_reports_directory(self):
        """Create reports directory if it doesn't exist."""
        self.reports_dir = Path('reports')
        self.reports_dir.mkdir(exist_ok=True)

    def get_test_cycles(self, days=None):
        """
        Retrieve test cycles from Jira for the specified number of days.
        
        Args:
            days (int): Number of days to look back (default: self.days_to_track)
            
        Returns:
            list: List of test cycles
        """
        days = days or self.days_to_track
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            url = f"{self.jira_url}/rest/api/3/search"
            jql = (
                f'project = {self.project_key} '
                f'AND created >= "{start_date}" '
                'AND type = "Test Cycle"'
            )
            
            response = self.session.get(
                url,
                params={
                    'jql': jql,
                    'fields': 'key,summary,created,status,customfield_10016'  # Add relevant fields
                }
            )
            response.raise_for_status()
            
            return response.json()['issues']
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving test cycles: {e}")
            return []

    def calculate_completion_percentage(self, test_cycle):
        """
        Calculate completion percentage for a test cycle.
        
        Args:
            test_cycle (dict): Test cycle data from Jira
            
        Returns:
            dict: Completion statistics
        """
        try:
            # Get test cases for the cycle
            url = f"{self.jira_url}/rest/api/3/search"
            jql = f'parent = {test_cycle["key"]}'
            
            response = self.session.get(
                url,
                params={
                    'jql': jql,
                    'fields': 'status'
                }
            )
            response.raise_for_status()
            
            test_cases = response.json()['issues']
            total_cases = len(test_cases)
            
            if total_cases == 0:
                return {
                    'cycle_key': test_cycle['key'],
                    'total_cases': 0,
                    'completed_cases': 0,
                    'completion_percentage': 0,
                    'status_breakdown': {}
                }
            
            # Count cases by status
            status_counts = {}
            completed_cases = 0
            
            for case in test_cases:
                status = case['fields']['status']['name']
                status_counts[status] = status_counts.get(status, 0) + 1
                
                # Consider 'Done' and 'Passed' as completed statuses
                if status.lower() in ['done', 'passed']:
                    completed_cases += 1
            
            completion_percentage = (completed_cases / total_cases) * 100
            
            return {
                'cycle_key': test_cycle['key'],
                'total_cases': total_cases,
                'completed_cases': completed_cases,
                'completion_percentage': round(completion_percentage, 2),
                'status_breakdown': status_counts
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calculating completion for {test_cycle['key']}: {e}")
            return None

    def generate_reports(self):
        """Generate CSV and HTML reports for test cycle completion statistics."""
        logger.info("Generating reports...")
        
        # Get test cycles
        test_cycles = self.get_test_cycles()
        if not test_cycles:
            logger.warning("No test cycles found for the specified period.")
            return
        
        # Calculate completion statistics
        stats = []
        for cycle in test_cycles:
            cycle_stats = self.calculate_completion_percentage(cycle)
            if cycle_stats:
                stats.append({
                    'Date': datetime.fromisoformat(cycle['fields']['created'].split('T')[0]),
                    'Cycle': cycle['key'],
                    'Summary': cycle['fields']['summary'],
                    'Total Cases': cycle_stats['total_cases'],
                    'Completed Cases': cycle_stats['completed_cases'],
                    'Completion %': cycle_stats['completion_percentage'],
                    'Status Breakdown': json.dumps(cycle_stats['status_breakdown'])
                })
        
        if not stats:
            logger.warning("No statistics to report.")
            return
        
        # Create DataFrame
        df = pd.DataFrame(stats)
        
        # Generate CSV report
        csv_path = self.reports_dir / f'testcycle_report_{datetime.now().strftime("%Y-%m-%d")}.csv'
        df.to_csv(csv_path, index=False)
        logger.info(f"CSV report generated: {csv_path}")
        
        # Generate visualization
        self._create_visualization(df)

    def _create_visualization(self, df):
        """
        Create an interactive visualization using Plotly.
        
        Args:
            df (pandas.DataFrame): Test cycle statistics
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Test Cycle Completion Trend', 'Daily Progress'),
            vertical_spacing=0.2
        )
        
        # Completion trend
        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['Completion %'],
                mode='lines+markers',
                name='Completion %'
            ),
            row=1, col=1
        )
        
        # Daily progress
        daily_stats = df.groupby('Date').agg({
            'Total Cases': 'sum',
            'Completed Cases': 'sum'
        }).reset_index()
        
        fig.add_trace(
            go.Bar(
                x=daily_stats['Date'],
                y=daily_stats['Total Cases'],
                name='Total Cases',
                marker_color='lightgray'
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=daily_stats['Date'],
                y=daily_stats['Completed Cases'],
                name='Completed Cases',
                marker_color='green'
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title_text='Test Cycle Progress Report',
            showlegend=True,
            height=800
        )
        
        # Save visualization
        html_path = self.reports_dir / f'testcycle_visualization_{datetime.now().strftime("%Y-%m-%d")}.html'
        fig.write_html(str(html_path))
        logger.info(f"HTML visualization generated: {html_path}")

def main():
    """Main function to run the Jira Test Cycle Tracker."""
    try:
        tracker = JiraTestCycleTracker()
        tracker.generate_reports()
        logger.info("Report generation completed successfully.")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()