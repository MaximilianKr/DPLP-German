import os, re
import argparse

def get_rels(basepath):
    with open(basepath + '/relations.txt') as f:
        rels = f.read()
    return rels.split('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Extracts the list of relations from all .dis files.',
    )
    parser.add_argument('path')           # positional argument

    args = parser.parse_args()
    basepath = args.path

    rels = []

    for dr in ['test', 'training', 'dev']:
        for fn in os.listdir(f'{basepath}/{dr}'):
            if not fn.endswith('.dis'):
                continue
            with open(f'{basepath}/{dr}/{fn}') as f:
                txt = f.read()
            
            pattern = re.compile(r"\(rel2par (\w+)\s*\)")
            for match in pattern.finditer(txt):
                relname = match.group(1)
                if not relname in rels:
                    rels.append(match.group(1))
    
    with open(f'{basepath}/relations.txt', 'w') as f :
        rels.sort()
        f.write('\n'.join(rels))

    print(get_rels(basepath))
