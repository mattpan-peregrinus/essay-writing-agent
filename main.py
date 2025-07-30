"""Main entry point for the essay writer application."""

from dotenv import load_dotenv
_ = load_dotenv()

from cli import main

if __name__ == "__main__":
    main()