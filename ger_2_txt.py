import sys, os
from bs4 import BeautifulSoup
import sys
import stanza
import re
import os, html
import argparse

nlp = stanza.Pipeline(lang='de', processors='tokenize')

def rst2txt(filepath):
    outfile = open(filepath + '.txt', 'w')
    rst = open(filepath + '.rs3', 'r').read()
    rst = '<xml>' + rst + '</xml>'
    soup = BeautifulSoup(rst, features='lxml')
    seg_ind = 1
    tok_ind = 0
    segments = soup.find_all('segment')
    for segment in segments:
        content = html.unescape(segment.text).replace(' .', '.')
        outfile.write(content + ' ')

if __name__ == "__main__":
    print('====================== rst 2 text =================')
    
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Extracts text from .rs3 files',
    )
    parser.add_argument('path')           # positional argument
    args = parser.parse_args()
    path = args.path

    if path.endswith('/'):
        path = path[:len(path)-1]
    all_files = os.listdir(path)
    counter = 0
    for filename in sorted(all_files):
        if not filename.endswith('.rs3'):
            continue
        filename = filename.split('.rs3')[0]
        try:
            rst2txt(f'{path}/{filename}')
        except Exception as ex:
            print('###################################################')
            print(ex)
            print(filename)

        counter += 1
        if counter % 10 == 0:
            print("Progress: {} / {}".format(counter, len(all_files)))

