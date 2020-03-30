import sys
import json
from input_generator import get_input
from minizinc import Instance, Model, Solver

# Varie
# Due tipi di modello ARR e MAT


# Dati instanza e numero dell'input
# recupera dzn relativo a num e lo carica
# nell'istanza
def initialize(instance, num):
    #TODO try catch
    values = get_input(num)

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


def show_solution(sol):
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


def show_arr_solution(solution,instance):
    sol = {}
    sol['K'] = instance['K']
    sol['H'] = instance['H']

    if type(solution) != dict:
        sol['M'] = solution.malati
        sol['P'] = solution.positivi
        sol['O'] = solution.osservazione
        sol['Q'] = solution.quarantena
    else:
        sol['M'] = solution["malati"]
        sol['P'] = solution["positivi"]
        sol['O'] = solution["osservazione"]
        sol['Q'] = solution["quarantena"]

    show_solution(sol)


# Qua faccio una cosa un po' brutta # Converto la solution di un modello MAT
# in un dizionario che simula una solution
# di un modello ARR
def to_sol(solution):
    solution = solution.sol

    K = len(solution)
    H = len(solution[0])

    sol = {}
    sol["malati"] = []
    sol["positivi"] = []
    sol["osservazione"] = []
    sol["quarantena"] = []

    s=0 # numero della stanza corrente
    for k in range(K):
        for h in range(H):
            for l in [0,1]:
                if solution[k][h][l] == 1:
                    sol["malati"].append(s)
                elif solution[k][h][l] == 2:
                    sol["positivi"].append(s)
                elif solution[k][h][l] == 3:
                    sol["osservazione"].append(s)
                elif solution[k][h][l] == 4:
                    sol["quarantena"].append(s)

                elif solution[k][h][l] == 5:
                    sol["malati"].append(s)
                    sol["malati"].append(s)
                elif solution[k][h][l] == 6:
                    sol["positivi"].append(s)
                    sol["positivi"].append(s)
                elif solution[k][h][l] == 7:
                    sol["quarantena"].append(s)
                    sol["quarantena"].append(s)
                else:
                    # stanza vuota
                    pass

                s += 1
    return sol





def show_statistic(stats):
    # valore, tempo di flat, tempo di resol, tempo totale)
    print('{:10}:{:>10}'.format('method',stats['method']))

    print('{:10}:{:10f}'.format('time',stats['time'].total_seconds()))
    print('{:10}:{:10f}'.format('flatTime',stats['flatTime'].total_seconds()))
    print('{:10}:{:10f}'.format('solveTime',stats['solveTime'].total_seconds()))

    print('{:10}:{:10d}'.format('solutions', stats['solutions']))


def show_result(result, instance, model_type):
    if not model_type in ['ARR', 'MAT']:
        print("ERROR! show_result() unknown model_type")

    show_statistic(result.statistics)
    print('{:10}:{:10d}'.format('objective',result.objective))
    print()
    if model_type == 'MAT':
        show_arr_solution(to_sol(result.solution), instance)
    else:
        show_arr_solution(result.solution, instance)







input_num = 12

# Load model from file
model = Model("./example_mat_model.mzn"); model_type = 'MAT'

# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")

# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, model)
initialize(instance, input_num)
result = instance.solve()

show_result(result, instance, model_type)


# Load model from file
model = Model("./example_arr_model.mzn"); model_type = 'ARR'

# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")

# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, model)
initialize(instance, input_num)
result = instance.solve()

show_result(result, instance, model_type)




