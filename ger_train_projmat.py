import os
import sys
import re
from shutil import copyfile, rmtree
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Trains projection matrices baed on the train, dev and test data prepared in a specific path.',
    )
    parser.add_argument('basepath')           # positional argument
    parser.add_argument("-s", "--skip_prepare", type=bool, default=False, help="Go straight to training. No preparation neede (it is already done)")
    parser.add_argument("-n", "--num_matrix", type=int, default=0, help="Number of proj-matrices to check (0: unlimited)")
    parser.add_argument('-sp', "--skip_parser", type=bool, default=False, help='Skips the syntax parsing step in data preparation (for speed)')
    args = parser.parse_args()

    if not args.skip_prepare:
        for path in (f'{args.basepath}/training',f'{args.basepath}/dev', f'{args.basepath}/test'):
            os.system(f'python3 ger_0_preprocess_rs3.py {path}')
            os.system(f'python2 ger_1_rst2dis.py {path}')
            os.system(f'python3 ger_1_reduce_relations.py {path}')
            os.system(f'python3 ger_2_txt.py {path}')
            os.system(f'python3 ger_3_ner.py {path}')
            if not args.skip_parser:
                os.system(f'python3 ger_4_txt2parse.py {path}')
            os.system(f'python3 ger_5_txt2conll.py {path}')
            os.system(f'python3 ger_6_conll_rst2merge.py {path}')

    os.system(f'python2 discoseg/ger_7_seg_train.py {args.basepath}')
    os.system(f'python2 ger_7_dpvocab.py {args.basepath}')
    
    os.system(f'python2 ger_8_learn_projmat.py {args.basepath} -n {args.num_matrix}')
