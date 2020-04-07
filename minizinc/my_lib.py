##################################################
# Import
##################################################
# Varie
import os
from math import ceil

# Per Random
from datetime import datetime
from random import randint
import random
random.seed(datetime.now())

# Per minizinc
from minizinc import Instance, Model, Solver

##################################################
# Globali
##################################################
# Inputs
DEST_DIR = "./inputs/"
INPUT_PREFIX = "input_"
INPUT_EXT = ".dzn"

# Pretty print dell'Output
SYMBOLS = {
        "empty"        : "--",
        "malato"       : "-M",
        "malati"       : "MM",
        "positivo"     : "-P",
        "positivi"     : "PP",
        "osservazione" : "-O",
        "quarantena"   : "-Q",
        "quaranteni"   : "QQ"
        }


##################################################
# Lettura Scrittura Input
##################################################

# Dato un numero e suffisi e prefissi torna
# dest_dir + fname_prefix + numero in fotmato {:02d} + fname_suffix
def gen_input_fpath(num, dest_dir=DEST_DIR,
        input_prefix=INPUT_PREFIX, input_suffix=INPUT_EXT):
    fpath = dest_dir + input_prefix
    fpath += '{:02d}'.format(num)
    fpath += input_suffix
    return fpath

# Dato un dizionario di un input lo salva nel file indicato
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

# Dato un file path ritorna il dizionario dell'input
def read_dzn(fpath):
    # TODO try catch
    if not os.path.isfile(fpath):
        return None

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

# Dato un numero ritorna il dizionario dell'input relativo
def get_input(num, dest_dir=DEST_DIR):
    if num >  100:
        print("ERROR! get_input() num troppo grande")
        exit(2)
    fpath = gen_input_fpath(num, dest_dir)
    # TODO try catch
    return read_dzn(fpath)






##################################################
# Generazione Input
##################################################

# Ritorna il massimo numero di persone nelle stanze
# Ipotizzo di poter mettere 2 persone per stanza
def capienza_max(values):
    return 2*values['H']*values['K']*2

# Ritorna il numero di stanze
def numero_stanze(values):
    return 2*values['H']*values['K']

# Ritorna il numero di stanze minimo
# per ospitare le persone indicate
def stanze_necessarie(values):
    return ceil(values['M']/2) +\
           ceil(values['P']/2) +\
           values['O'] +\
           ceil(values['Q']/2)

# Ritorna dizionario con chiavi M,P,O,Q
# con i valori per occupare tutte le stanze con
# due ospiti oppure uno in Osservazione
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
def gen_istanze(n, K, H):
    istanze = []
    values = {'K':K,'H':H,'M':0,'P':0,'O':0,'Q':0}

    for i in range(n):
        istanze.append(istanza_casuale(values))

    return istanze

# Dati K e H massimi da raggiungere genera n istanze per ogni coppia K,H
# TODO Eventualemnte modificare i for perche'
# Creare input cosi' genera istanze con difficolta' a "dente di sega"
def gen_inputs(K_max, H_max, n,
        dest_dir = DEST_DIR, input_prefix=INPUT_PREFIX,
        input_extension=INPUT_EXT):

    os.makedirs(dest_dir, exist_ok=True)

    num=0 # numero istanza corrente
    for k in range(1,K_max+1):
        for h in range(2, H_max+1):
            values = {'K':k,'H':h,'M':0,'P':0,'O':0,'Q':0}
            for i in range(n):
                ist = istanza_casuale(values)

                fpath = gen_input_fpath(num, dest_dir, input_prefix,
                        input_extension)
                write_dzn(ist,fpath)

                num += 1
    print("Generati %d input nella cartella %s" %(num, dest_dir))


##################################################
# Minizinc Models and Intances Stuff
##################################################

# Dati instanza e numero dell'input recupera dzn relativo
# a num e lo carica nell'istanza
def initialize_instance(instance, num, dest_dir=DEST_DIR):
    #TODO try catch
    values = get_input(num,dest_dir)

    instance["K"]=values["K"]; # corridoi
    instance["H"]=values["H"]; # stanze per lato

    instance["M"]=values["M"]; # malati
    instance["P"]=values["P"]; # positivi
    instance["O"]=values["O"]; # osservazione
    instance["Q"]=values["Q"]; # quarantena precauzionale

