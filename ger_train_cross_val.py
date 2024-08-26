import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Trains rst segmenter and parser for a 5-way corss validation data, arranged in k1, ... k5 subdirs of the basepath.',
    )
    parser.add_argument('basepath')           # positional argument
    parser.add_argument("-sp", "--skip_prepare", type=bool, default=False, help="Go straight to training. No preparation neede (it is already done)")
    parser.add_argument('-rm', "--relation_map", type=str, default='', help='Json file with relation mapping; used to reduce relations in .dis files.')

    args = parser.parse_args()
    print(args)

    skip_prepare = ''
    if args.skip_prepare:
        skip_prepare = '-sp True'
    relation_map = ''
    if len(args.relation_map) > 0:
        relation_map = f'-rm {args.relation_map}'

    for k in range(5):
        os.system(f'python3 ger_train.py {args.basepath}/k{k+1} {skip_prepare} {relation_map}')


