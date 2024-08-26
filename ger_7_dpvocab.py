import pickle as cPickle
import gzip
import os
from dplp_parser.data import Data
import sys
import argparse

def bc_prepare(basepath):
    all_content = ''
    for sub in ['training', 'dev', 'test']:
        print("word_bc for " + sub)
        subpath = basepath + '/' + sub + '/'
        all_files = os.listdir(subpath)
        for f in all_files:
            if(f.endswith('.txt')):
                with open(subpath + f) as g:
                    all_content += g.read() + '\n'
    with open(basepath +'/words_bc.txt', 'w') as f:
        f.write(all_content)
        print('word_bc.txt created')
    os.system('python3 tan-clustering/pmi_cluster.py {}/words_bc.txt {}/words_bc_out.txt'.format(basepath, basepath))
    print('tab clustering -> words_bc_out.txt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Creates vocabulary for training.',
    )
    parser.add_argument('basepath')           # positional argument
    parser.add_argument("-q", "--quick", type=bool, default=False)
    args = parser.parse_args()
    print(args)

    print("================== Build Vocabs =====================")
    if not args.quick:
        bc_prepare(args.basepath)
    dpvocab = {} 
    for sub in ['training', 'dev', 'test']:
        print('dpvocab for ' + sub)
        subpath = args.basepath + '/' + sub
        for filename in os.listdir(subpath):
            if args.quick or (not filename.endswith('.txt')):
                continue
            with open(subpath + '/' + filename) as f:
                text = f.read()
            for token in text.split():
                # if token in dpvocab:
                dpvocab[token] = dpvocab.get(token, len(dpvocab))


    bcvocab = {}

    with open(args.basepath + '/words_bc_out.txt') as f:
        tokens = f.readlines()
        for tok in tokens:
            word_clust, word, idx = tok.split('\t')
            bcvocab[word] = word_clust

    fdpvocab = args.basepath + '/word-dict.pickle.gz'
    fbcvocab = args.basepath + '/bcvocab.pickle.gz'
    fvocab = args.basepath + '/vocab.pickle.gz'

    fp=gzip.open(fdpvocab,'wb')
    cPickle.dump(dpvocab,fp, protocol=2)
    fp.close()
    print("dpvocab saved in {}".format(fdpvocab))

    fp=gzip.open(fbcvocab,'wb')
    cPickle.dump(bcvocab,fp, protocol=2)
    fp.close()
    print("bcvocab saved in {}".format(fbcvocab))

    data = Data(bcvocab=bcvocab, withdp=False)

    data.builddata(args.basepath + '/training')
    data.buildvocab(topn=10000)
    data.savevocab(fvocab)
    print("Vocab saved in {}".format(fvocab))


