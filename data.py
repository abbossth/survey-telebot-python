import openpyxl

wb = openpyxl.load_workbook("survey_db.xlsx")

records = wb["records"]


def print_doc():
    for row in records.values:
        for value in row:
            print(value)


def add_record(data):
    records.append(data)
    print("Record appended successfully!")

