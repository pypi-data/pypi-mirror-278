from pydt3 import DEVONthink3

dt3 = DEVONthink3()


def test_databases():
    print("Databases:")
    for db in dt3.databases:
        print(db.name)


# pytest "/Users/yutianran/Documents/MyPKM/test_denvonthink.py::test_inbox"
def test_selected_records():
    # get selected records
    records = dt3.selected_records
    # get the first selected record and print its information
    if records:
        first = records[0]
        print(first.name)
        print(first.type)
        print(first.reference_url)
        print(first.plain_text)
    selected_record = records[0]
    print(selected_record.name)


def test_inbox():
    inbox = dt3.inbox
    print(inbox.name)
    # create a new folder in inbox
    dt3.create_location("new-group-from-pydt3", inbox)
    # create record in inbox
    record = dt3.create_record_with(
        {
            "name": "hello-from-pydt3",
            "type": "markdown",
            "plain text": "# Hello from pydt3",
        },
        inbox,
    )
    print(record)


def test():
    print(__file__)
    test_databases()
    test_selected_records()
    test_inbox()

    print("Done")


if __name__ == "__main__":
    test()
