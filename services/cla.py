import argparse

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Health monitor for API endpoints")
    parser.add_argument("--check", action="store_true", help="Run a single check")
    parser.add_argument("--watch", action="store_true", help="Run checks every 60 seconds")
    parser.add_argument("--quiet", action="store_true", help="Disable Slack notifications")
    return parser.parse_args()