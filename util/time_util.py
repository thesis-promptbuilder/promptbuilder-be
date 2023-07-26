from datetime import datetime


def now():
    return datetime.utcnow()


def get_time_string():
    return now().strftime("%Y-%m-%d")
