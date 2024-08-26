import sys
import os
import argparse

def txt2parse(file_path):
    infile = f'{file_path}.txt'
    outfile = f'{file_path}.parse'
    
    os.system(f'java -jar ./BerkeleyParser-1.7.jar -gr ./ger_sm5.gr -inputFile {infile} -outputFile {outfile}')

if __name__ == "__main__":
    print('====================== text 2 parse =================\n')

    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Extracts syntax parse tree for the .txt files',
    )
    parser.add_argument('path')           # positional argument
    args = parser.parse_args()
    path = args.path

    if path.endswith('/'):
        path = path[:len(path)-1]
    all_files = os.listdir(path)
    for filename in sorted(all_files):
        if not filename.endswith('.txt'):
            continue
        filename = filename.split('.txt')[0]
        print(f'{path}/{filename}')
        try:
            txt2parse(f'{path}/{filename}')
        except Exception as ex:
            print('###################################################')
            print(filename)
            print(ex)
