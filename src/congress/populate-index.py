from elasticsearch import Elasticsearch
from datetime import datetime
import re
import os
import urllib3
from tqdm import tqdm
import hashlib
import secrets
from concurrent.futures import ThreadPoolExecutor, as_completed
from elasticsearch import helpers

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
client = Elasticsearch(['https://elastic:iloveoranges@localhost:9200'], verify_certs=False)


# def insert_data_bulk(docs):
#     try:
#         response = client.bulk(body=docs)
#         if not response["errors"]:
#             print(f"Inserted {len(docs)} documents")
#         else:
#             print(f"Failed to insert {len(docs)} documents")
#     except Exception as e:
#         print('insert_data_bulk:', e)

def extract_date_from_string(string):
    pattern = r'\b(\d{1,2}-\d{1,2}-\d{4})\b'
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    else:
        return None


def process_directory(directory):
    try:
        paths = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath) and filepath.endswith(".txt"):
                paths.append(filepath)
        return paths
    except Exception as e:
        print('process_directory', e)


def concurrentMap(fn, l_args, workers=200, **kwargs):
    try:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            for f in as_completed(ex.submit(fn, arg, **kwargs) for arg in l_args):
                try:
                    yield f.result()
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)


def generate_random_hash():
    random_data = secrets.token_bytes(16)
    hash = hashlib.sha1(random_data).hexdigest()
    return hash

def process_5(file_path):
    if '_' in file_path:
        _, date, section = file_path.split("_")
        date = date.replace('April', '04')
        section = section.replace(".txt", '').upper()
    else:
        date = extract_date_from_string(file_path)

    with open(file_path, 'r', encoding="utf8") as file:
        docs = []
        lines_buffer = []  # Buffer to accumulate lines
        for line in file:
            lines_buffer.append(line.strip())
            if len(lines_buffer) == 5:
                doc = {
                    "_index": "congress-aggregated",
                    "date": datetime.strptime(date, "%m-%d-%Y"),
                    "document_id": generate_random_hash(),
                    "content": "\n".join(lines_buffer)  # Join lines into a single document
                }
                docs.append(doc)  # Append each document to the list
                lines_buffer = []  # Reset buffer for the next document

        # If there are remaining lines in the buffer, create a document with them
        if lines_buffer:
            doc = {
                "_index": "congress-aggregated",
                "date": datetime.strptime(date, "%m-%d-%Y"),
                "document_id": generate_random_hash(),
                "content": "\n".join(lines_buffer)
            }
            docs.append(doc)

    helpers.bulk(client, docs)

def process(file_path):
    if '_' in file_path:
        _, date, section = file_path.split("_")
        date = date.replace('April', '04')
        section = section.replace(".txt", '').upper()
    else:
        date = extract_date_from_string(file_path)

    with open(file_path, 'r', encoding="utf8") as file:
        docs = []
        for line in file:
            doc = {
                "_index": "congress",
                "date": datetime.strptime(date, "%m-%d-%Y"),
                "document_id": generate_random_hash(),
                "content": line.strip()
            }
            docs.append(doc)  # Append each document to the list
    helpers.bulk(client, docs)


directory_path = 'E:\\archive\\text2'
paths = process_directory(directory_path)
print("Processing text2 1 line")
it = concurrentMap(process, paths, workers=200)
progress = True
if progress:
    it = tqdm(it, total=len(paths), desc="Downloading files")
for r in it:
    pass
print("Processing text2 5 line")
it = concurrentMap(process_5, paths, workers=200)
progress = True
if progress:
    it = tqdm(it, total=len(paths), desc="Downloading files")
for r in it:
    pass

directory_path = 'E:\\archive\\text1'
paths = process_directory(directory_path)
print("Processing text1 1 line")
it = concurrentMap(process, paths, workers=2000)
progress = True
if progress:
    it = tqdm(it, total=len(paths), desc="Downloading files")
for r in it:
    pass
print("Processing text1 5 line")
it = concurrentMap(process_5, paths, workers=2000)
progress = True
if progress:
    it = tqdm(it, total=len(paths), desc="Downloading files")
for r in it:
    pass

directory_path = 'E:\\archive\\text3'
paths = process_directory(directory_path)
print("Processing text3 1 line")
it = concurrentMap(process, paths, workers=200)
progress = True
if progress:
    it = tqdm(it, total=len(paths), desc="Downloading files")
for r in it:
    pass
print("Processing text3 5 line")
it = concurrentMap(process_5, paths, workers=200)
progress = True
if progress:
    it = tqdm(it, total=len(paths), desc="Downloading files")
for r in it:
    pass