from lxml import etree
import os, sys, json, copy
import argparse
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Reduces the number of relations bsed on <parsing_eval_metrics/rel_mapping.json>',
    )
    parser.add_argument('path')           # positional argument
    args = parser.parse_args()
    path = args.path

    with open('parsing_eval_metrics/rel_mapping.json') as f:
        rel_map = json.load(f)

    all_files = os.listdir(path)
    for filename in sorted(all_files):
        if not filename.endswith('.dis'):
            continue

        filename = f'{path}/{filename}'
        with open(filename) as f:
            text = f.read()
        
        for key, value in rel_map.items():
            text = text.replace(f'(rel2par {key})', f'(rel2par {value})')
        
        with open(filename, 'w') as f:
            f.write(text)

    print("Relations reduced.")