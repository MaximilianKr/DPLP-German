## evalparser.py
## Author: Yangfeng Ji
## Date: 11-05-2014
## Time-stamp: <yangfeng 09/25/2015 16:32:42>

#from fa_proj_model import ParsingModel
from model import ParsingModel
import os
from tree import RSTTree
from docreader import DocReader
from evaluation import Metrics
from os import listdir
from os.path import join as joinpath
from util import drawrst, reversedict


def parse(pm, doc):
    """ Parse one document using the given parsing model

    :type pm: ParsingModel
    :param pm: an well-trained parsing model

    :type fedus: string
    :param fedus: file name of an document (with segmented EDUs) 
    """
    pred_rst = pm.sr_parse(doc)
    return pred_rst


def writebrackets(fname, brackets):
    """ Write the bracketing results into file
    """
    # print 'Writing parsing results into file: {}'.format(fname)
    with open(fname, 'w') as fout:
        for item in brackets:
            fout.write(str(item) + '\n')


def evalparser(path='./examples', report=False, 
               bcvocab=None, draw=True,
               withdp=False, fdpvocab=None, fprojmat=None,
               modelpath=None, dis_output_path=None, fconfusion=None, rels=None):
    """ Test the parsing performance

    :type path: string
    :param path: path to the evaluation data

    :type report: boolean
    :param report: whether to report (calculate) the f1 score
    """
    # ----------------------------------------
    # Load the parsing model
    # print 'Load parsing model ...'
    pm = ParsingModel(withdp=withdp,
        fdpvocab=fdpvocab, fprojmat=fprojmat)
    pm.loadmodel(modelpath)
    if not isinstance(pm.labelmap.keys()[0], int):
        pm.labelmap = reversedict(pm.labelmap)

    # ----------------------------------------
    # Evaluation
    met = Metrics(levels=['span','nuclearity','relation'])
    conf_matrix = dict({})
    # ----------------------------------------
    # Read all files from the given path
    doclist = [joinpath(path, fname) for fname in listdir(path) if fname.endswith('.merge')]
    for fmerge in doclist:
        # ----------------------------------------
        # Read *.merge file
        dr = DocReader()
        doc = dr.read(fmerge)
        # ----------------------------------------
        # Parsing
        pred_rst = pm.sr_parse(doc, bcvocab)
        name = fmerge.split("/")[-1]
        dis_name = name[:len(name) - 6] + ".dis"
        if (dis_output_path is not None):
            if not dis_output_path.endswith('/'):
                dis_output_path += '/'
            cont = pred_rst.writetree(pred_rst.tree, "Root")
            dis_filename =  dis_output_path + dis_name
            with open(dis_filename, "w") as f:
                f.write(cont)

        if draw:
            strtree = pred_rst.parse()
            drawrst(strtree, fmerge.replace(".merge",".ps"))
        # Get brackets from parsing results
        pred_brackets = pred_rst.bracketing()
        fbrackets = fmerge.replace('.merge', '.brackets')
        # Write brackets into file
        writebrackets(fbrackets, pred_brackets)
        # ----------------------------------------
        # Evaluate with gold RST tree
        if report:
            fdis = '{}/{}'.format(path, dis_name)

            # print 'Updating confusion matrix with dis file: ' + fdis

            fgod_merge = fdis.replace(".dis",".merge")
            gold_rst = RSTTree(fdis, fgod_merge)
            gold_rst.build()
            gold_brackets = gold_rst.bracketing()
            met.eval(gold_rst, pred_rst)
            update_confusion(conf_matrix, gold_rst, pred_rst)

    if report:
        if (fconfusion is not None):
            report_confusion(conf_matrix, fconfusion, rels)
        return met.report()

def report_confusion(conf_matrix, fconfusion, rels):

    with open(fconfusion, 'w') as f:
        f.write("Relations\t")
        for r in rels:
            f.write(r)
            f.write("\t")
        f.write("\n")

        for r in rels:
            f.write(r)
            f.write("\t")

            for c in rels:
                if r not in conf_matrix or c not in conf_matrix[r]:
                    f.write('0')
                else:
                    f.write(str(conf_matrix[r][c]))
                f.write("\t")
            f.write("\n")


def update_confusion(conf_matrix, gold_rst, pred_rst):
    goldbrackets = gold_rst.bracketing()
    predbrackets = pred_rst.bracketing()

    for g_brac in goldbrackets:
        for p_brac in predbrackets:
            if g_brac[0] != p_brac[0]:
                continue

            if(g_brac[2] not in conf_matrix):
                conf_matrix[g_brac[2]] = dict({})

            conf_matrix[g_brac[2]][p_brac[2]] = conf_matrix[g_brac[2]].get(p_brac[2], 0) + 1




