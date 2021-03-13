import sys
from time import perf_counter, sleep

from wordbyword.file_formats.read_file import read_file
from wordbyword.tokenization import split_tokens

filename = input('Enter filename: ')

text = read_file(filename)
if text is None:
    print('Unknown file format.')
    sys.exit(1)


wps = float(input('Words per minute: '))/60

time_per_word = 1/wps
previous_word_len = 0
tokens = split_tokens(text)

for tok in tokens:
    start = perf_counter()

    toklen = len(tok)
    print(tok + ' ' * (previous_word_len - toklen), end='\r')
    previous_word_len = toklen

    elapsed = perf_counter() - start
    to_sleep = time_per_word - elapsed
    if to_sleep > 0:
        sleep(to_sleep)
