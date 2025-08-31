import os
import argparse
import traceback
import stanza
import torch
from stanza.utils.conll import CoNLL
import re

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

def process_files(nlp, file_path_without_ext):
    """
    Runs NER and CoNLL processing on a single file.
    """
    # --- NER Processing (from ger_3_ner.py) ---
    try:
        with open(f'{file_path_without_ext}.txt') as f:
            content = f.read()

        print(f"Processing {file_path_without_ext}.txt")
        doc = nlp(content)

        with open(f'{file_path_without_ext}.ner', 'w') as f:
            for sent in doc.sentences:
                for token in sent.tokens:
                    f.write(token.text + '\t' + token.ner + '\n')

    except Exception as ex:
        print('--- NER Error ---')
        print(f"Failed on: {file_path_without_ext}")
        print(ex)
        return # Skip to next file if NER fails

    # --- CoNLL Processing (from ger_5_txt2conll.py) ---
    try:
        # We already have the processed 'doc' from the NER step
        conll = CoNLL.convert_dict(doc.to_dict())

        sent_ind = 0
        newConll = []
        for sent in conll:
            for token in sent:
                token_str = '\t'.join(token)
                token_str = f"{sent_ind}	{token_str}"
                newConll.append(token_str)
            sent_ind += 1
        
        conllCombinedPPs = combinePPs('\n'.join(newConll))
        
        with open(f'{file_path_without_ext}.conll', 'w') as f :
            for row in conllCombinedPPs:
                f.write(row+'\n')

    except Exception as ex:
        print('--- CoNLL Error ---')
        print(f"Failed on: {file_path_without_ext}")
        print(ex)
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description='Runs Stanza NER and CoNLL preprocessing on all .txt files in a directory.',
    )
    parser.add_argument('path')
    args = parser.parse_args()
    path = args.path

    print('====================== Stanza Preprocessing (NER & CoNLL) =================')
    print(f'Use device: {"cuda" if torch.cuda.is_available() else "cpu"}')
    
    # Initialize the Stanza pipeline once
    nlp = stanza.Pipeline(
        lang='de',
        use_gpu=True
    )

    if path.endswith('/'):
        path = path[:len(path)-1]
    
    all_files = os.listdir(path)
    for filename in sorted(all_files):
        if not filename.endswith('.txt'):
            continue
        
        file_path_without_ext = os.path.join(path, filename.split('.txt')[0])
        process_files(nlp, file_path_without_ext)
    
    print("====================== Stanza Preprocessing Complete ======================")
