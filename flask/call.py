import sys
import subprocess
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', type=str)
    parser.add_argument('--export', type=str)
    parser.add_argument('--convert', type=str)
    parser.add_argument('--cwd', type=str)
    opt = parser.parse_args()

    # convert the commands back
    train = opt.train.replace('#', ' ')
    export = opt.export.replace('#', ' ')
    convert = opt.convert.replace('#', ' ')

    subprocess.Popen("{} && {} && {}".format(train, export, convert), shell=True, stdout=sys.stdout, stderr=sys.stdout, cwd=opt.cwd)
    # subprocess.Popen("{} && {}".format(export, convert), shell=True, stdout=sys.stdout, stderr=sys.stdout, cwd=opt.cwd)