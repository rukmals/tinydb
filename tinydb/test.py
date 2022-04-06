import json


def print_db():
    with open("/home/nuwanga/projects/tinydb/database/db_transactions.json", 'r+') as file:
        file_data = json.load(file)
        for d in file_data["_default"]:
            print(d['transaction_id'])
            print(d)

print_db()