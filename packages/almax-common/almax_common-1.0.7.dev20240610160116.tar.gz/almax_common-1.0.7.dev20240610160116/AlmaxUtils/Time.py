from datetime import datetime, timedelta;

now = datetime.now();

def CalculateTimePassed(start: datetime = 0):
    return datetime.now() - start;

def TimeToString(time: datetime) -> str:
    seconds = time.total_seconds();
    minutes = seconds // 60;
    hours = minutes // 60;
    days = hours // 24;
    return f"{round(days)} Days = {round(hours)} Hours = {round(minutes)} Minutes = {round(seconds, 2)} Seconds";

def GetTimeDesired(AddSeconds: int = 0, Format = "%d-%m-%Y %H:%M:%S") -> str:
    return (datetime.now() + timedelta(seconds=AddSeconds)).strftime(Format);

def LastDayNameOccurence(day_name: str):
    # Dictionary to map day names to their respective numbers
    days = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    # Get today's date
    today = datetime.today();
    
    # Get the current day of the week (0=Monday, 1=Tuesday, ..., 6=Sunday)
    current_day_num = today.weekday();
    
    # Get the desired day of the week number
    desired_day_num = days[day_name.lower()];
    
    # Calculate the difference in days
    delta_days = (current_day_num - desired_day_num) % 7;
    if delta_days == 0:
        delta_days = 7;
    
    # Calculate the last occurrence date
    last_day_date = today - timedelta(days=delta_days);
    
    return last_day_date;