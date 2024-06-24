import re

words_to_search = ['immigration', "law"]

def count_sentences_with_words(file_path, words):
    sentence_count = 0
    pattern = re.compile(r'\b(?:' + '|'.join(words) + r')\b', flags=re.IGNORECASE)
    with open(file_path, 'r') as file:
        for line in file:
            sentences = line.strip().split('.')
            for sentence in sentences:
                if all(word.lower() in sentence.lower() for word in words):
                    sentence_count += 1

    return sentence_count

file_path = '/Users/fkhan/text1/CRECB-2007-pt26-issue-2007-12-17.htm_12-17-2007_ISSUE.txt'
count = count_sentences_with_words(file_path, words_to_search)
print("Number of sentences with the list of words:", count)