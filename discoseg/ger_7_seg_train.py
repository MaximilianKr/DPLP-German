"""
All in one module
1, build vocab
2, build training samples
3, train a segmentation model
"""

import buildvocab, buildsample, buildmodel, buildedu
import os
import argparse

def main():
    print('====================== segmenter training =================')

    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='Trains rst segmenter for the dev, training and test data prepared in a specific path.',
    )
    parser.add_argument('basepath')           # positional argument
    args = parser.parse_args()

    basepath = args.basepath

    trainpath = basepath + '/segtrain'
    testpath = basepath + '/test'
    devpath = basepath + '/dev'
    fvocab = basepath + '/seg-vocab.pickle.gz'
    ftrain = basepath + '/seg-train.pickle.gz'
    fdev =   basepath + '/seg-dev.pickle.gz'
    fmodel = basepath + '/seg-model.pickle.gz'
    
    # Fixed
    os.system("rm -rf rst/seg")
    # os.system("mkdir rst")
    os.system("rm -rf {}".format(trainpath))
    os.system("mkdir {}".format(trainpath))
    os.system("cp -r {}/training/* {}".format(basepath, trainpath))
    os.system("cp -r {}/dev/* {}".format(basepath, trainpath))

    os.system("rm -rf {}/segmenter_result".format(basepath))
    os.system("mkdir {}/segmenter_result".format(basepath))
    writepath = "{}/segmenter_result".format(basepath)
    
    ## Build vocab
    thresh = 2
    buildvocab.main(trainpath, thresh, fvocab)
    ## Build training data
    buildsample.main(trainpath, ftrain, fvocab)
    ## Build dev data
    buildsample.main(devpath, fdev, fvocab)
    ## Build test data
    # buildsample.main(testpath, ftest, fvocab)
    ## Training
    buildmodel.main(ftrain=ftrain, fdev=fdev, fmodel=fmodel)
    ## Segmentation
    buildedu.main(fmodel, fvocab, testpath, writepath)

if __name__ == '__main__':
    main()
