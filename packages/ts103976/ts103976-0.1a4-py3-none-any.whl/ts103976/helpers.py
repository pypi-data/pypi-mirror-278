from datetime import datetime


def etsi_datetime():
    return datetime.now(datetime.now().astimezone().tzinfo).isoformat()
