import argparse
from pyoura.spinners import Oura
import time

def main():
    """
    Entry point for the command-line interface.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="A Python library for creating command-line spinners")
    parser.add_argument("spinner", type=str, help="The type of spinner to display")
    parser.add_argument("text", type=str, nargs="?", default="Loading...", help="The text to display")
    args = parser.parse_args()

    spinner = Oura()
    # Create an instance of the Oura class with a specific spinner type
    spinner = Oura(spinner=args.spinner,color="cyan")

    # Start the spinner with a custom message
    spinner.start(args.text)
    # Simulate some task
    time.sleep(5)
    # Stop the spinner and display a success message
    spinner.succeed("Finished successfully")

if __name__ == "__main__":
    main()
