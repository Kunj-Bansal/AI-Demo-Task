from datetime import datetime, timezone, timedelta
import dateparser

def parse_and_validate_freshness(date_str: str) -> tuple[str | None, bool]:
    """
    Parses dynamic date strings and returns an ISO-8601 string 
    along with a boolean indicating if it's within the last 24 hours.
    """
    if not date_str:
        return None, False
        
    # Parse relative or absolute date
    parsed_dt = dateparser.parse(date_str, settings={'TIMEZONE': 'UTC', 'RETURN_AS_TIMEZONE_AWARE': True})
    
    if not parsed_dt:
        return None, False

    now = datetime.now(timezone.utc)
    is_fresh = (now - parsed_dt) <= timedelta(hours=24)
    
    return parsed_dt.isoformat(), is_fresh