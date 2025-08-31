import os
import re
from collections import Counter

corpus_dir = 'data/pcc/rs3'
# This pattern specifically finds relname attributes on group or leaf nodes.
relation_pattern = re.compile(r'relname="([^"]+)"')
all_relations = []

for filename in os.listdir(corpus_dir):
    if not filename.endswith('.rs3'):
        continue
    try:
        with open(os.path.join(corpus_dir, filename), 'r') as f:
            content = f.read()
            # We only search for relations that are actually used on nodes.
            relations_in_file = relation_pattern.findall(content)
            all_relations.extend(relations_in_file)
    except Exception as e:
        print(f'Error processing {filename}: {e}')

counts = Counter(all_relations)

if not counts:
    print('No relations with `relname` attributes found in the corpus.')
else:
    for relation, count in counts.most_common():
        print(f'{count:>5} {relation}')
