import json
import argparse
import os

class Entry:

    def __init__(self, tags, description, commands):
        self.tags = tags
        self.description = description
        self.commands = commands

    def __dict__(self):
        return {
            'tags': [i.strip().lower() for i in self.tags],
            'description': self.description.strip(),
            'commands': self.commands
        }

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--json', help='JSON file to add entry to', default='dataset.json')

    args = parser.parse_args()

    if not os.path.exists(args.json):
        print(f"[-] File {args.json} does not exist.")
        exit(1)

    try:
        b_size = os.stat(args.json).st_size
        with open(args.json, 'r') as f:
            dataset = json.load(f)

        if b_size/1024 > 1000:
            size = f"{b_size/(1024*1024)} Megabytes"
        else:
            size = f"{b_size/(1024)} Kilobytes"

        print(f"[*] Dataset file: {args.json}")
        print(f'[*] Dataset size: {size} ({b_size} Bytes)')
        print(f'[*] Current dataset length: {len(dataset)}')
        
        print(f"\n[+] Adding entry no. {len(dataset) + 1}")

        tags = input('Tags (space seperated): ').lower().strip().split()
        description = input('Description: ').strip()
        commands = [i.strip() for i in input('Commands (comma [,] seperated): ').split(',')]
        comments = [i.strip() for i in input('Comments for each command (comma [,] seperated): ').split(',')]

        # Combining commands and comments into a dictionary: k:commands v:comments
        commands = dict(zip(commands, comments))

        entry = Entry(tags, description, commands)
        dataset.append(entry.__dict__())

        with open(args.json, 'w') as f:
            json.dump(dataset, f, indent=4)

        print("[+] Updated the dataset.")
    except KeyboardInterrupt:
        print("\n[-] Keyboard Interrupt.")
        exit(1)
    except Exception as e:
        print(f"[-] Error: {e.__str__()}")
        exit(1)
