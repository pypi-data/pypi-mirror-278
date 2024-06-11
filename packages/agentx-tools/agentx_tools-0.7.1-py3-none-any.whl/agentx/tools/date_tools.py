from langchain_core.tools import tool
from datetime import datetime, timedelta

class DateTools():
    @tool("get_current_date")
    def get_current_date():
        """Useful to get the current day, month, and year.

        Returns:
            dict: A dictionary containing the current day, month, and year.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 5
                    }
        """
        now = datetime.now()
        current_date = {
            "year": now.year,
            "month": now.month,
            "day": now.day
        }
        return current_date

    @tool("get_current_time")
    def get_current_time():
        """Useful to get the current hour, minute, and second.

        Returns:
            dict: A dictionary containing the current hour, minute, and second.
                Example:
                    {
                        "hour": 14,
                        "minute": 30,
                        "second": 45
                    }
        """
        now = datetime.now()
        current_time = {
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second
        }
        return current_time

    @tool("get_date_after_days")
    def get_date_after_days(days: int):
        """Useful to get the date after a specified number of days from today.

        Args:
            days (int): The number of days to add to the current date.
                Example: 10

        Returns:
            dict: A dictionary containing the year, month, and day of the future date.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 15
                    }
        """
        future_date = datetime.now() + timedelta(days=days)
        date_after_days = {
            "year": future_date.year,
            "month": future_date.month,
            "day": future_date.day
        }
        return date_after_days

    @tool("get_date_before_days")
    def get_date_before_days(days: int):
        """Useful to get the date before a specified number of days from today.

        Args:
            days (int): The number of days to subtract from the current date.
                Example: 10

        Returns:
            dict: A dictionary containing the year, month, and day of the past date.
                Example:
                    {
                        "year": 2023,
                        "month": 9,
                        "day": 25
                    }
        """
        past_date = datetime.now() - timedelta(days=days)
        date_before_days = {
            "year": past_date.year,
            "month": past_date.month,
            "day": past_date.day
        }
        return date_before_days
    
    @tool("get_first_day_of_month")
    def get_first_day_of_month(year: int, month: int):
        """Useful to get the first day of a given month.

        Args:
            year (int): The year.
                Example: 2023
            month (int): The month.
                Example: 10

        Returns:
            dict: A dictionary containing the year, month, and day of the first day of the month.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 1
                    }
        """
        first_day = datetime(year, month, 1)
        return {"year": first_day.year, "month": first_day.month, "day": first_day.day}

    @tool("get_last_day_of_month")
    def get_last_day_of_month(year: int, month: int):
        """Useful to get the last day of a given month.

        Args:
            year (int): The year.
                Example: 2023
            month (int): The month.
                Example: 10

        Returns:
            dict: A dictionary containing the year, month, and day of the last day of the month.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 31
                    }
        """
        next_month = datetime(year, month, 1) + timedelta(days=31)
        last_day = next_month - timedelta(days=next_month.day)
        return {"year": last_day.year, "month": last_day.month, "day": last_day.day}

    @tool("get_next_month")
    def get_next_month(year: int, month: int):
        """Useful to get the next month.

        Args:
            year (int): The year.
                Example: 2023
            month (int): The month.
                Example: 10

        Returns:
            dict: A dictionary containing the year and month of the next month.
                Example:
                    {
                        "year": 2023,
                        "month": 11
                    }
        """
        next_month = datetime(year, month, 1) + timedelta(days=31)
        return {"year": next_month.year, "month": next_month.month}

    @tool("get_previous_month")
    def get_previous_month(year: int, month: int):
        """Useful to get the previous month.

        Args:
            year (int): The year.
                Example: 2023
            month (int): The month.
                Example: 10

        Returns:
            dict: A dictionary containing the year and month of the previous month.
                Example:
                    {
                        "year": 2023,
                        "month": 9
                    }
        """
        previous_month = datetime(year, month, 1) - timedelta(days=1)
        return {"year": previous_month.year, "month": previous_month.month}

    @tool("get_next_year")
    def get_next_year(year: int):
        """Useful to get the next year.

        Args:
            year (int): The year.
                Example: 2023

        Returns:
            int: The next year.
                Example: 2024
        """
        return year + 1

    @tool("get_previous_year")
    def get_previous_year(year: int):
        """Useful to get the previous year.

        Args:
            year (int): The year.
                Example: 2023

        Returns:
            int: The previous year.
                Example: 2022
        """
        return year - 1

    @tool("get_days_in_month")
    def get_days_in_month(year: int, month: int):
        """Useful to get the number of days in a given month.

        Args:
            year (int): The year.
                Example: 2023
            month (int): The month.
                Example: 10

        Returns:
            int: The number of days in the month.
                Example: 31
        """
        next_month = datetime(year, month, 1) + timedelta(days=31)
        return (next_month - timedelta(days=next_month.day)).day


    @tool("get_week_number")
    def get_week_number(date: dict):
        """Useful to get the week number for a given date.

        Args:
            date (dict): A dictionary containing the year, month, and day.
                Example:
                    {
                        "year": 2023,
                        "month": 6,
                        "day": 10
                    }

        Returns:
            int: The week number of the date.
        """
        date_obj = datetime(date["year"], date["month"], date["day"])
        week_number = date_obj.isocalendar()[1]
        return week_number

    @tool()
    def get_quarter(month: int):
        """Useful to get the quarter of a given month.

        Args:
            month (int): The month.
                Example: 10

        Returns:
            int: The quarter (1-4).
                Example: 4
        """
        return (month - 1) // 3 + 1

    @tool()
    def get_date_from_week_and_year(week: int, year: int):
        """Useful to get the date from a given week number and year.

        Args:
            week (int): The week number (1-52).
                Example: 40
            year (int): The year.
                Example: 2023

        Returns:
            dict: A dictionary containing the year, month, and day of the date.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 5
                    }
        """
        first_day_of_year = datetime(year, 1, 1)
        date_obj = first_day_of_year + timedelta(weeks=week-1)
        return {"year": date_obj.year, "month": date_obj.month, "day": date_obj.day}

    @tool("get_date_from_day_of_year")
    def get_date_from_day_of_year(day_of_year: int, year: int):
        """Useful to get the date from a given day of the year and year.

        Args:
            day_of_year (int): The day of the year (1-365 or 1-366 for leap years).
                Example: 278
            year (int): The year.
                Example: 2023

        Returns:
            dict: A dictionary containing the year, month, and day of the date.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 5
                    }
        """
        first_day_of_year = datetime(year, 1, 1)
        date_obj = first_day_of_year + timedelta(days=day_of_year-1)
        return {"year": date_obj.year, "month": date_obj.month, "day": date_obj.day}

    @tool("get_day_of_year")
    def get_day_of_year(date: dict):
        """Useful to get the day of the year for a given date.

        Args:
            date (dict): A dictionary containing the year, month, and day.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 5
                    }

        Returns:
            int: The day of the year (1-365 or 1-366 for leap years).
                Example: 278
        """
        date_obj = datetime(date["year"], date["month"], date["day"])
        first_day_of_year = datetime(date["year"], 1, 1)
        return (date_obj - first_day_of_year).days + 1

    @tool("get_days_until_end_of_year")
    def get_days_until_end_of_year(date: dict):
        """Useful to get the number of days until the end of the year for a given date.

        Args:
            date (dict): A dictionary containing the year, month, and day.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 5
                    }

        Returns:
            int: The number of days until the end of the year.
                Example: 87
        """
        date_obj = datetime(date["year"], date["month"], date["day"])
        last_day_of_year = datetime(date["year"], 12, 31)
        return (last_day_of_year - date_obj).days

    @tool("get_days_since_beginning_of_year")
    def get_days_since_beginning_of_year(date: dict):
        """Useful to get the number of days since the beginning of the year for a given date.

        Args:
            date (dict): A dictionary containing the year, month, and day.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 5
                    }

        Returns:
            int: The number of days since the beginning of the year.
                Example: 277
        """
        date_obj = datetime(date["year"], date["month"], date["day"])
        first_day_of_year = datetime(date["year"], 1, 1)
        return (date_obj - first_day_of_year).days

    @tool("get_next_weekday")
    def get_next_weekday(date: dict, weekday: int):
        """Useful to get the next specified weekday for a given date.

        Args:
            date (dict): A dictionary containing the year, month, and day.
                Example:
                    {
                        "year": 2023,
                        "month": 6,
                        "day": 10
                    }
            weekday (int): The weekday to find (0=Monday, 1=Tuesday, ..., 6=Sunday).

        Returns:
            dict: A dictionary containing the year, month, and day of the next specified weekday.
        """
        date_obj = datetime(date["year"], date["month"], date["day"])
        days_ahead = weekday - date_obj.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        next_weekday = date_obj + timedelta(days=days_ahead)
        return {"year": next_weekday.year, "month": next_weekday.month, "day": next_weekday.day}

    @tool("get_previous_weekday")
    def get_previous_weekday(date: dict, weekday: int):
        """Useful to get the previous occurrence of a given weekday before a specific date.

        Args:
            date (dict): A dictionary containing the year, month, and day.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 5
                    }
            weekday (int): The weekday (0 for Monday, 1 for Tuesday, ..., 6 for Sunday).
                Example: 0

        Returns:
            dict: A dictionary containing the year, month, and day of the previous occurrence of the weekday.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 2
                    }
        """
        date_obj = datetime(date["year"], date["month"], date["day"])
        days_ago = date_obj.weekday() - weekday
        if days_ago < 0:  # Target day already happened this week
            days_ago += 7
        previous_weekday_date = date_obj - timedelta(days=days_ago)
        return {"year": previous_weekday_date.year, "month": previous_weekday_date.month, "day": previous_weekday_date.day}

    @tool("get_nth_weekday_of_month")
    def get_nth_weekday_of_month(year: int, month: int, weekday: int, n: int):
        """Useful to get the nth occurrence of a specific weekday in a given month.

        Args:
            year (int): The year.
            month (int): The month.
            weekday (int): The weekday to find (0=Monday, 1=Tuesday, ..., 6=Sunday).
            n (int): The occurrence number of the weekday in the month.

        Returns:
            dict: A dictionary containing the year, month, and day of the nth weekday.
        """
        first_day_of_month = datetime(year, month, 1)
        first_weekday = first_day_of_month.weekday()
        days_until_weekday = (weekday - first_weekday + 7) % 7
        nth_weekday = first_day_of_month + timedelta(days=days_until_weekday + (n - 1) * 7)
        return {"year": nth_weekday.year, "month": nth_weekday.month, "day": nth_weekday.day}

    @tool("get_last_weekday_of_month")
    def get_last_weekday_of_month(year: int, month: int, weekday: int):
        """Useful to get the last occurrence of a specific weekday in a given month.

        Args:
            year (int): The year.
            month (int): The month.
            weekday (int): The weekday to find (0=Monday, 1=Tuesday, ..., 6=Sunday).

        Returns:
            dict: A dictionary containing the year, month, and day of the last weekday.
        """
        last_day_of_month = datetime(year, month + 1, 1) - timedelta(days=1)
        days_behind = (last_day_of_month.weekday() - weekday + 7) % 7
        last_weekday = last_day_of_month - timedelta(days=days_behind)
        return {"year": last_weekday.year, "month": last_weekday.month, "day": last_weekday.day}

    @tool("get_age")
    def get_age(birth_date: dict, current_date: dict):
        """Useful to calculate the age based on the birth date and current date.

        Args:
            birth_date (dict): A dictionary containing the year, month, and day of the birth date.
                Example:
                    {
                        "year": 1990,
                        "month": 5,
                        "day": 15
                    }
            current_date (dict): A dictionary containing the year, month, and day of the current date.
                Example:
                    {
                        "year": 2023,
                        "month": 10,
                        "day": 5
                    }

        Returns:
            int: The age in years.
                Example: 33
        """
        birth_date_obj = datetime(birth_date["year"], birth_date["month"], birth_date["day"])
        current_date_obj = datetime(current_date["year"], current_date["month"], current_date["day"])
        age = current_date_obj.year - birth_date_obj.year
        if (current_date_obj.month, current_date_obj.day) < (birth_date_obj.month, birth_date_obj.day):
            age -= 1
        return age

    @tool("get_date_from_timestamp")
    def get_date_from_timestamp(timestamp: int):
        """Useful to get the date from a Unix timestamp.

        Args:
            timestamp (int): The Unix timestamp.
                Example: 1686412800

        Returns:
            dict: A dictionary containing the year, month, and day of the date.
        """
        date_obj = datetime.fromtimestamp(timestamp)
        return {"year": date_obj.year, "month": date_obj.month, "day": date_obj.day}

    @tool("get_timestamp_from_date")
    def get_timestamp_from_date(date: dict):
        """Useful to convert a date to a Unix timestamp.

        Args:
            date (dict): A dictionary containing the year, month, and day.

        Returns:
            int: The Unix timestamp.
        """
        date_obj = datetime(date["year"], date["month"], date["day"])
        return int(date_obj.timestamp())

    @tool("get_date_from_iso_format")
    def get_date_from_iso_format(iso_date: str):
        """Useful to convert an ISO-formatted date string to a date.

        Args:
            iso_date (str): The ISO-formatted date string (e.g., "2023-06-10").

        Returns:
            dict: A dictionary containing the year, month, and day of the date.
        """
        date_obj = datetime.fromisoformat(iso_date)
        return {"year": date_obj.year, "month": date_obj.month, "day": date_obj.day}

    @tool("get_iso_format_from_date")
    def get_iso_format_from_date(date: dict):
        """Useful to get the ISO format date string from a given date.

        Args:
            date (dict): A dictionary containing the year, month, and day.
                Example:
                    {
                        "year": 2023,
                        "month": 6,
                        "day": 10
                    }

        Returns:
            str: The ISO format date string.
        """
        date_obj = datetime(date["year"], date["month"], date["day"])
        return date_obj.isoformat()

    @tool("get_date_from_ordinal")
    def get_date_from_ordinal(ordinal: int):
        """Useful to get the date from an ordinal number.

        Args:
            ordinal (int): The ordinal number.
                Example: 738532

        Returns:
            dict: A dictionary containing the year, month, and day of the date.
        """
        date_obj = datetime.fromordinal(ordinal)
        return {"year": date_obj.year, "month": date_obj.month, "day": date_obj.day}
    
    @tool("get_day_of_week")
    def get_day_of_week(date: dict):
        """Useful to get the day of the week for a given date.

        Args:
            date (dict): A dictionary containing the year, month, and day.

        Returns:
            str: The day of the week (e.g., Monday, Tuesday, etc.).
        """
        date_obj = datetime(date["year"], date["month"], date["day"])
        day_of_week = date_obj.strftime("%A")
        return day_of_week

    @tool("get_days_between_dates")
    def get_days_between_dates(start_date: dict, end_date: dict):
        """Useful to calculate the number of days between two dates.

        Args:
            start_date (dict): A dictionary containing the year, month, and day of the start date.
            end_date (dict): A dictionary containing the year, month, and day of the end date.

        Returns:
            int: The number of days between the start and end dates.
        """
        start_date_obj = datetime(start_date["year"], start_date["month"], start_date["day"])
        end_date_obj = datetime(end_date["year"], end_date["month"], end_date["day"])
        days_between = (end_date_obj - start_date_obj).days
        return days_between
