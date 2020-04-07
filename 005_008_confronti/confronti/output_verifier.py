import os
import sys
import json
from launcher import show_statistic, show_objective, show_solution

arr_dir = "./arr_outputs/"
mat_dir = "./mat_outputs/"

fname_prefix = "output_"
fname_suffix = ".json"


def read_output(num, directory, suppress_error=False):
    if not directory[-1] == '/':
        directory = directory + '/'
    fpath  = directory + fname_prefix
    fpath += '{:02d}'.format(num) + fname_suffix
    if not os.path.isfile(fpath):
        if not suppress_error:
            print("File does not exist!\n path: %s " %(fpath))
        return None

    return json.load(open(fpath))




def main():

    args = sys.argv
    if len(args) < 3:
        print("Put two arguments!! For example")
        print("python output_verifier.py arr_outputs mat_outputs")
        exit(1)

    source_dir1 = args[1]
    source_dir2 = args[2]

    if not os.path.isdir(source_dir1):
        print("ERROR!! %s is not a directory!!" %(source_dir1))
        exit(1)
    if not os.path.isdir(source_dir2):
        print("ERROR!! %s is not a directory!!" %(source_dir2))
        exit(1)

    num=0
    d1 = read_output(num, source_dir1)
    d2 = read_output(num, source_dir2)
    while not (d1 is None or d2 is None):
        obj1 = d1['obj']
        obj2 = d2['obj']
        print("num:", num)

        if (obj1 != obj2):
            print("Different obj!")
            print("obj1:",obj1,"\tobj2:",obj2)
        else:
            print("ok")
        print()
        num+=1
        d1 = read_output(num, source_dir1)
        d2 = read_output(num, source_dir2)


if __name__ == '__main__':
    main()
