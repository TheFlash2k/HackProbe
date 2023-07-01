import json
from scripts.utils import *
import argparse
import os
import tempfile
from deepdiff import DeepDiff

def find_local_diff(json1, json2):
    differences = DeepDiff(json1, json2)
    local = differences.get("iterable_item_removed", {})
    updated = []

    for key in local.keys():
        updated.append(local[key])

    return updated

def add_to_db(data : list):
    msg("Adding new entries to the database...", '*', end='')
    try:
        client = MongoClient(Config.conn_string)
        db = client[Config.db_name]
        collection = db[Config.collection_name]
        collection.insert_many(data)
        client.close()
        print(f" {Colors.GREEN}Done!{Colors.RESET}")
    except Exception as e:
        msg(f"An error occurred! {e.__str__()}", '!')
        return None
    return True


def sync(json_file):
    
    with open(json_file, 'r') as f:
        local_data = json.load(f)

    # create a temporary file
    tmp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    msg(f"Created a temporary file named {Colors.MAGENTA}{tmp.name}{Colors.RESET} to store the dump from the DB.", '*')

    msg("Fetching data from the database:", '*', end='')
    try:
        client = MongoClient(Config.conn_string)
        db = client[Config.db_name]
        collection = db[Config.collection_name]
        results = collection.find()
        _data = []
        for doc in results:
            doc.pop('_id')
            _data.append(doc)
        client.close()
        tmp.write(json.dumps(_data, indent=4, sort_keys=True))
        tmp.write('\n')
        print(f" {Colors.GREEN}Done!{Colors.RESET}")
    except Exception as e:
        msg(f"An error occurred! {e.__str__()}", '!')
        return None
    
    tmp.close()

    msg("Checking if the local cache has new entries...", '*', end='')
    with open(tmp.name, 'r') as f:
        db_data = json.load(f)
    new_entries = find_local_diff(local_data, db_data)
    print(f" {Colors.GREEN}Done!{Colors.RESET}")

    if new_entries == {}:
        msg("Local cache and the server are up to date.", '+')
        return True
    
    msg(f"{Colors.BLUE}{len(new_entries)}{Colors.RESET} new entries found in the local cache.", '+')

    msg("Removing the temporary file...", '*', end='')
    os.unlink(tmp.name)
    print(f" {Colors.GREEN}Done!{Colors.RESET}")

    if not new_entries:
        msg("No new entries found in the local cache.", '+')
        return True
    
    if not add_to_db(new_entries):
        return None
    
    msg("Fetching new file from the remote DB and re-verifying and updating the local-cache in-case", '*', end='')
    try:
        client = MongoClient(Config.conn_string)
        db = client[Config.db_name]
        collection = db[Config.collection_name]
        results = collection.find()
        _data = []
        for doc in results:
            doc.pop('_id')
            _data.append(doc)
        client.close()
        with open(json_file, 'w') as f:
            f.write(json.dumps(_data, indent=4, sort_keys=True))
        print(f" {Colors.GREEN}Done!{Colors.RESET}")
    except Exception as e:
        msg(f"An error occurred! {e.__str__()}", '!')
        return None

    return True

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Synchronize the local JSON file with remote MongoDB.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f', '--file', help='Cheat Sheet Database JSON File', default='cheat-sheet.json')
    args = parser.parse_args()

    json_file = os.path.abspath(args.json)
    msg(f"Loading {Colors.BLUE}{json_file}{Colors.RESET}\r", '*')
    # Because relative importing's a bitch..
    with open(f"../{args.json}", 'r') as f:
        data = json.load(f)

    msg(f"Loaded  {Colors.BLUE}{json_file}{Colors.RESET} {Colors.GREEN}successfully{Colors.RESET}!", '+')

    msg(f"Checking the database connection...")

    if not check_config():
        exit(1)

    if not sync(f"../{args.json}"):
        msg("Unable to sync database and the local cache...")
        exit(1)
    