import subprocess
import sqlite3

class DB:
    def __init__(self, db_path):
        self.path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    @property
    def exists(self):
        res = subprocess.run(f"[ -f {self.path} ]", shell=True)

        if res.returncode == 0:
            return True
        elif res.returncode == 1:
            return False
        else:
            raise Exception(f"failed to check if {self.path} exists...")

    def find(self, table_name, key, value):
        """
        finds the row in the table w.r.t to the table, the key and a search value within the key

        Parameters:
            table_name (string): The table name within the db
            key (string): The key to search within the db
            value (arbitrary): A search value for the key

        Returns:
            result (row data): The table entry

        """
        cmd = f"SELECT * FROM {table_name} WHERE {key} = ?;"
        self.cursor.execute(cmd, (value,))
        result = self.cursor.fetchall()
        return result

    def delete(self):

        if not self.exists:
            return

        res = subprocess.run(f"rm {self.path}", shell=True)
        if res.returncode != 0:
            raise Exception(f"Failed to delete {self.path}")
