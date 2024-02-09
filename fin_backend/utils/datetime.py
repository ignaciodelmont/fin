import datetime


def now() -> str:
    """
    Returns now in ISO format
    """
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
