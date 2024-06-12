from datetime import datetime, timedelta
import pytest
from common.TimeEntry import TimeEntry

@pytest.mark.parametrize("date_entry, intended_date", [
    ('yesterday', datetime.now() - timedelta(days=1)),
    ('today', datetime.now()),
    ('tomorrow', datetime.now() + timedelta(days=1)),
    ('last week', datetime.now() - timedelta(days=7)),
    ('last fortnight', datetime.now() - timedelta(days=14)),
    ('3 days ago', datetime.now() - timedelta(days=3)),
    ('4 days ago', datetime.now() - timedelta(days=4)),
    ('4daysago', datetime.now() - timedelta(days=4)),
    ('2 weeks ago', datetime.now() - timedelta(days=14)),
    ('3 weeks ago', datetime.now() - timedelta(days=21)),
    ('3 wks ago', datetime.now() - timedelta(days=21)),
    ('3 w ago', datetime.now() - timedelta(days=21)),
    ('3 wago', datetime.now() - timedelta(days=21)),
    ('3wago', datetime.now() - timedelta(days=21)),
    ('3wks ago', datetime.now() - timedelta(days=21)),
    ('12/8/24', datetime.strptime("12/08/24", "%d/%m/%y")),
    ('3/8/2024', datetime.strptime("3/08/24", "%d/%m/%y")),
])
def test_parse_date_entry(date_entry, intended_date):
    """
    The script, when inputting time entries, must parse the following
    strings into start and end dates
    - yesterday
    - today
    - last week
    - last fortnight
    - N days ago
    - N weeks ago
    - DD/M/YY
    - DD/MM/YYYY
    """
    intended_date = intended_date.replace(hour=0, minute=0, second=0, microsecond=0)
    time_entry = TimeEntry(date_entry, "an hour ago")
    parsed_date = time_entry.parse_date_string(date_entry)

    assert parsed_date == intended_date, f"{parsed_date} from {date_entry} doesnt match {intended_date}"

@pytest.mark.parametrize("time_string, intended_time", [
    ("an hour ago", (datetime.now() - timedelta(hours=1)).replace(second=0,microsecond=0)),
    ("noon", datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)),
    ("lunch", datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)),
    ("lunch time", datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)),
    ("midnight", datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),
    ("now", datetime.now().replace(second=0, microsecond=0)),
    ("1hr ago", (datetime.now().replace(second=0, microsecond=0) - timedelta(hours=1))),
    ("1 hr ago", (datetime.now().replace(second=0, microsecond=0) - timedelta(hours=1))),
    ("2hrs ago", (datetime.now().replace(second=0, microsecond=0) - timedelta(hours=2))),
    ("2 hrs ago", (datetime.now().replace(second=0, microsecond=0) - timedelta(hours=2))),
    ("13:45", datetime.now().replace(hour=13, minute=45, second=0, microsecond=0)),
    ("1345", datetime.now().replace(hour=13, minute=45, second=0, microsecond=0)),
    ("01:00 PM", datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)),
    ("01:00PM", datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)),
    ("01:00 AM", datetime.now().replace(hour=1, minute=0, second=0, microsecond=0)),
    ("01:00AM", datetime.now().replace(hour=1, minute=0, second=0, microsecond=0)),
    ("1 pM", datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)),
    ("1 pm", datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)),
    ("1 Am", datetime.now().replace(hour=1, minute=0, second=0, microsecond=0)),
    ("1 am", datetime.now().replace(hour=1, minute=0, second=0, microsecond=0)),
    ("10 am", datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)),
    ("10 pm", datetime.now().replace(hour=22, minute=0, second=0, microsecond=0)),
    ])
def test_parse_time_string_to_seconds_into_day(time_string, intended_time):
    """
    The script, when inputting time entries, must parse the following
    tarm strings into the start and end times

    - an hour ago
    - noon
    - lunch
    - lunch time
    - midnight
    - now

    - 1hr ago
    - 1 hr ago
    - 2hrs ago
    - 2 hrs ago

    - HH:MM
    - HHMM

    - HH:MM AM
    - HH:MMAM

    - HH:MM PM
    - HH:MMPM

    - HH PM
    """
    now = datetime.now().replace(hour=0,minute=0, second=0, microsecond=0)
    time_entry = TimeEntry("1/1/2024", "an hour ago")
    parsed_time = time_entry.parse_time_string(time_string)

    assert parsed_time == intended_time - now, f"{time_string} parsed as {parsed_time} is not equal to {intended_time - now}"

@pytest.mark.parametrize("duration_string, intended_seconds", [
    ("a second", 1),
    ("10 seconds", 10),
    ("10 sec", 10),
    ("10 s", 10),
    ("a minute", 60),
    ("5 minutes", 300),
    ("5 min", 300),
    ("5 m", 300),
    ("an hour", 3600),
    ("anhour", 3600),
    ("3 hours", 10800),
    ("3 hr", 10800),
    ("3 h", 10800),
    ("3h", 10800),
    ("a day", 86400),
    ("2 days", 172800),
    ("2 d", 172800),
    ("2 day", 172800),
    ("1.5 hours", 5400),
    ("1.5 hr", 5400),
    ("1.5 h", 5400),
    ("0.5 minutes", 30),
    ("1 day 2 hours 3 minutes 4 seconds", 93784),
    ("1d 2h 3m 4s", 93784),
    ("1.25 days", 108000),
    ("0.75 hours", 2700),
    ("1 day and 2 hours", 93600),
    ("a day and an hour", 90000),
    ("a day and an hour and 34.5mins + 33s", 90000 + 2103),
    ("1day+1hr+34.5m+33s", 90000 + 2103),
    ])
