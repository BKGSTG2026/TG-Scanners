"""
Logic for parsing 'messages' either mock messages or 'real' ones. 
This logic is not correct- just used for a POC
"""

PREFIX_LEN=4
TAG_STATUS_LEN=7
EPC_LEN=19
DAT_LEN=15

# Format should follow the line directly below - data currently parsed is INVALID and just used as a POC
# <prefix> [<tagstatus>] [<epclen>] [<epc>] [<datlen>] [<data>] <suffix> [CR/LF]

# Running as-is with string like the below, parses into the following:
# 400180004000290E34004E201914DB92C00000000000
# <prefix> <tag_status> <epc>                       <dat>
# <4001>   <8>          <0004000290E34004E201914DB> <92C00000000000>

def parse_message(raw_message: str) -> dict:
    """
    Minimal parser for testing end-to-end ingestion.

    Just chose arbitrary ranges for values
    """
    if not isinstance(raw_message, str):
        raise ValueError("Expected raw_message to be a string")

    cleaned = raw_message.strip()


    result = {"raw": cleaned, 
        "length": len(cleaned),
        "prefix": cleaned[:PREFIX_LEN],
        "tag_status": cleaned[PREFIX_LEN:PREFIX_LEN+TAG_STATUS_LEN],
        "epc": cleaned[PREFIX_LEN+TAG_STATUS_LEN:PREFIX_LEN+TAG_STATUS_LEN+EPC_LEN],
        "dat": cleaned[PREFIX_LEN+TAG_STATUS_LEN+EPC_LEN:PREFIX_LEN+TAG_STATUS_LEN+EPC_LEN+DAT_LEN]
    }
    # Debug message - TODO: Configure debug logging with optional flag
    print(f"Parsed message: {result}")
    return result
