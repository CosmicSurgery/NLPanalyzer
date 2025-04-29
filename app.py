import argparse
import os
import subprocess

# modules
from data import processor

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='NLPanalyzer CLI tool')
    
    # Add the arguments
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--process', action='store_true', help='Process the data')
    group.add_argument('--dashboard', action='store_true', help='Launch the interactive dashboard')
    group.add_argument('--report', action='store_true', help='Generate a static report')
    group.add_argument('--clear', action='store_true', help='Clear all chat data in memory and reset all log files')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Execute the appropriate function based on the argument
    if args.process:
        process_data()
    elif args.dashboard:
        launch_dashboard()
    elif args.report:
        generate_report()
    elif args.clear:
        clear_data()
    else:
        parser.print_help()

def clear_data():
    print("Clearing data...")
    try:
        os.remove(os.path.join(os.getcwd(), 'data', 'status.log'))
        os.remove(os.path.join(os.getcwd(), 'vis', 'data.h5'))
    except:
        print("logs already deleted.")
        try:
            os.remove(os.path.join(os.getcwd(), 'vis', 'data.h5'))
        except:
            print("h5 files already deleted.")
    

def process_data():
    print("Processing data...")
    # Add your data processing logic here
    processor.main(PATH=os.path.join(os.getcwd(),'data'))

def launch_dashboard():
    print("Launching interactive dashboard...")
    result = subprocess.run(['cmd','/c', 'bokeh serve --show vis --port 8000'])
    print(result.stdout)
    # Add your dashboard launching logic here

def generate_report():
    print("Generating static report...")
    # Add your report generation logic here

if __name__ == "__main__":
    main()