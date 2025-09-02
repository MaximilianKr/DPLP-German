import os
import sys
import re
from shutil import copyfile, rmtree
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Trains rst segmenter and parser for the train, dev and test data prepared in a specific path.',
    )
    parser.add_argument('basepath')           # positional argument
    parser.add_argument("-sp", "--skip_prepare", type=bool, default=False, help="Go straight to training. No preparation neede (it is already done)")
    parser.add_argument('-op', "--only_prepare", type=bool, default=False, help='Only prepaer data; exit before training parser or segmenter.')
    parser.add_argument("-n", "--num_matrix", type=int, default=0, help="Number of proj-matrices to check (0: unlimited)")
    parser.add_argument("-m", "--matrix_type", type=str, default="identity", help="Projection matrix type: identity (default), standard")
    parser.add_argument('-rm', "--relation_map", type=str, default='', help='Json file with relation mapping; used to reduce relations in .dis files.')

    args = parser.parse_args()
    print(args)

    for path in (f'{args.basepath}/training',f'{args.basepath}/dev', f'{args.basepath}/test'):
        if not args.skip_prepare:
            os.system(f'python3 ger_0_preprocess_rs3.py {path}')
            os.system(f'python2 ger_1_rst2dis.py {path}')
            os.system(f'python3 ger_2_txt.py {path}')
            # The unified script handles NER, parsing, and CoNLL generation
            os.system(f'python3 run_stanza_preprocessing.py {path}')
            os.system(f'python3 ger_6_conll_rst2merge.py {path}')
    
    if args.only_prepare:
        sys.exit()

    relmap = args.relation_map
    if len(relmap) == 0:
        relmap = 'skip'
    for path in (f'{args.basepath}/training',f'{args.basepath}/dev', f'{args.basepath}/test'):
        os.system(f'python3 ger_7_prepare_dis.py {path} {args.relation_map}')

    if not os.path.exists(f"{args.basepath}/model"):
        os.mkdir(f"{args.basepath}/model")

    os.system(f'python2 ger_7_dpvocab.py {args.basepath}')
    os.system(f'python2 discoseg/ger_7_seg_train.py {args.basepath}')
    
    os.system(f'python2 ger_8_learn_projmat.py {args.basepath} -n {args.num_matrix} -m {args.matrix_type}')
    os.system(f'python3 ger_8_rels_extract.py {args.basepath}')
    os.system(f'python2 ger_9_parser_train.py {args.basepath} | tee {args.basepath}/result.txt')
