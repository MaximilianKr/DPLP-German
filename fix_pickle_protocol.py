import pickle
import sys
import gzip

file_path = sys.argv[1]
protocol = 2

with gzip.open(file_path, 'rb') as fin:
    data = pickle.load(fin)

with gzip.open(file_path, 'wb') as fout:
    pickle.dump(data, fout, protocol=2)
