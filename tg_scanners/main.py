import argparse
from tg_scanners.listener.factory import build_message_source
from tg_scanners.parser.message_parser import parse_message
from tg_scanners.db.repository import MessageRepository

def main():
    # Add command-line args for passing '--mode' arg
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["mock", "server"],
        default="mock",
        help="Run mode"
    )
    
    # Parse args
    args = parser.parse_args()

    # Intialize db connection
    repository = MessageRepository()

    # Initialize either mock messages or TCP/IP messages
    source = build_message_source()

    # For each message (either mock or real) push them to the database
    for message in source.listen():
        repository.save(message)

if __name__ == "__main__":
    main()