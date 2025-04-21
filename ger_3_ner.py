import os
import argparse
import stanza
# from stanza.pipeline.core import DownloadMethod


if __name__ == "__main__":
    print('====================== ner extraction =================')
    nlp = stanza.Pipeline(
        lang='de',
        # download_method=DownloadMethod.REUSE_RESOURCES,
        processors='tokenize,ner'
    )
   
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Extracts NER data for the content of the .txt files.',
    )
    parser.add_argument('path')           # positional argument
    args = parser.parse_args()
    path = args.path
 
    if path.endswith('/'):
        path = path[:len(path)-1]

    all_files = os.listdir(path)

    for filename in sorted(all_files):
        if not filename.endswith('.txt'):
            continue
        filename = filename.split('.')[0]
        try:
            with open(path + '/' + filename +'.txt') as f:
                content = f.read()

            print(path + '/' + filename +'.txt')
            processed_text = nlp(content)

            with open(path + '/' + filename + '.ner', 'w') as f:
                for sent in processed_text.sentences:
                    for token in sent.tokens:
                        f.write(token.text + '\t' + token.ner + '\n')
        except Exception as ex:
            print('###################################################')
            print(filename)
            print(ex)