def show_instance(instance):
    print("K:",instance["K"])
    print("H:",instance["H"])

    print("M:",instance["M"])
    print("P:",instance["P"])
    print("O:",instance["O"])
    print("Q:",instance["Q"])

# Data una soluzione e un numero di una stanza s
# ritorna il simbolo corretto per quella stanza
# Es: -M oppure MM oppure -Q oppure -O
def get_symbol(s,sol):
    if (sol['M'].count(s) == 1):
        symb = SYMBOLS['malato']
    elif (sol['M'].count(s) == 2):
        symb = SYMBOLS['malati']

    elif (sol['P'].count(s) == 1):
        symb = SYMBOLS['positivo']
    elif (sol['P'].count(s) == 2):
        symb = SYMBOLS['positivi']

    elif (sol['O'].count(s) == 1):
        symb = SYMBOLS['osservazione']

    elif (sol['Q'].count(s) == 1):
        symb = SYMBOLS['quarantena']
    elif (sol['Q'].count(s) == 2):
        symb = SYMBOLS['quaranteni']

    else:
        symb = SYMBOLS['empty']

    return symb;
# Data una soluzione e l'istanza ritorna il dizionario sol
# della soluzione (se solution e' None torna None)
def get_sol(solution,instance, show_sol=False):
    if sol == None:
        print("No solution")
        return None

    sol = {}
    sol['K'] = instance['K']
    sol['H'] = instance['H']

    if type(solution) != dict:
        sol['M'] = solution.malati
        sol['P'] = solution.positivi
        sol['O'] = solution.osservazione
        sol['Q'] = solution.quarantena
    else:
        print("ERROR! In get_solution solution e' gia' dict")

    if show_sol:
        show_solution(sol)
    return sol

# Date le statistics torna il dizionario stats
def get_stats(statistics, show_stats=False):
    stats = {}
    # valore, tempo di flat, tempo di resol, tempo totale)
    stats['method']    = statistics['method']

    try:
        stats['time'] = float(statistics['time'].total_seconds())
    except:
        stats['time'] = .0
    try:
        stats['solveTime'] = float(statistics['solveTime'].total_seconds())
    except:
        stats['solveTime'] = .0
    try:
        stats['flatTime']  = float(statistics['flatTime'].total_seconds())
    except:
        stats['flatTime']  = .0
    try:
        stats['solutions'] = statistics['solutions']
    except:
        stats['solutions'] = .0

    if show_stats:
        for k in stats.keys():
            val = stats[k]
            if type(val) == str:
                print("{:10}:{:>10}".format(k, stats[k]))
            elif type(val) == float:
                print("{:10}:{:10f}".format(k, stats[k]))
            elif type(val) == int:
                print("{:10}:{:10d}".format(k, stats[k]))
            else:
                print("ERROR! In get_stats tipo chiave imprevisto!")

    return stats

def show_sol(sol):
    if type(solution) != dict:
        print("ERROR! In show_sol solution deve essere dict")

    if sol == None:
        print("No solution")
        return

    K = sol['K']
    H = sol['H']
    s = 0
    for k in range(K):
        for h in range(2*H):
            code = get_symbol(s,sol)
            e = " "
            if (h==H-1 or h==2*H-1 or h==2*H*K-1):
                e = "\n"
            if (h==H-1):
                code += "\t" + str(k)

            print(code, end=e)
            s+=1
        print()

def show_objective(obj):
    if obj is None:
        print('{:10}:{:>10}'.format('objective', 'None'))
    else:
        print('{:10}:{:10d}'.format('objective',obj))

def show_statistic(statistics):
    get_stats(statistics, show_stats=True)


# Dati result ed instance stampa il recap della soluzione trovata
def show_result(result, instance):
    show_statistic(result.statistics)
    show_objective(result.objective)
    get_sol(result.solution, instance, show_sol=True)

# TODO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# TODO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# TODO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# TODO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

#arrivato a 227 di launcher.py

# TODO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# TODO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# TODO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# TODO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO



##################################################
# Main
##################################################
def main():
    print("Main non ancora implementato")
    print("Probabilmente fara' dei test")

if __name__ == "__main__":
    main()
