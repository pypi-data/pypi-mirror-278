import rich.box as box
from rich.console import Console
from rich.padding import Padding
from rich.table import Table

RUN_STATUS = "Status"
RUN_DATE = "Creation Date"
RUN_ID = "Id"
RUN_AUTHOR = "Author"
RUN_MESSAGE = "Message"


def display_line(console, name, value):
    console.print(name, f"[bold]{value}[/bold]", sep=":")


def display_run_detailed(run):
    console = Console(highlight=False)

    display_line(console, RUN_ID, run.get("run_id"))
    display_line(console, RUN_AUTHOR, run.get("author"))
    display_line(console, RUN_DATE, run.get("generation_date"))
    display_run_short(run)


def display_run_short(run):
    status = run.get("status")
    color = get_status_color(status)
    console = Console(highlight=False)

    display_line(console, RUN_STATUS, f"[{color}]{status}[/{color}]")
    if status == "error":
        display_line(console, RUN_MESSAGE, run.get("message"))
    display_table_parameter(console, "Input", run.get("inputs"))

    display_table_parameter(console, "Output", run.get("outputs"))


def get_status_color(status):
    color = "white"
    match status:
        case "success":
            color = "green"
        case "error":
            color = "red"
        case "running":
            color = "blue"
        case "cancelled":
            color = "magenta"
    return color


def display_table_parameter(console, prefix, datas):
    console.print(f"{prefix}s:")

    table = Table(show_edge=False, box=box.ASCII)
    table.add_column(prefix + " name")
    table.add_column("Type")
    table.add_column("Value/Basename")
    if datas is not None:
        for data in datas:
            value = ""
            if "value" in data.keys() and data.get("value") is not None:
                value = data.get("value")
            elif (
                "basename" in data.keys() and data.get("basename") is not None
            ):
                value = data.get("basename")
            elif "url" in data.keys():
                value = data.get("url")
            table.add_row(data.get("name"), data.get("param_type"), str(value))
    console.print(Padding(table, (0, 4)))
