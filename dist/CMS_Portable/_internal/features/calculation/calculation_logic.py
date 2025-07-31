from datetime import date, timedelta
import calendar

def calculate_end_date(start_date: date, duration: int, unit: str) -> date:
    if unit == "Days":
        return start_date + timedelta(days=duration)
    elif unit == "Months":
        # Approximate months to days for simplicity, or implement more precise month addition
        # For precise month addition, consider using relativedelta from dateutil
        year = start_date.year
        month = start_date.month + duration
        while month > 12:
            month -= 12
            year += 1
        day = min(start_date.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)
    elif unit == "Years":
        return date(start_date.year + duration, start_date.month, start_date.day)
    return start_date

def calculate_extended_end_date(end_date: date, extension: int, unit: str) -> date:
    if unit == "Days":
        return end_date + timedelta(days=extension)
    elif unit == "Months":
        year = end_date.year
        month = end_date.month + extension
        while month > 12:
            month -= 12
            year += 1
        day = min(end_date.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)
    elif unit == "Years":
        return date(end_date.year + extension, end_date.month, end_date.day)
    return end_date
