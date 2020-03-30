import os, sys
from math import ceil

from datetime import datetime
import random
from random import randint
random.seed(datetime.now())

from minizinc import Instance, Model, Solver


def read_dzn(fpath):
    # TODO try catch
    f = open(fpath)

    comment_char = '%'
    values = {'K':-1,'H':-1,'M':-1,'P':-1,'O':-1,'Q':-1}

    lines = f.readlines()
    for l in lines:
        if comment_char in l:
            index = l.find(comment_char)
            l = l[0:index]

        l = l.replace(" ","")
        l = l.replace("\t","")
        l = l.replace("\n","")
        if not l=='' and '=' in l and ';' in l:
            l = l.replace(";","")
            k,v = l.split('=')
            if k in values.keys():
                # TODO try catch su int
                values[k] = int(v)

    for k in values.keys():
        if values[k] == -1:
            print("Not well formatted input")
            exit(2)

    return values


def get_input(num):
    if num >  100:
        print("ERROR! get_input() num troppo grande")
        exit(2)
    fpath = dest_dir + fname_prefix
    fpath += '{:02d}'.format(num)
    fpath += fname_suffix
    # TODO try catch
    return read_dzn(fpath)


def write_dzn(values, fpath):
    # TODO try catch
    f = open(fpath,'w')

    comment_char = '%'

    ref_dict = {'K':-1,'H':-1,'M':-1,'P':-1,'O':-1,'Q':-1}
    if not values.keys() == ref_dict.keys():
        print("Values non contiene tutti i valori")
        exit(1)

    for k in values.keys():
        if values[k] == -1:
            print("Values non ha tutti i valori inizzializzati")
            exit(2)
        text = str(k) +  "=" + str(values[k]) + ";\n"
        f.write(text)


# Ritorna il massimo numero di persone nelle stanze
# Ipotizzo di poter mettere 2 persone per stanza
#def capienza_max(K=0,H=0):
#    return 2*H*K*2
def capienza_max(values):
    return 2*values['H']*values['K']*2

# Ritorna il numero di stanze
#def numero_stanze(K=0,H=0):
#    return 2*H*K
def numero_stanze(values):
    return 2*values['H']*values['K']

# Ritorna il numero di stanze minimo per ospitare
# le persone indicate
#def stanze_necessarie(M=0,P=0,O=0,Q=0):
#    return ceil(M/2) + ceil(P/2) + O + ceil(Q/2)
def stanze_necessarie(values):
    return ceil(values['M']/2) +\
           ceil(values['P']/2) +\
           values['O'] +\
           ceil(values['Q']/2)

# Ritorna dizionario con chiavi M,P,O,Q
# con i valori per occupare tutte le stanze con
# due ospiti oppure uno in Osservazione
#def occupa_tutto(K=0,H=0,M=0,P=0,O=0,Q=0):
def satura_stanze(values):
    values = values.copy()
    if stanze_necessarie(values) > numero_stanze(values):
        print("IMPOSSIBLE")
        exit(1)
    keys = ['M','P','O','Q']
    while stanze_necessarie(values) <= numero_stanze(values):
        rk = randint(0,len(keys)-1)
        values[keys[rk]] += 1
        last_key = keys[rk]

    values[last_key] -= 1
    # Se ho valori dispari significa che ho una sola persona
    # in una stanza, se posso ne inserisco un'altra
    for k in ['M','P','Q']:
        if values[k]%2 == 1:
            values[k] += 1

    if stanze_necessarie(values) > numero_stanze(values):
        print("DEBUG: qualcosa non va...")
        print(values)


    return values

def istanza_casuale(values):
    values = satura_stanze(values)
    if randint(0,2) != 2: # due volte su tre
        keys = ['M','P','O','Q']
        # rimuovo un po' di persone a caso
        n_rimuovere = randint(1, capienza_max(values)//4)
        rimosse=0
        while rimosse != n_rimuovere:
            key = keys[randint(0,len(keys)-1)]
            da_rimuovere = randint(1,n_rimuovere-rimosse)
            if values[key] >= da_rimuovere:
                values[key] -= da_rimuovere
                rimosse += da_rimuovere

    else:
        # dimezzo Malati, Positivi o Quarantena
        keys = ['M','P','Q']
        key = keys[randint(0,len(keys)-1)]
        values[key] = values[key]//2 + values[key]%2 #mantengo dispari se era disp

    return values


# Genera n istanze casuali con H e K dato
def genera_istanze(n, K, H):
    istanze = []
    values = {'K':K,'H':H,'M':0,'P':0,'O':0,'Q':0}

    for i in range(n):
        istanze.append(istanza_casuale(values))

    return istanze


values = {'K':1,'H':1,'M':1,'P':0,'O':0,'Q':0}
values = {'K':2,'H':3,'M':1,'P':0,'O':0,'Q':0}

dest_dir = "./inputs/"
fname_prefix = "input_"
fname_suffix = ".dzn"

def main():
    K_max = 4
    H_max = 4
    n = 4 # istanze per ogni coppia K,H

    num=0 # numero istanza corrente
    for k in range(1,K_max+1):
        for h in range(2, H_max+1):
            values = {'K':k,'H':h,'M':0,'P':0,'O':0,'Q':0}
            for i in range(n):
                ist = istanza_casuale(values)

                fpath = dest_dir + fname_prefix
                fpath += '{:02d}'.format(num)
                fpath += fname_suffix
                write_dzn(ist,fpath)

                num += 1


if __name__ == "__main__":
    main()

