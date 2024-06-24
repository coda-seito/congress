import os
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

html_directory = '/Users/fkhan/PycharmProjects/maps/congres/txt/text'

files = os.listdir(html_directory)

def combine_hyphenated_words(line):
    words = line.split()
    combined_words = []
    i = 0
    while i < len(words):
        if '-' in words[i]:
            combined_word = words[i]
            i += 1
            while i < len(words) and '-' in words[i]:
                combined_word += words[i]
                i += 1
            combined_words.append(combined_word)
        else:
            combined_words.append(words[i])
            i += 1
    return ' '.join(combined_words)

def process(input_file_str):
    input_file = f'/Users/fkhan/PycharmProjects/maps/congres/txt/text/{input_file_str}'
    output_file = f'/Users/fkhan/text3/{input_file_str}'

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        current_sentence = ""
        for line in infile:
            line = combine_hyphenated_words(line.strip())
            current_sentence += line + " "
            sentences = sent_tokenize(current_sentence)
            if len(sentences) > 1:
                outfile.write(sentences[0].strip() + '\n')
                current_sentence = sentences[-1]
        if current_sentence.strip():
            outfile.write(current_sentence.strip() + '\n')

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

it = concurrentMap(process, files)
progress = True
if progress:
    it = tqdm(it, total=len(files), desc="Downloading files")
for r in it:
    pass