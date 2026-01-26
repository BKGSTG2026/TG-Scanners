from tg_scanners.listener.factory import build_message_source
from tg_scanners.parser.message_parser import parse_message
from tg_scanners.db.repository import MessageRepository

def main() -> None:
    repository = MessageRepository()

    def handle_message(raw_message: str) -> None:
        parsed = parse_message(raw_message)
        # repository.save({"raw": "TEST_INSERT", "length": 11})
        repository.save(parsed)

    source = build_message_source()
    source.start(handle_message)

if __name__ == "__main__":
    main()

