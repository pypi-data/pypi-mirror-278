import os
import sqlite3
import subprocess
from datetime import datetime
from common.TimeEntry import TimeEntry

class TimeSheet:
    def __init__(self, sq3_path = None):
        self.sq3_path = sq3_path if sq3_path else self.find_db_path()
        self.sq3_conn = sqlite3.connect(self.sq3_path)
        self.sq3_cursor = self.sq3_conn.cursor()

        self._create_tables_if_not_exist()

    def insert_time_entry(self, time_entry):
        """
        Insert a time entry object and add it to the database

        Parameters:
            - time_entry (TimeEntry): The time entry object
        """

        cmd = """
        INSERT INTO time_entry (start_ts, duration_sec, end_ts, description, category, client)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        self.sq3_cursor.execute(cmd, (
            time_entry.start_ts,
            time_entry.duration_sec,
            time_entry.end_ts,
            time_entry.note,
            time_entry.category,
            time_entry.client
            ))

        self.sq3_conn.commit()

    def find_db_path(self):
        """
        Find a database starting with `timmy-time_XXXXXX.sqlite` in the local directory
        If the database doesn't exist, it returns a database path to make

        Returns:
            sq3_path (string): The path to the sq3lite database path
        """
        cwd = self._get_cwd()
        db_name = self._find_db_in_dir(cwd)

        if not cwd:
            raise Exception("Failed to find cwd")

        if db_name:
            return f"{cwd}/{db_name}"
        else:
            return f"{cwd}/timmy-time.sqlite"

    @staticmethod
    def _find_db_in_dir(directory_path):
        """
        Looks in a directory for timmy-time_XXXXX.sqlite.

        Parameters:
            directory_path (string): The path of the directory to search in

        Returns:
            db_name (string): if db is present, it returns the db name. else it returns none
        """
        files = os.listdir(directory_path)

        if len(files) < 1:
            return None

        files_filtered = [*filter(lambda fn: "timmy-time" in fn, files)]
        if len(files_filtered) < 1:
            return None

        return files_filtered[0].strip()

    @staticmethod
    def _get_cwd():
        """
        Gets the current workign directory

        Returns:
            cwd_path (string): THe current working directory
        """
        res = subprocess.run("pwd", shell=True, capture_output=True, check=True)
        res.check_returncode()

        cwd = res.stdout.decode()

        return cwd.strip()

    def get_time_entries(self):
        """
        Get the time entries from the database

        NOTE: Unimplemented...
        Parameters:
            date_limit (string): the earliest date up until the current date
            row_limit (int): maximum number of rows from the latest row entry

        Returns:
            entry_collection ([time_entry]): a list of entires
                - start_ts, duration_sec, end_ts, description, category, client

        """
        cmd = "SELECT start_ts, duration_sec, end_ts, description, category, client FROM time_entry"
        cmd += " ORDER BY start_ts ASC"

        self.sq3_cursor.execute(cmd)
        results = self.sq3_cursor.fetchall()

        return results

    def _create_tables_if_not_exist(self):
        """
        creates the following tables
        - time_entry: start_ts (datetime), duration_sec(int), end_ts(datetime), description(string), category(string), client(string)
        """
        cmd = """
        CREATE TABLE IF NOT EXISTS time_entry (
            start_ts DATETIME,
            duration_sec INTEGER,
            end_ts DATETIME,
            description TEXT,
            category TEXT,
            client TEXT
        );
        """
        self.sq3_cursor.execute(cmd)
