import os, json
import argparse
import re
import sys
  
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Args are missing: \n 1- path containing the .dis files \n 2- (optional) path of the relation map file')
    path = sys.argv[1]
    frelmap = ''
    if len(sys.argv) > 2:
        frelmap = sys.argv[2]

    relmap = {}
    if frelmap != '':
        with open(frelmap) as f:
            relmap = json.load(f)

    all_files = os.listdir(path)
    for filename in sorted(all_files):
        if not filename.endswith('.dis'):
            continue

        filename = f'{path}/{filename}'
        with open(filename) as f:
            text = f.read()
        
        for key, value in relmap.items():
            text = text.replace(f'(rel2par {key})', f'(rel2par {value})')

        text = re.sub(r'(\(rel2par \s*[\w\-]+\s*\))', lambda m: m.group(1).replace('-', ''), text)
        with open(filename, 'w') as f:
            f.write(text)

    print("Dis files prepared.")
