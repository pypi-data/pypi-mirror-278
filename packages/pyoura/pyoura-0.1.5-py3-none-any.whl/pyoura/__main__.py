import argparse
from pyoura import create_ora

def main():
    """
    Entry point for the command-line interface.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="A Python library for creating command-line spinners")
    parser.add_argument("spinner", type=str, help="The type of spinner to display")
    parser.add_argument("text", type=str, nargs="?", default="Loading...", help="The text to display")
    args = parser.parse_args()

    # Create the spinner
    spinner = create_ora(text=args.text, spinner=args.spinner)
    spinner.start()

    # Your main function logic here
    # For demonstration, let's just wait for a few seconds
    import time
    time.sleep(5)

    # Stop the spinner
    spinner.stop()

if __name__ == "__main__":
    main()
