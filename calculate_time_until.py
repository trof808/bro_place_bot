from datetime import datetime

def calculate_time_until(target_year, target_month, target_day, target_hour, target_minute, target_second):
    # Get the current date and time
    current_datetime = datetime.now()

    # Create a datetime object for the target date and time
    target_datetime = datetime(target_year, target_month, target_day, target_hour, target_minute, target_second)

    # Calculate the difference between current and target datetime
    time_difference = target_datetime - current_datetime

    # Extract days, seconds, and remaining seconds
    days = time_difference.days
    seconds = time_difference.seconds
    remaining_seconds = seconds % 60
    seconds //= 60

    # Extract hours and remaining minutes
    hours = seconds // 60
    remaining_minutes = seconds % 60

    return days, hours, remaining_minutes, remaining_seconds
