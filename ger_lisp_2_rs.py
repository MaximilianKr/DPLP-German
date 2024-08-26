import discoursegraphs as dg
import sys
import os
import traceback

# def lisp2rs(dis_fname):
#     rst_tree2 = dg.read_distree(dis_fname + '.lisp')

#     # tree' -> rs3'
#     rs3_fname_reconverted = dis_fname + '_reconverted.rs3'
#     dg.write_rs3(rst_tree2, rs3_fname_reconverted)


# if __name__ == "__main__":
#     print('====================== lisp 2 rs =================')
#     path = sys.argv[1]
#     if path.endswith('/'):
#         path = path[:len(path)-1]
#     all_files = os.listdir(path)
#     for filename in all_files:
#  		# process only merged files
#         if not filename.endswith('.lisp'):
#             continue
#         filename = filename.split('.lisp')[0]
#         # try:
#         print(path+'/'+filename)
#         print('&&&&&&&&&&&&&&&&&&&&')
#         lisp2rs(path+'/'+filename)
#         # except Exception as ex:
#         #     print('###################################################')
#         #     if os.path.exists(path+'/'+filename+'.dis'):
#         #     	os.remove(path+'/'+filename+'.dis')
#         #     print(filename)
#         #     print(ex)
#         #     print(traceback.format_exc())



#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

"""
These Tests aim to show that RST trees remain unchanged, even after reconversion.
"""

import os
# from tempfile import mkdtemp


import discoursegraphs as dg


def test_rs3_dis_pcc_reconvert(dis_fname):
    """rs3->tree->dis->tree->rs3->tree"""
    # temp_dir = mkdtemp()
    # dis -> tree'
    rst_tree2 = dg.read_distree(dis_fname)
    # tree' -> rs3'
    rs3_fname = dis_fname
    rs3_fname_reconverted = rs3_fname + '_reconverted.rs3'
    dg.write_rs3(rst_tree2, rs3_fname_reconverted)
    # assert rst_tree1.tree.pformat() == rst_tree2.tree.pformat() == rst_tree3.tree.pformat()


if __name__== "__main__":
    fpath = sys.argv[1]
    test_rs3_dis_pcc_reconvert(fpath)