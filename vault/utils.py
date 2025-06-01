# utils.py
from isodate import parse_duration

def iso_to_duration(iso_string):
    try:
        return parse_duration(iso_string)  # Returns timedelta
    except Exception as e:
        print(f"Error parsing duration: {e}")
        return None
