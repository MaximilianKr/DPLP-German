import os
import argparse
import traceback
import stanza
import torch
from stanza.utils.conll import CoNLL
import re
from legacy_parser_formatter import format_tree, post_process_parse_string

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

def process_file(nlp, file_path_without_ext, is_in_docker):
    """
    Runs all Stanza preprocessing steps on a single text file and
    writes the corresponding output files. Adapts its behavior based
    on the environment (host vs. Docker).
    """
    input_file = f'{file_path_without_ext}.txt'
    print(f"Processing {input_file}")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()

        if not text:
            print(f"Warning: Skipping empty file: {input_file}")
            return

        doc = nlp(text)

        # --- 1. NER Processing ---
        with open(f'{file_path_without_ext}.ner', 'w', encoding='utf-8') as f:
            for sent in doc.sentences:
                for token in sent.tokens:
                    f.write(f"{token.text}\t{token.ner}\n")

        # --- 2. CoNLL Processing ---
        conll = CoNLL.convert_dict(doc.to_dict())
        sent_ind = 0
        newConll = []
        for sent in conll:
            for token in sent:
                token_str = '\t'.join(token)
                token_str = f"{sent_ind}\t{token_str}"
                newConll.append(token_str)
            sent_ind += 1
        conllCombinedPPs = combinePPs('\n'.join(newConll))
        with open(f'{file_path_without_ext}.conll', 'w', encoding='utf-8') as f:
            for row in conllCombinedPPs:
                f.write(f"{row}\n")

        # --- 3. Constituency Parsing (Environment-Dependent) ---
        parse_file = f'{file_path_without_ext}.parse'
        if is_in_docker:
            # Inside Docker: Fallback to BerkeleyParser
            print(f"  (Running in container, falling back to BerkeleyParser for {parse_file})")
            java_command = f'java -jar ./BerkeleyParser-1.7.jar -gr ./ger_sm5.gr -inputFile {input_file} -outputFile {parse_file}'
            os.system(java_command)
        else:
            # On Host: Use Stanza parser
            print(f"  (Running on host, using Stanza for {parse_file})")
            formatted_trees = [format_tree(sentence.constituency) for sentence in doc.sentences]
            final_output_string = post_process_parse_string(' '.join(formatted_trees))
            with open(parse_file, 'w', encoding='utf-8') as f:
                f.write(final_output_string)

    except Exception as e:
        print(f"--- ERROR: Failed to process file: {file_path_without_ext} ---")
        print(e)
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description='Runs all Stanza preprocessing (NER, CoNLL, Constituency Parsing) on .txt files.',
    )
    parser.add_argument('path', help="Directory containing the .txt files")
    args = parser.parse_args()
    path = args.path

    # --- Environment Detection ---
    IS_IN_DOCKER = os.path.exists('/.dockerenv')

    print('====================== Unified Stanza Preprocessing ======================')
    device = "cuda" if torch.cuda.is_available() and not IS_IN_DOCKER else "cpu"
    print(f'Using device: {device}')
    print(f'Running in container: {IS_IN_DOCKER}')
    
    # Initialize a Stanza pipeline that is compatible with the environment
    processors = 'tokenize,pos,lemma,ner,depparse'
    if not IS_IN_DOCKER:
        processors += ',constituency' # Only use constituency on the host
    
    nlp = stanza.Pipeline(
        lang='de',
        processors=processors,
        use_gpu=(device == 'cuda')
    )

    if path.endswith('/'):
        path = path.rstrip('/')
    
    all_files = os.listdir(path)
    for filename in sorted(all_files):
        if not filename.endswith('.txt'):
            continue
        
        file_path_without_ext = os.path.join(path, filename.split('.txt')[0])
        process_file(nlp, file_path_without_ext, IS_IN_DOCKER)
    
    print("====================== Stanza Preprocessing Complete =====================")
