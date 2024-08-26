import os
import sys
import re
from shutil import copyfile, rmtree
from lxml import etree
import argparse, json

# Example: python3 ger_predict_dis_from_txt.py data/test -p  data/de/model/K_150_Tau_0.5_C_1_iter_100.projmat.gz -m  data/de/model/K_150_Tau_0.5_C_1.model.gz  -d data/de -o data/de/test

def convert_dis_to_rs3(predict, path):
   for fname in os.listdir(predict):
        if not fname.endswith('.dis'):
            continue

        fname = fname[0:-4]
        with open(f'{path}/{fname}.merge') as f:
            merge_lines = f.readlines()

        edus = []
        tokens = []
        prev_edu = -1
        for word in merge_lines:
            word = word.strip()
            if not len(word):
                continue
            cols = word.split('\t')
            token = cols[2]
            edu_num = int(cols[-1])
            if prev_edu != -1 and prev_edu != edu_num:
                edus.append(' '.join(tokens))
                tokens = []
            prev_edu = edu_num
            tokens.append(token)
        if len(tokens):
            edus.append(' '.join(tokens))

        os.system(f'python ger_lisp_2_rs.py {predict}/{fname}.dis')
        rst_tree = etree.parse(f'{predict}/{fname}.dis_reconverted.rs3')

        leaves = rst_tree.xpath('/rst/body/segment')
        for i in range(len(leaves)):
            leaves[i].text = edus[i]
        
        # fix_rs3_relations(rst_tree, etree)
        rst_tree.write(f'{predict}/{fname}.rs3', encoding='utf8' )
    
def fix_rs3_relations(rs3_tree, etree):
    with open('parsing_eval_metrics/rel_mapping.json') as f:
        rel_map = json.load(f)

    reltypes = set()
    relsnode = rs3_tree.xpath('/rst/header/relations')[0]
    for rel in list(relsnode.xpath('rel')):
        name = rel.get('name').lower()
        rel.set('name', name)
        reltypes.add((name, rel.get('type')))
    
    for rel in rel_map.keys():
        reltype = 'rst'
        if rel_map[rel] == 'additive':
            reltype = 'multinuc'
        if not (rel, reltype) in reltypes:
            element = etree.SubElement(relsnode, 'rel')
            element.set('name', rel)
            element.set('type', reltype)
            reltypes.add((rel, reltype))
    
    for rel in rel_map.keys():
        reltype = 'rst'
        if rel == 'additive':
            reltype = 'multinuc'
        if not (rel, reltype) in reltypes:
            element = etree.SubElement(relsnode, 'rel')
            element.set('name', rel)
            element.set('type', reltype)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Predicts the rst three (.dis and .rs3 files) for all .txt files in the <path>.',
    )
    parser.add_argument('path')           # positional argument
    parser.add_argument("-p", "--fprojmat", type=str, default='data/de/model/projmat.pickle.gz', help="The projection matrix pickle file.")
    parser.add_argument("-m", "--fmodel", type=str, default='data/de/model/model.pickle.gz', help="The trained model file.")
    parser.add_argument("-d", "--datapath", type=str, default='data/de', help="Path to the training data files (vocabs, ...)")
    parser.add_argument("-o", "--outpath", type=str, help="The path of the output dis and rs3 files.")
    # TODO: add argument for segmenter model
    args = parser.parse_args()

    outpath = args.outpath
    if outpath is None:
        outpath = args.path

    if not os.path.exists(f'{args.path}'):
        raise Exception(f'The input path {args.path} is missing.') 
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        
    # os.system(f'python3 ger_2_txt.py {args.path}')
    os.system(f'python3 ger_3_ner.py {args.path}')
    os.system(f'python3 ger_4_txt2parse.py {args.path}')
    os.system(f'python3 ger_5_txt2conll.py {args.path}')
    
    # run segmente:
    os.system(f'python2 discoseg/ger_segmenter.py {args.path} -d {args.datapath}')
    # run parser, but don't report because everything is predicted.
    os.system(f'python2 ger_rstparser.py {args.path} -p {args.fprojmat} -m {args.fmodel} -d {args.datapath} -o {outpath}')

    convert_dis_to_rs3(outpath, args.path)

    print(f'Output files are saved in {outpath}')
