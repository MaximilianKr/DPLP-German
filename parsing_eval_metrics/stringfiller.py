import sys, os, re

golddir = sys.argv[1]
preddir = sys.argv[2]


goldfiles = os.listdir(golddir)
predfiles = os.listdir(preddir)


for file in goldfiles:
	if(not file.endswith(".dis")):
		continue
	print(file)
	with open(golddir + "/" + file) as f:
		gold = f.read()

		content = re.findall("\(leaf (\d+)\).*\(text _\!(.*)_\!", gold)

		pred = ""
		with open(preddir + "/" + file) as g:
			pred = g.read()

		pred = re.sub("lorem ipsum", "", pred)
		for i in range(len(content)):
			pred = re.sub("(\(leaf " + str(content[i][0]) + "\).*\(text.*_\!)(_\!)", r"\1" + content[i][1] + r"\2", pred)
			pred = re.sub("\n\(", "\n (", pred)

		pred = re.sub(r"\)\)", ")\n )", pred)

		with open(preddir + "/" + file , "w") as k:
			k.write(pred)


