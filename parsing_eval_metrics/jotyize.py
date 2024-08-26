import re
import os
import sys

path = sys.argv[1]

files = os.listdir(path)

for f in files:
	form = f.split(".")[-1]
	
	if form != "dis":
		continue
	with open(path + "/" + f) as g:
		content = g.read()
	content = re.sub("\(Root\n", r"(Root", content)
	content = re.sub("\s*\(text\s*", r" (text ", content)
	content = re.sub("(\))(\))", r"\1\n\2", content)
	content = re.sub("(\))(\))", r"\1\n\2", content)
	content = re.sub("\n *(\(rel2par .*\))", r" \1", content)
	content = re.sub("\n\)", "\n )", content)
	content = re.sub("Nucleus\s*", r" Nucleus ", content)
	content = re.sub("Satellite\s*", r" Satellite ", content)
	content = re.sub(" +", " ", content)
	content = re.sub("rel2par manner\)", "rel2par manner-means)", content)


	with open(path + "/" + f, "w") as k:
		k.write(content)







