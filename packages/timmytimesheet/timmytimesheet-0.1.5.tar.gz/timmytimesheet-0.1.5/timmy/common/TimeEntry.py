import re
from datetime import datetime, timedelta
from dateutil import parser

class TimeEntry:
    def __init__(self, start_date_string, start_time_string, end_date_string = None, end_time_string=None, note=None, category=None, client=None):

        # START PARAMETERS
        start_date = self.parse_date_string(start_date_string)
        start_seconds_into_day = self.parse_time_string(start_time_string)
        self.start_ts = start_date + start_seconds_into_day

        # ENDING PARAMETERS
        if end_date_string and not end_time_string:
            raise ValueError(f"end date {end_date_string} was received but not end_time_string")

        if not end_date_string and end_time_string:
            raise ValueError(f"end time {end_time_string} was received but not end_date_string")

        if end_date_string and end_time_string:
            self.end_ts = self.parse_date_string(end_date_string) + self.parse_time_string(end_time_string)
        else:
            self.end_ts = None

        # Entry Description
        self.note = note.strip() if note else None
        self.category = category.strip() if category else None
        self.client = client.strip() if client else None

        # OUTPUT PARAMETERS
        self.duration_sec_override = None
        self.is_submitted = False

    def __str__(self):
        display_string = []
        display_string.append(f"START: {self.start_ts}")
        if self.end_ts:
            display_string.append(f"END: {self.end_ts}")
            duration_sec = self.duration_sec
            duration_hrs = round(self.duration_sec/3600,5)
            display_string.append(f"DURATION: {duration_hrs} hr(s)")
        if self.note:
            display_string.append(f"NOTE: {self.note}")

        return "\r\n".join(display_string)

    @property
    def csv_row_entry(self):
        return [self.start_ts, self.duration_sec/3600, self.end_ts, self.notes, self.category]

    def set_end_ts(self, end_date_string, end_time_string):
        """set the start date and time.

        Parameters:
            end_date_string (string): The end date
            end_time_string (string): The end time
        """
        try:
            end_date = self.parse_date_string(end_date_string)
            end_seconds_into_day = self.parse_time_string(end_time_string)
            self.end_ts = end_date + end_seconds_into_day
            self.duration_sec_override = None
        except ValueError as err:
            self.end_ts = None
            raise ValueError(err)

    def set_duration(self, duration_string):

        if not self.start_ts:
            raise ValueError("self.start_ts is missing...")

        self.duration_sec_override = self.parse_duration_string(duration_string)
        self.end_ts = self.start_ts + timedelta(seconds=self.duration_sec_override)

    def set_note(self, note_string):
        self.note = note_string.strip()

    def set_category(self, category_string):
        self.category = category_string.strip()

    def set_client(self, client_string):
        self.client = client_string.strip()

    @property
    def duration_sec(self):
        if self.duration_sec_override:
            return self.duration_sec_override
        delta_sec = self.end_ts - self.start_ts
        return delta_sec.total_seconds()

    @staticmethod
    def parse_date_string(date_string):
        today = datetime.now().replace(hour=0, minute=0, second=0,
                                       microsecond=0)

        if date_string == "today":
            return today
        if date_string == "yesterday":
            return today - timedelta(days=1)
        if date_string == "tomorrow":
            return today + timedelta(days=1)
        if date_string == "last week":
            return today - timedelta(days = 7)
        if date_string == "last fortnight":
            return today - timedelta(days = 14)


        days_ago_match = re.match(r'(\d+)\s*d(ay)?(s)?\s?+ago', date_string)
        if days_ago_match:
            n_days = int(days_ago_match.group(1))
            return today - timedelta(days=n_days)

        weeks_ago_match = re.match(r'(\d+)\s*w(ee)?(k)?(s)?\s?+ago', date_string)
        if weeks_ago_match:
            n_weeks = int(weeks_ago_match.group(1))
            return today - timedelta(weeks=n_weeks)

        try:
            parsed_date = parser.parse(date_string, dayfirst=True)
            return parsed_date.replace(hour=0, minute=0, second=0, microsecond=0)
        except ValueError:
            raise ValueError(f"Date format not recognised: {date_string}")

    @staticmethod
    def parse_time_string(time_string):
        """parses time string into seconds into the day
        parses time string into a seconds into the day from 00:00AM on
        the start of the date.

        Parameters:
            time_string (string): The time string (e.g. 1100; 11:00;
            11:00AM; 11:00 AM; noon; lunch)

        Returns:
            seconds_into_day (float): Number of seconds into the day

        """
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if time_string in "now":
            delta = datetime.now().replace(second=0, microsecond=0) - today
            return delta

        if time_string in ["noon", "lunch", "lunch time"]:
            delta = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0) - today
            return delta

        if time_string == "midnight":
            delta = datetime.now().replace(hour=00, minute=0, second=0, microsecond=0) - today
            return delta

        if time_string == "an hour ago":
            delta = datetime.now() - timedelta(hours=1)
            return delta.replace(second=0, microsecond=0) - today

        hours_ago_match = re.match(r'(\d+)\s*hr[s]?\s*ago', time_string, re.IGNORECASE)
        if (hours_ago_match):
            n_hrs = int(hours_ago_match.group(1))
            delta = datetime.now() - timedelta(hours=n_hrs)
            return delta.replace(second=0, microsecond=0) - today

        # Match "HH:MM AM/PM" or "HH:MMAM/PM" pattern
        am_pm_match = re.match(r'(\d{1,2}):(\d{2})\s*([APMapm]{2})', time_string)
        if am_pm_match:
            hour = int(am_pm_match.group(1))
            minute = int(am_pm_match.group(2))
            period = am_pm_match.group(3).upper()
            if period == 'PM' and hour != 12:
                hour += 12
            elif period == 'AM' and hour == 12:
                hour = 0
            delta = today.replace(hour=hour, minute=minute)
            return delta - today

        # Match "HHMM" pattern
        hhmm_match = re.match(r'(\d{2})(\d{2})', time_string)
        if hhmm_match:
            hour = int(hhmm_match.group(1))
            minute = int(hhmm_match.group(2))
            delta = today.replace(hour=hour, minute=minute)
            return delta - today

        # Match "HH:MM" pattern
        hh_mm_match = re.match(r'(\d{1,2}):(\d{2})', time_string)
        if hh_mm_match:
            hour = int(hh_mm_match.group(1))
            minute = int(hh_mm_match.group(2))
            delta = today.replace(hour=hour, minute=minute)
            return delta - today

        # Match "XXPM" pattern
        hourly_match = re.match(r'(\d{1,2})\s*([APMapm]{2})', time_string)
        if hourly_match:
            hour = int(hourly_match.group(1))
            period = hourly_match.group(2).upper()
            if period == 'PM' and hour != 12:
                hour += 12
            elif period == 'AM' and hour == 12:
                hour = 0
            delta = today.replace(hour=hour)
            return delta - today


        raise ValueError("Failed to parse the time...")

    @staticmethod
    def parse_duration_string(duration_string):
        total_seconds = 0.0

        # Match and convert days
        days_match = re.findall(r'(\d*\.?\d+)\s*d(ay)?(s)?', duration_string, re.IGNORECASE)
        for match in days_match:
            days = float(match[0])
            total_seconds += days * 86400  # 86400 seconds in a day

        # Match and convert hours
        hours_match = re.findall(r'(\d*\.?\d+)\s*h(ou)?(r)?(s)?', duration_string, re.IGNORECASE)
        for match in hours_match:
            hours = float(match[0])
            total_seconds += hours * 3600  # 3600 seconds in an hour

        # Match and convert minutes
        minutes_match = re.findall(r'(\d*\.?\d+)\s*m(in)?(ute)?(s)?', duration_string, re.IGNORECASE)
        for match in minutes_match:
            minutes = float(match[0])
            total_seconds += minutes * 60  # 60 seconds in a minute

        # Match and convert seconds
        seconds_match = re.findall(r'(\d*\.?\d+)\s*s(ec)?(ond)?(s)?', duration_string, re.IGNORECASE)
        for match in seconds_match:
            seconds = float(match[0])
            total_seconds += seconds  # seconds

        # Match and convert "a second"
        if re.search(r'\ba\s*second\b', duration_string, re.IGNORECASE):
            total_seconds += 1

        # Match and convert "a minute"
        if re.search(r'\ba\s*minute\b', duration_string, re.IGNORECASE):
            total_seconds += 60

        # Match and convert "an hour"
        if re.search(r'\ban\s*hour\b', duration_string, re.IGNORECASE):
            total_seconds += 3600

        # Match and convert "a day"
        if re.search(r'\ba\s*day\b', duration_string, re.IGNORECASE):
            total_seconds += 86400

        if total_seconds == 0:
            raise ValueError(f"Failed to set duration with {duration_string} string")

        return total_seconds
