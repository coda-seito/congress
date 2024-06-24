import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import re

file_path = "./txt/absolute.txt"

list_arr = []
with open(file_path, 'r') as file:
    for line in file:
        str = line.strip()
        if str:
            arr = line.split(",")
            pub_date = arr[0]
            section = arr[1]
            filename = arr[2].replace("\n", "")
            file_name_end = filename.replace("html/", "")
            # parts = file_name_end.split("-")
            # result = "-".join(parts[:3]).replace(".pdf",'').replace("pdf",'')
            # result = re.sub(r'-pt\d', '', result)
            # result = re.sub(r'-vol\d', '', result)
            url = f"https://www.govinfo.gov/content/pkg/{filename}"
            list_arr.append(url + "|" + file_name_end+"_"+ pub_date+"_"+section+".pdf")

import PyPDF2

def is_valid_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            _ = PyPDF2.PdfFileReader(file)
        return True
    except Exception as e:
        return False

def download_large_file(line):
    try:
        url, file_name = line.split('|')
        save_path = f'./txt/{file_name}'
        if os.path.exists(save_path) and is_valid_pdf(save_path):
            return
        else:
            print('|', end='')
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
    except Exception as e:
        print(e)

def concurrentMap(fn, l_args, workers=20, **kwargs):
    try:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            print("Starting Futures")
            for f in as_completed(ex.submit(fn, arg, **kwargs) for arg in l_args):
                try:
                    yield f.result()
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)

it = concurrentMap(download_large_file, list_arr)
progress = True
if progress:
    it = tqdm(it, total=len(list_arr), desc="Downloading files")
for r in it:
    pass
