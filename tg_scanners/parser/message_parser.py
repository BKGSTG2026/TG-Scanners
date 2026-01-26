def parse_message(raw_message: str) -> dict:
    """
    Minimal parser for testing end-to-end ingestion.

    For now:
    - Store the raw message as-is
    - Compute its length
    """
    if not isinstance(raw_message, str):
        raise ValueError("Expected raw_message to be a string")

    cleaned = raw_message.strip()

    result = {"raw": cleaned, "length": len(cleaned)}
    print(f"Parsed message: {result}")  # add this line
    return result
