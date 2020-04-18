# Data una coppia K,H mostra i valori MPOQ delle istanze
# - risolte in minor tempo
# - risolte in maggior tempo
# - con minor numero di persone
# - con maggior numero di persone
# Se un istanza è candidata per più tipologie viene mostrata una sola volta
# Le istanze sono ordinate da sinistra a destra per solveTime crescente

import my_lib
import os
import sys
import json

import numpy as np

import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')

keys = ['M','P','O','Q']

K = 3
H = 3

def get_all_data():
    """ Raccolgo i dati che devo plottare """
    inputs = []
    solveTimes = []
    nums = []

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
    return inputs, solveTimes, nums




def sort_by_solveTime(s_inputs, s_solveTimes, s_nums):
    """ Ordino per solveTime crescente """
    s_inputs = [y for x,y in sorted(zip(s_solveTimes, s_inputs))]
    s_nums   = [y for x,y in sorted(zip(s_solveTimes, s_nums))]
    s_solveTimes = list(sorted(s_solveTimes))
    return s_inputs, s_solveTimes, s_nums


def select_to_plot(inputs, solveTimes, nums):
    """
    Selezioni le istanze che poi plottero'
    Mantengo gli indici relativi
    """
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

    return s_inputs, s_solveTimes, s_nums


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def plot(s_inputs, s_solveTimes, s_nums, show=False, save=True):
    m = [i['M'] for i in s_inputs]
    p = [i['P'] for i in s_inputs]
    o = [i['O'] for i in s_inputs]
    q = [i['Q'] for i in s_inputs]

    labels = [str(n) for n in s_nums]

    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars

    fig, ax1 = plt.subplots()

    # Plotto tempi
    times = ax1.plot(x, s_solveTimes, color='black')
    # End # Plotto tempi

    # Plotto num persone
    ax2 = ax1.twinx()
    n_pers = [i['M']+i['P']+i['O']+i['Q'] for i in s_inputs]
    pers = ax2.plot(x, n_pers, color='orange', alpha=0.7)
    # End Plotto num persone


    # Plotto barre
    ax = ax1.twinx() # instantiate a second axes that shares the same x-axis

    rects_m = ax.bar(x - 3*width/2, m, width, label='M')
    rects_p = ax.bar(x - width/2, p, width, label='P')
    rects_o = ax.bar(x + width/2, o, width, label='O')
    rects_q = ax.bar(x + 3*width/2, q, width, label='Q')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    #ax.set_ylabel('Values')
    ax.set_xlabel('Input Num')
    ax.set_title('K={} H={}'.format(K,H))
    #ax.set_yticks(range(max(m+p+o+q)+1))
    ax.set_yticks([])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    lns = [rects_m, rects_p, rects_o, rects_q, times[0], pers[0]]
    labs = [l.get_label() for l in lns]
    labs = labs[:-2] + ['solveTimes', 'num pers']
    ax.legend(lns, labs)


    for pos in x:
        ax.annotate('{:.2f}'.format(s_solveTimes[pos]),
                    xy=(pos, 0),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    #TODO background color?
                    ha='center', va='bottom')

    autolabel(rects_m,ax)
    autolabel(rects_p,ax)
    autolabel(rects_o,ax)
    autolabel(rects_q,ax)
    # End # Plotto barre

    fig.tight_layout()
    if save:
        fig_path = 'fig_K{}H{}.png'.format(K,H)
        fig.savefig(fig_path)

    if show:
        plt.show()


K = 3
H = 3
def main():
    #args = sys.argv
    #if len(args) > 2:
    #    #print("python output_visualizer.py arr_outputs 18")
    #    print("Al piu' un argomento")
    #    exit(1)

    #try:
    #    num = int(num)
    #except:
    #    print("ERROR!! %s must be a number!!" %(num))
    #    exit(1)
    plot_all = True
    sort     = True

    show     = True
    save     = True

    inputs, solveTimes, nums = get_all_data()
    if plot_all:
        s_inputs, s_solveTimes, s_nums = inputs, solveTimes, nums
    else:
        s_inputs, s_solveTimes, s_nums = select_to_plot(inputs, solveTimes, nums)

    if sort:
        s_inputs, s_solveTimes, s_nums = sort_by_solveTime(s_inputs, s_solveTimes, s_nums)

    plot(s_inputs, s_solveTimes, s_nums, show, save)



if __name__ == '__main__':
    main()
