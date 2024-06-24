import pytesseract
import fitz
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from util import old_download
from tqdm import tqdm

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from io import BytesIO
import os
import time
import torch

from PIL import Image
import io
import numpy as np
import easyocr


def img_to_text_easy_ocr(image_bytes, i, file_name):
    try:
        # Open the image using PIL
        image_pil = Image.open(io.BytesIO(image_bytes))

        # Initialize EasyOCR reader with GPU support
        reader = easyocr.Reader(['en'], gpu=True)

        start_time = time.time()
        # Perform OCR on the image
        results = reader.readtext(np.array(image_pil))  # Convert PIL Image to NumPy array
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Write OCR results to a text file
        path = f'./txt/{file_name}.txt'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'a') as file:
            file.write(f'Page: {i + 1}\n')
            for result in results:
                file.write(result[1] + '\n')  # Extract text from OCR result
    except Exception as e:
        print(e)


def img_to_text_tesseract(image_bytes, i, file_name):
    try:
        image_pil = Image.open(BytesIO(image_bytes))
        start_time = time.time()
        text = pytesseract.image_to_string(image_pil, lang='eng')
        end_time = time.time()
        elapsed_time = end_time - start_time
        path = f'./txt/{file_name}.txt'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'a') as file:
            file.write(f'Page: {i + 1}\n')
            file.write(text)
    except Exception as e:
        print(e)


def read_pdf(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        return pdf_document
    except Exception as e:
        print(e)


def pdf_to_images(pdf_document, page_number, resolution=100):
    try:
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap(matrix=fitz.Matrix(resolution / 72, resolution / 72))
        image_bytes = image.tobytes()
        return image_bytes
    except Exception as e:
        print(e)


def download_large_file(url, save_path):
    try:
        if os.path.exists(save_path):
            return
        else:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            print('@', end='')
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
    except Exception as e:
        print(e)


def process(line):
    try:
        date = line.split("|")[0]
        url = line.split("|")[1]
        file_name = os.path.basename(url)
        pdf_path = f'./download/{file_name}'
        download_large_file(url, pdf_path)
        pdf_document = read_pdf(pdf_path)

        new_file_name = file_name.replace(".pdf", "") + "-" + date
        path = f'./txt/{new_file_name}.txt'
        if os.path.exists(path):
            return
        else:
            print('|', end='')
            for page_number in range(pdf_document.page_count):
                image = pdf_to_images(pdf_document, page_number)
                img_to_text_easy_ocr(image, page_number, new_file_name)

        with open('./completed.txt', 'a') as file:
            file.write(pdf_path + "\n")
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


device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
print(device)
it = concurrentMap(process, old_download)
progress = True
if progress:
    it = tqdm(it)
for r in it: {}
