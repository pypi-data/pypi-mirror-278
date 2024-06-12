#! ./venv/bin/python3
import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table

from datetime import datetime, timedelta

from common.TimeEntry import TimeEntry
from common.TimeSheet import TimeSheet

app = typer.Typer()
console = Console()

@app.command()
def enter(
        start_date_string: Annotated[str, typer.Option("--start-date", "-sd", prompt=True)],
        start_time_string: Annotated[str, typer.Option("--start-time", "-st", prompt=True)],
        description: Annotated[str, typer.Option("--desc", "-d", prompt=True)],
        client: Annotated[str, typer.Option("--client","-cl", prompt=True)],
        category: Annotated[str, typer.Option("--category","-cat", prompt=True)],
        ):

    time_entry = TimeEntry(start_date_string, start_time_string)
    time_entry.set_note(description)
    time_entry.set_client(client)
    time_entry.set_category(category)

    task_end_type = typer.prompt("Use Duration (TYPE: 'd') or End Datetime (TYPE 't')")
    if task_end_type == "d":
        duration_string = typer.prompt("Duration of Work")
        time_entry.set_duration(duration_string)
    elif task_end_type == "t":
        end_date = typer.prompt("End Date")
        end_time = typer.prompt("End Time")
        time_entry.set_end_ts(end_date, end_time)

    start_date = time_entry.start_ts.strftime("%d-%m-%y")
    start_time = time_entry.start_ts.strftime("%H:%M")

    duration_hrs = str(round(time_entry.duration_sec / 3600, 5))

    end_date = time_entry.end_ts.strftime("%d-%m-%y")
    end_time = time_entry.end_ts.strftime("%H:%M")

    timesheet = TimeSheet()
    timesheet.insert_time_entry(time_entry)

@app.command()
def show():

    timesheet = TimeSheet()

    table = Table("start ts", "duration (hrs)", "end ts", "description", "client")
    for row in timesheet.get_time_entries():
        start_ts, duration_sec, end_ts, description, category, client = row
        duration_hrs = round(duration_sec/3600, 5)
        # 2024-05-28 12:00:00

        start_ts = datetime.strptime(start_ts, '%Y-%m-%d %H:%M:%S').strftime("%d/%m/%Y %H:%M")
        end_ts = datetime.strptime(end_ts, '%Y-%m-%d %H:%M:%S').strftime("%d/%m/%Y %H:%M")

        table.add_row(start_ts, str(duration_hrs), end_ts, description, client)
    console.print(table)


if __name__ == "__main__":
    app()
