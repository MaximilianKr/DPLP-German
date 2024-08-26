import sys
import os, io, sys
import traceback
import discoursegraphs as dg
from bs4 import BeautifulSoup
from shutil import copyfile
import argparse

def rs2dis_convert(file_path):
    tree = dg.read_rs3tree(file_path + '.rs3')
    dg.write_dis(tree, output_file=file_path + '.dis')

if __name__ == "__main__":
    print('====================== rst 2 dis =================')
    
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Converts .rs3 files to .dis format',
    )
    parser.add_argument('path')           # positional argument
    args = parser.parse_args()
    path = args.path
    
    if path.endswith('/'):
        path = path[:len(path) - 1]
    all_files = os.listdir(path)
    for filename in sorted(all_files):
        # process only merged files
        if not filename.endswith('.rs3'):
            continue
        filename = filename.split('.rs3')[0]

        try:
            rs2dis_convert(path + '/' + filename)
        except Exception as ex:
            print('################################################### ')
            print(filename)
            print(ex)
            traceback.print_exc()
