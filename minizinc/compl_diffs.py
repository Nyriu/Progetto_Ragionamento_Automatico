# Data una coppia K,H mostra i valori MPOQ delle istanze
# - risolte in minor tempo
# - risolte in maggior tempo
# - con minor numero di persone
# - con maggior numero di persone
# Se un istanza è candidata per più tipologie viene mostrata una sola volta
# TODO Le istanze sono ordinate da sinistra a destra per solveTime crescente

import my_lib
import os
import sys
import json

import numpy as np

import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')

keys = ['M','P','O','Q']

K = 2
H = 3


inputs = []
solveTimes = []
nums = []

# Raccolgo i dati che devo plottare
num = 0
inp = my_lib.get_input(num)
out = my_lib.read_output(num, my_lib.OUTPUT_DIR, suppress_error=True)
while not (out == None):
    if inp['K'] == K and inp['H'] == H:
        inputs.append(inp)
        solveTimes.append(out['stats']['solveTime'])
        nums.append(num)

    num+=1
    inp = my_lib.get_input(num)
    out = my_lib.read_output(num, my_lib.OUTPUT_DIR, suppress_error=True)


## DEBUG STUFF
#cut_l = 5
#nums = nums[:cut_l]
#solveTimes = solveTimes[:cut_l]
#inputs = inputs[:cut_l]
#
#for i in inputs:
#    print(i)
##END DEBUG STUFF

# Selezioni le istanze che poi plottero'
# Mantengo gli indici relativi
ind_min_sTime = None # risolto in meno tempo
ind_max_sTime = None # risolto in piu' tempo
ind_min_peps  = None  # con minor numero di persone
ind_max_peps  = None  # con maggior numero di persone
for i, inp in enumerate(inputs):
    if ind_min_sTime == None or solveTimes[i] < solveTimes[ind_min_sTime]:
        ind_min_sTime = i
    elif ind_max_sTime == None or solveTimes[i] > solveTimes[ind_max_sTime]:
        ind_max_sTime = i

    if ind_min_peps == None and ind_max_peps == None:
        ind_min_peps = i
        ind_max_peps = i

    m_peps = 0 # min num persone
    M_peps = 0 # max num persone
    peps = 0   # persone correnti
    for k in keys:
        m_peps += inputs[ind_min_peps][k]
        M_peps += inputs[ind_max_peps][k]
        peps += inp[k]
    if peps < m_peps:
        ind_min_peps = i
    elif peps > M_peps:
        ind_max_peps = i


# Rimuovo duplicati
selected = list(set([ind_min_sTime, ind_max_sTime, ind_min_peps, ind_max_peps]))

s_inputs     = [inputs[i] for i in selected]
s_solveTimes = [solveTimes[i] for i in selected]
s_nums       = [nums[i] for i in selected]


m = [i['M'] for i in s_inputs]
p = [i['P'] for i in s_inputs]
o = [i['O'] for i in s_inputs]
q = [i['Q'] for i in s_inputs]

labels = [str(n) for n in s_nums]

x = np.arange(len(labels))  # the label locations
width = 0.1  # the width of the bars

fig, ax = plt.subplots()
rects_m = ax.bar(x - 3*width/2, m, width, label='M')
rects_p = ax.bar(x - width/2, p, width, label='P')
rects_o = ax.bar(x + width/2, o, width, label='O')
rects_q = ax.bar(x + 3*width/2, q, width, label='Q')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Values')
ax.set_xlabel('Inputs')
#ax.set_title('Scores by group and gender')
ax.set_yticks(range(max(m+p+o+q)+1))
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# Annoto i tempi
plt.annotate('{}'.format("solveTimes"), TODO
            xy=(-1, 0),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            #TODO background color?
            ha='center', va='bottom')
for pos in x:
    ax.annotate('{}'.format(s_solveTimes[pos]),
                xy=(pos, 0),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                #TODO background color?
                ha='center', va='bottom')

autolabel(rects_m)
autolabel(rects_p)
autolabel(rects_o)
autolabel(rects_q)

fig.tight_layout()

plt.show()


##def main():
##    args = sys.argv
##    if len(args) < 3:
##        print("Put two arguments!! For example")
##        print("python output_visualizer.py arr_outputs 18")
##        exit(1)
##
##    source_dir = args[1]
##    num = args[2]
##
##    if not os.path.isdir(source_dir):
##        print("ERROR!! %s is not a directory!!" %(source_dir))
##        exit(1)
##    try:
##        num = int(num)
##    except:
##        print("ERROR!! %s must be a number!!" %(num))
##        exit(1)
##
##
##    data = read_output(num, source_dir)
##    print(data)
##    print()
##    show_statistic(data['stats'])
##    show_objective(data['obj'])
##    print()
##    show_solution(data['sol'])
##    print()
##
##
##
##if __name__ == '__main__':
##    main()
