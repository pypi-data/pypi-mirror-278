import argparse

def main():
    """
    Entry point for the command-line interface.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="A Python library for creating command-line spinners")
    parser.add_argument("spinner", type=str, help="The type of spinner to display")
    parser.add_argument("text", type=str, nargs="?", default="Loading...", help="The text to display")
    args = parser.parse_args()

    # Your main function logic here
    print(f"Using spinner: {args.spinner}")
    print(f"Text to display: {args.text}")

if __name__ == "__main__":
    main()
