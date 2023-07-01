# HackProbe - A Search Engine for JSON-based Cheat Sheets

---

## What is HackProbe?

HackProbe is a Flask-based API that uses MongoDB to perform fuzzy searching on the JSON cheat sheet that you create.

> Note: I will provide you with a pretty big JSON file that you can use to test the API. You can also use it to create your own cheat sheet.

Currently, HackProbe does not have any frontend, therefore we must rely on `search.py` to search for the commands that we need.

### Prerequisites

- Python3
- Pip3

### Installation

```bash
pip3 install -r requirements.txt
```

### Usage

Before using, please make sure to set the variables inside the [config.ini](config.ini) file correctly.

#### API Server

To start the API server:

```bash
python3 app.py
```

The server accepts the following arguments:

```bash
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file to load (default: config.ini)    
  -H HOST, --host HOST  Host to run the server on (default: 0.0.0.0) 
  -p PORT, --port PORT  Port to run the server on (default: 5000)    
```

#### Search

To search for a command:

```bash
python3 search.py <command>
```

In case the API is not running locally, or is running on a different port:

```bash
python3 search.py <command> --host <host> --port <port>
```

You can also use `-c` or `--cmd` flag with the `search.py` to display only the commands that match the search query.

```bash
python3 search.py linux scp -c -H 127.0.0.1 -p 5000
```

Gives the following output:

```bash
[+] Followings commands were found
1. scp local-file user@ip:/remote/path/to/drop/to
2. scp -P remote-ssh-port local-file user@ip:/remote/path/to/drop/to
3. scp -i key.pem local-file user@ip:/remote/path/to/drop/to
4. scp user@ip:/remote/path/to/drop/to local-file
5. scp -P remote-ssh-port user@ip:/remote/path/to/drop/to  local-file
6. scp -i key.pem user@ip:/remote/path/to/drop/to local-file
```

#### Sync

To update the database and the local JSON file:

```bash
python3 sync.py
```

If you want to specify a custom JSON file:

```bash
python3 sync.py -f <path/to/json/file>
```

> NOTE: Please make sure that you have set the variables inside config.ini file correctly before running this script

## What I want HackProbe to be

- [x] A quick search engine to search for the commands that you need to carry out a certain task
- [x] A script to sync the local cheat-sheet cache and the remote database
- [ ] A really really pretty frontend that is easy to use and navigate
- [ ] A `docker-compose.yml` file that can be used to deploy the API, database and the frontend altogether
- [ ] A way to share your cheat sheets with others
- [ ] An admin frontend to add, edit and delete cheat sheets without having to mess with RAW JSON

---

### NOTE

This is currently a work in progress. I will update this README as I make progress on the project. I'm making this project in my spare time. If you want to contribute, please feel free to do so.

---
