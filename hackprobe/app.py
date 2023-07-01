from fastapi import FastAPI, Request
import uvicorn
import re
import argparse

from scripts.utils import *

app = FastAPI()

def get_match(match : str):
    res = []
    
    if isinstance(match , str):
        match = match.split()

    try:
        client = MongoClient(Config.conn_string)
        db = client[Config.db_name]
        collection = db[Config.collection_name]
        pattern = [re.compile(f'.*{word}.*', re.IGNORECASE) for word in match]
        query = {'tags': {'$all': pattern}}
        results = collection.find(query)
        for doc in results:
            res.append(doc)
        client.close()
        for i in range(len(res)):
            res[i].pop('_id')
    except Exception as e:
        msg(f"An error occurred! {e.__str__()}", '!')
    finally:
        return res
    
@app.get('/')
def index():
    return { "message" : "Welcome to HackProbe API Server!" }, 200

@app.get('/search')
def search(request : Request, match : str):
    msg(f"To match: {Colors.BLUE}{match}{Colors.RESET} FROM {Colors.MAGENTA}{request.client.host}{Colors.RESET}", '+')
    results = get_match(match)
    return { "results" : results }, 200

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='HackProbe API Server', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config', help='Config file to load', default='config.ini')
    parser.add_argument('-H', '--host', help='Host to run the server on', default='0.0.0.0')
    parser.add_argument('-p', '--port', help='Port to run the server on', default=5000)
    args = parser.parse_args()

    if not check_config(config_file=args.config):
        exit(1)

    msg("Starting the server...", '*')
    uvicorn.run(
        app,
        host=args.host,
        port=args.port
    )