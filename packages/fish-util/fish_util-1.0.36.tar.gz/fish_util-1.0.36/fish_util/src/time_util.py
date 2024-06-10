import arrow
import pathlib


def get_current_time():
    return arrow.now().format("YYYY-MM-DD HH:mm:ss")


def get_current_time_str():
    return arrow.now().format("YYYYMMDD_HHmmss")


def get_time_dir(parent_dir):
    current_time = arrow.now().format("YYMMDD_HHmmss")
    note_dir = pathlib.Path(f"{parent_dir}/{current_time}")
    note_dir.mkdir(parents=True, exist_ok=True)
    print(f"Note directory: {note_dir}")
    return note_dir


current_date = arrow.now().format("YYMMDD")
current_time = arrow.now().format("HHmmss")

test_time = arrow.now()
test_str = test_time.strftime("%Y/%m/%Y-%m-%d.md")
print(test_str)
