from dplp_parser.evalparser import evalparser
from cPickle import load
import sys
import gzip
import argparse, os


#Example: python2 ger_rstparser.py data/test -p  data/de/model/K_150_Tau_0.5_C_1_iter_100.projmat.gz -m  data/de/model/K_150_Tau_0.5_C_1.model.gz  -d data/de -o data/de


def main(inpath, outpath, datapath, fprojmat, fmodel):
  with gzip.open(datapath + "/bcvocab.pickle.gz", 'rb') as fin:
    bcvocab = load(fin)

  evalparser(path=inpath, report=False, draw=False,
             bcvocab=bcvocab,
             withdp=True,
             fdpvocab= datapath + "/word-dict.pickle.gz",
             fprojmat= fprojmat,
             modelpath= fmodel,
             dis_output_path=outpath, fconfusion= inpath + '/relation_confusion.csv')


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Generates rst trees for the segmented text  files (.conll format).',
    )
  
  parser.add_argument('path')           # positional argument 
  parser.add_argument("-p", "--fprojmat", type=str, default='data/de/model/projmat.pickle.gz', help="The projection matrix pickle file.")
  parser.add_argument("-m", "--fmodel", type=str, default='data/de/model/model.pickle.gz', help="The trained model.")
  parser.add_argument("-d", "--datapath", type=str, default='data/de', help="Path to the training data files.")
  parser.add_argument("-o", "--outpath", type=str, help="The path of the output dis and rs3 files.")
  args = parser.parse_args()
  
  outpath = args.outpath
  if outpath is None:
    outpath = args.path
  
  print('Read files from {} and write output to: {}'.format(args.path, outpath))
  main(args.path, outpath, args.datapath, args.fprojmat, args.fmodel)
