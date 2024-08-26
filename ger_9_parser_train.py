from dplp_parser.readdoc import readdoc
from dplp_parser.data import Data
#from fa_proj_model import ParsingModel
from dplp_parser.model import ParsingModel
from dplp_parser.util import reversedict
from dplp_parser.evalparser import evalparser
import cPickle
import pickle
import gzip, os, sys
import argparse

config = {
    'fvocab': "vocab.pickle.gz",
    'fdpvocab': "word-dict.pickle.gz",
    'fbcvocab': "bcvocab.pickle.gz",
    'fdata' : "trn.data",
    'flabel' : "trn.label"
}


# def createdoc(path):
#     ftrn = path + "/trn-doc.pickle.gz"
#     rpath = path + "/training/"
#     readdoc(rpath, ftrn)
#     ftst = path + "/tst-doc.pickle.gz"
#     rpath = path + "/test/"
#     readdoc(rpath, ftst)

def createtrndata(data, path, topn):
    data.builddata(path + '/training')
    data.buildvocab(topn=topn)
    data.buildmatrix()
    data.savematrix(path+config['fdata'], path+config['flabel'])
    data.savevocab(path+config['fvocab'])

def trainmodel(data, path, fmodel):
    import os
    # a = gzip.open(fvocab,mode='rb')
    # D = cPickle.load(a)
    # vocab, labelidxmap = D['vocab'], D['labelidxmap']
    # print 'len(vocab) = {}'.format(len(vocab))
    # trnM, trnL = data.loadmatrix(fdata, flabel)
    # print 'trnM.shape = {}'.format(trnM.shape)
    # idxlabelmap = reversedict(labelidxmap)
    # pm = ParsingModel(vocab=vocab, idxlabelmap=idxlabelmap)
    trnM, trnL = data.loadmatrix(path+config['fdata'], path+config['flabel'])
    pm = ParsingModel(vocab=data.vocab, idxlabelmap=reversedict(data.labelmap))
    pm.train(trnM, trnL)
    pm.savemodel(fmodel)
    #pm.save_projmat("data/fa/projmat.pickle.gz")

def get_rels(basepath):
    with open(basepath + '/relations.txt') as f:
        rels = f.read()
    return rels.split('\n')

if __name__ == '__main__':
    print('====================== parser training =================')
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Trains a model based on a specific projection matrix.',
    )
    parser.add_argument('basepath')           # positional argument
    parser.add_argument("-p", "--fprojmat", type=str, default='model/projmat.pickle.gz', help="The projection matrix pickle file.")
    parser.add_argument("-m", "--fmodel", type=str, default='model/model.pickle.gz', help="The output file containing the trained model.")
    args = parser.parse_args()
    basepath = args.basepath
    if not basepath.endswith('/'):
        basepath += '/'

    # model_name = sys.argv[1]
    # fmodel = "data/de/model/{}.gz".format(model_name)
    ## Use brown clsuters
    with gzip.open(basepath+config['fbcvocab'], 'rb') as fin:
        bcvocab = cPickle.load(fin)
    fprojmat = basepath + args.fprojmat
    fmodel = basepath + args.fmodel

    data = Data(bcvocab=bcvocab,
                withdp=True,
                fdpvocab= basepath+config['fdpvocab'],
                fprojmat= fprojmat
                )
    # Create training data
    createtrndata(data, path= basepath, topn=10000)
    # Train model
    trainmodel(data, basepath, fmodel)
    print("Training finished. Model saved in {}".format(fmodel))

    fpred_dis = basepath+"test/pred_dis/"
    if not os.path.exists(fpred_dis):
        os.mkdir(fpred_dis)

    evalparser(
        path=basepath+"test/", report=True,
        bcvocab=bcvocab, draw=False,
        withdp=True,
        fdpvocab=basepath+config['fdpvocab'],
        modelpath=fmodel,
        fprojmat=fprojmat,
        dis_output_path=fpred_dis,
        fconfusion=basepath+"relation_confusion.csv", 
        rels=get_rels(basepath)
    )

    # os.system("python3 parsing_eval_metrics/stringfiller.py {}test {}test/pred_dis".format(basepath, basepath))
    # os.system("python3 parsing_eval_metrics/jotyize.py {}".format(fpred_dis))
    # os.system("python3 parsing_eval_metrics/jotyize.py {}test".format(basepath))
    # os.system("perl -I./parsing_eval_metrics/ parsing_eval_metrics/ParsingAccuracyMeasuresDocLevelForSystems.pl {}test {} {}joty_eval_{}.txt".format(
    #         basepath, fpred_dis, basepath, fmodel))
