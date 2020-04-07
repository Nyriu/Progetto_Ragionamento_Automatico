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



## arr_18 = read_output(18, arr_dir)
## mat_18 = read_output(18, mat_dir)
##
## #print('arr_18')
## #print(arr_18)
## #print('mat_18')
## #print(mat_18)
##
## print()
## print('arr_18')
## show_statistic(arr_18['stats'])
## show_objective(arr_18['obj'])
## print()
## show_solution(arr_18['sol'])
## print()
##
## print()
## print('mat_18')
## show_statistic(mat_18['stats'])
## show_objective(mat_18['obj'])
## print()
## show_solution(mat_18['sol'])
## print()


def main():

    args = sys.argv
    if len(args) < 3:
        print("Put two arguments!! For example")
        print("python output_visualizer.py arr_outputs 18")
        exit(1)

    source_dir = args[1]
    num = args[2]

    if not os.path.isdir(source_dir):
        print("ERROR!! %s is not a directory!!" %(source_dir))
        exit(1)
    try:
        num = int(num)
    except:
        print("ERROR!! %s must be a number!!" %(num))
        exit(1)


    data = read_output(num, source_dir)
    print(data)
    print()
    show_statistic(data['stats'])
    show_objective(data['obj'])
    print()
    show_solution(data['sol'])
    print()



if __name__ == '__main__':
    main()
