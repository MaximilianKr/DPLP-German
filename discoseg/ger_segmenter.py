""" Call a pretrained segmenter for discourse segmentation
"""

import buildedu
from sys import argv
import argparse, os

def main(readpath, writepath, datapath):
    fvocab = datapath + "/seg-vocab.pickle.gz"
    fmodel = datapath + "/seg-model.pickle.gz"
    buildedu.main(fmodel, fvocab, readpath, writepath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Segments the texts in a specified path, using the pre-existing model and vocab in the datapath.',
    )
    parser.add_argument('path')           # positional argument
    parser.add_argument("-d", "--datapath", type=str, default='data/de', help="Path to the training data files (vocabs, ...)")
    args = parser.parse_args()

    main(args.path, args.path, args.datapath)
