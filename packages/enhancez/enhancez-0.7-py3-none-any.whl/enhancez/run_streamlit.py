import os
import subprocess


def run():
    # Set the current directory to where this script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run Streamlit from the current directory
    subprocess.run(['streamlit', 'run', 'ZOO.py', '--', 'server.headless=true'])


if __name__ == '__main__':
    run()
