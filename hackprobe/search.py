import requests
import json
import argparse
from urllib.parse import quote

from scripts.utils import *

verbose = False

def search(host, port, query):
    try:
        if verbose:
            msg(f"Trying to connect to http://{host}:{port}", '*')
        res = requests.get(f"http://{host}:{port}/search?match={query}")
        print(res.text)
        if res.status_code == 200:
            return res.json()['results']
        else:
            msg(f"An error occurred! {res.json()['message']}", '!')
            return None
    except Exception as e:
        msg(f"An error occurred! {e.__str__()}", '!')
        return None

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Search for the commands in the database.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tags', help='The tags you want to search for', nargs='+')
    parser.add_argument('-H', '--host', help='Host to run the server on', default='localhost')
    parser.add_argument('-p', '--port', help='Port to run the server on', default=5000)
    parser.add_argument('-v', '--verbose', help='Enable verbose mode', action='store_true')
    parser.add_argument('-c', '--cmd', help='Show only the commands', action='store_true')
    args = parser.parse_args()

    verbose = args.verbose

    if verbose:
        msg(f"Searching for {Colors.BLUE}{args.tags}{Colors.RESET}...", '*')

    tags = quote(' '.join(args.tags))
    res = search(args.host, args.port, tags)

    if res == [] or res == None:
        msg(f"No commands were found {Colors.RED}:({Colors.RESET}", '!')
        exit()

    if not args.cmd:
        msg(f"Found:", '*')
        print(json.dumps(res, indent=4, sort_keys=True))
    else:
        msg(f"Followings commands were found", '+')
        _it = 0
        for i in range(len(res)):
            cmds = res[i]['commands']
            for cmd in cmds:
                print(f"{Colors.MAGENTA}{_it+1}. {Colors.RESET}{cmd['cmd']}")
                _it += 1