def test_parse_duration_to_seconds(duration_string, intended_seconds):
    """
    The script, when inputting a duration string, must convert the
    duriation into seconds and return it. Durations may be integers OR
    float values.

    seconds handlers
    - a(n) second
    - N s(ec)(ond)(s) or Ns(ec)(ond)(s)

    minutes handlers
    - a min(ute)
    - N min(ute)(s) or Nmin(ute)(s)

    hours handlers
    - a(n) hour(s)
    - N h(ou)r(s) Nh(our)r(s)

    days handler
    - a(n) day(s)
    - N d(ay)(s) or Nd(ay)(s)

    """
    time_entry = TimeEntry("yesterday", "lunch")
    parsed_seconds = time_entry.parse_duration_string(duration_string)
    assert parsed_seconds == intended_seconds, f"Expected {intended_seconds}, but got {parsed_seconds}"

@pytest.mark.parametrize("start_date, start_time, end_date, end_time, intended_duration_sec", [
    ("yesterday","lunch", "today", "lunch", 2*43200),
    ("yesterday","lunch", "today", "midnight", 43200),
    ])

def test_calculate_duration_to_seconds(start_date, start_time, end_date, end_time, intended_duration_sec):
    time_entry = TimeEntry(start_date, start_time)
    time_entry.set_end_ts(end_date, end_time)
    duration_sec = time_entry.duration_sec
    assert duration_sec == intended_duration_sec, f"{duration_sec}s does not equal intended {intended_duration_sec}s"

@pytest.mark.parametrize("start_date, start_time, duration_override,intended_end_ts", [
    ("12/12/2024","lunch", "3hrs", datetime.strptime("12-12-2024_15:00", "%d-%m-%Y_%H:%M")),
    ("13/01/2024","13:00", "an hour and 30 minutes", datetime.strptime("13-01-2024_14:30", "%d-%m-%Y_%H:%M")),
    ("13/01/2024","1pm", "an hour and 30 minutes", datetime.strptime("13-01-2024_14:30", "%d-%m-%Y_%H:%M")),
    ])
def test_end_ts_with_duration(start_date, start_time, duration_override, intended_end_ts):
    time_entry = TimeEntry(start_date, start_time)
    time_entry.set_duration(duration_override)
    assert time_entry.end_ts == intended_end_ts, f"{time_entry.end_ts} is not equal to intended {intended_end_ts} after {duration_override} was applied"

@pytest.mark.parametrize("method", ["note", "client", "category"])
@pytest.mark.parametrize("text_to_write", ["this is a note", '\this is a Note', "\rdigism\n\r\t"])
def test_details_set_entry(method, text_to_write):
    """
    The module must strip the text then write it to the text_to_write.
    """
    time_entry = TimeEntry("today", "lunch")
    getattr(time_entry, f"set_{method}")(text_to_write)
    property_value = getattr(time_entry, method)
    assert property_value == text_to_write.strip(), f"{property_value} not equal to the intended {text_to_write}"

@pytest.mark.parametrize("method", ["note", "client", "category"])
@pytest.mark.parametrize("text_to_write", ["this is a note", '\this is a Note', "\rdigism\n\r\t"])
def test_details_init_entry(method, text_to_write):
    """
    The module, when initializing text details, must strip and save the text into the property...
    """
    time_entry = TimeEntry("today", "lunch", **{method: text_to_write})
    property_value = getattr(time_entry, method)
    assert property_value == text_to_write.strip(), f"{property_value} not equal to the intended {text_to_write}"

def test_duration_override():
    """
    When overrideing the duration when a time is set, the new duration
    must be the duratino override. The end_ts must be updated
    accordingly
    """
    time_entry = TimeEntry("yesterday","lunch")
    time_entry.set_end_ts("today", "lunch")
    time_entry.set_duration("1hrs")
    assert time_entry.duration_sec == 3600, "The duration was not overridden..."

def test_end_ts_override():
    """
    When setting the end_ts, the duration properpty must output the
    updated end_ts duration NOT the old duration value...
    """
    time_entry = TimeEntry("yesterday", "lunch")
    time_entry.set_duration("1hr")
    time_entry.set_end_ts("today", "midnight")

    duration_hrs = time_entry.duration_sec / 3600

    if (duration_hrs != 12):

        # Check this fails for this implementation...
        if (time_entry.duration_sec_override):
            pytest.fail("time_entry.end_ts didnt reset the time_entry.duration_sec_override property...")

        pytest.fail(f"duration of {duration_hrs} isnt 12hrs")

    pass
