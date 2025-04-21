import os
import re
import argparse
import traceback
import stanza
from stanza.utils.conll import CoNLL
# from stanza.pipeline.core import DownloadMethod


def txt2conll(nlp, file_path):
    with open(f'{file_path}.txt') as f:
        text = f.read()
        
    doc = nlp(text)
    conll = CoNLL.convert_dict(doc.to_dict())

    sent_ind = 0
    newConll = []
    for sent in conll:
        for token in sent:
            # token is list ['1', 'das', 'DET', ...]
            token_str = '\t'.join(token)  # flatten list to tab-separated str
            token_str = f"{sent_ind}\t{token_str}"  # prepend sentence index
            newConll.append(token_str)
        sent_ind += 1
    
    conllCombinedPPs = combinePPs('\n'.join(newConll))
    
    with open(f'{file_path}.conll', 'w') as f :
        for row in conllCombinedPPs:
            f.write(row+'\n')


def find_partial_parse(text, begin, word):
    index = text.find(word, begin)
    if (index < 0):
        return -1
    index += 1
    while(index < len(text)):
        if (text[index] == '('):
            break
        index += 1
    return index


def combinePPs(conll):
    tokens = conll.split('\n')
    pat = re.compile('\d+-\d+')
    newConll = []
    counter = 0
    while counter < len(tokens):
        found = re.findall(pat, tokens[counter])
        if found:
            comb = tokens[counter].split('\t')
            prep = tokens[counter+1].split('\t')
            det = tokens[counter+2].split('\t')
            comb[3] = prep[3]
            comb[4] = prep[4]
            comb[5] = prep[5]
            comb[6] = det[6]
            newConll.append('\t'.join(comb))
            counter += 3
        else:
            newConll.append(tokens[counter])
            counter += 1
    return newConll

if __name__ == "__main__":
    print('====================== text 2 conll =================')

    nlp = stanza.Pipeline(
        lang='de',
        # download_method=DownloadMethod.REUSE_RESOURCES,
    )

    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Creates .conll files for the .txt files.',
    )
    parser.add_argument('path')           # positional argument
    args = parser.parse_args()
    path = args.path

    if path.endswith('/'):
        path = path[:len(path)-1]
    all_files = os.listdir(path)
    counter = 0
    for filename in sorted(all_files):
        if not filename.endswith('.txt'):
            continue
        filename = filename.split('.txt')[0]
        try:
            txt2conll(nlp, f'{path}/{filename}')
        except Exception as ex:
            print('###################################################')
            print(filename)
            print(ex)
            traceback.print_exc()
