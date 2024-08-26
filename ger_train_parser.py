import os
import sys
import re
from shutil import copyfile, rmtree
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Trains rst segmenter using the projmat found by ger_train_projmat.py and the train, dev and test data prepared in the specific path.',
    )
    parser.add_argument('basepath')           # positional argument
    parser.add_argument("-p", "--fprojmat", type=str, default='data/de/model/projmat.pickle.gz', help="The projection matrix pickle file.")
    parser.add_argument("-m", "--fmodel", type=str, default='data/de/model/model.pickle.gz', help="The trained model.")
    args = parser.parse_args()

    os.system(f'python2 ger_9_parser_train.py {args.basepath} -p {args.fprojmat} -m {args.fmodel}')
