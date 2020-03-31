import os
import json
from launcher import show_statistic, show_objective, show_solution

arr_dir = "./arr_outputs/"
mat_dir = "./mat_outputs/"

fname_prefix = "output_"
fname_suffix = ".json"


def read_output(num, directory):
    fpath  = directory + fname_prefix
    fpath += '{:02d}'.format(num) + fname_suffix
    if not os.path.isfile(fpath):
        print("File does not exist!\n path: %s " %(fpath))
        return None

    return json.load(open(fpath))



arr_18 = read_output(18, arr_dir)
mat_18 = read_output(18, mat_dir)

#print('arr_18')
#print(arr_18)
#print('mat_18')
#print(mat_18)

print()
print('arr_18')
show_statistic(arr_18['stats'])
show_objective(arr_18['obj'])
print()
show_solution(arr_18['sol'])
print()

print()
print('mat_18')
show_statistic(mat_18['stats'])
show_objective(mat_18['obj'])
print()
show_solution(mat_18['sol'])
print()
