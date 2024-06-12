import time
import subprocess
import pytest
import sqlite3

from common.TimeEntry import TimeEntry
from common.TimeSheet import TimeSheet
from common.DBHolder import DB

@pytest.fixture(scope="session")
def db():
    db_obj = DB("timmy-time.sqlite")
    yield db_obj
    # db_obj.delete()

def test_create_db(db):
    """
    the database object must be created when the object is created and no file is present
    """
    timesheet = TimeSheet(db.path)
    if not db.exists:
        pytest.fail(f"Module failed to create {db_path}")

@pytest.mark.parametrize('table_name', ["time_entry"])
def test_check_db_tables(db, table_name):
    """
    The database must check which tables are present.
    """
    timesheet = TimeSheet(db.path)

    cmd = """
    SELECT name FROM sqlite_master WHERE type='table' AND name=?;
    """
    db.cursor.execute(cmd, (table_name, ))
    result = db.cursor.fetchone()
    if not result:
        pytest.fail(f"Table {table_name} wasnt created...")

@pytest.mark.parametrize("table_name", ["time_entry"])
@pytest.mark.parametrize("table_field, field_value", [
    ("description", "abc"),
    ("category","abc"),
    ("client", "test")
])
@pytest.mark.parametrize("start_date, start_time, end_date, end_time", [
    ("today","lunch", "tomorrow","lunch")
])
def test_create_db_entry(db, table_name, start_date, start_time, end_date, end_time, table_field, field_value):

    timesheet = TimeSheet(db.path)

    time_entry = TimeEntry(start_date, start_time, end_date, end_time)
    if (table_field == "description"):
        getattr(time_entry, f"set_note")(field_value)
    else:
        getattr(time_entry, f"set_{table_field}")(field_value)

    timesheet.insert_time_entry(time_entry)

    result = db.find(table_name, table_field, field_value)
    assert len(result) == 1, "Failed to create an entry"


@pytest.mark.parametrize("start_date, start_time, end_date, end_time", [
    ("today", "lunch", "tomorrow", "lunch")
])
def test_get_db_entries(db, start_date, start_time, end_date, end_time):

    db.delete()

    timesheet = TimeSheet(db.path)

    for i in range(1,4):
        time_entry = TimeEntry(start_date, start_time)
        time_entry.set_note(f"line {i}")
        time_entry.set_duration(f"{i} hrs")

        timesheet.insert_time_entry(time_entry)

    entries = timesheet.get_time_entries()

    assert len(entries) == 3, f"more than 3 entreis are present - {len(entries)}"
