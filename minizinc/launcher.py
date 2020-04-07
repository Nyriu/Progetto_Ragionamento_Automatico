import os
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
    if sol == None:
        print("No solution")
        return None

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
    if solution is None:
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
        sol['M'] = solution["malati"]
        sol['P'] = solution["positivi"]
        sol['O'] = solution["osservazione"]
        sol['Q'] = solution["quarantena"]

    show_solution(sol)
    return sol


# Qua faccio una cosa un po' brutta # Converto la solution di un modello MAT
# in un dizionario che simula una solution
# di un modello ARR
def to_sol(solution):
    if solution is None:
        return None
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





def show_statistic(statistics):
    stats = {}
    # valore, tempo di flat, tempo di resol, tempo totale)
    stats['method']    = statistics['method']

    try:
        stats['time']      = float(statistics['time'].total_seconds())
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

    for k in stats.keys():
        val = stats[k]
        if type(val) == str:
            print('{:10}:{:>10}'.format(k, stats[k]))
        elif type(val) == float:
            print('{:10}:{:10f}'.format(k, stats[k]))
        elif type(val) == int:
            print('{:10}:{:10d}'.format(k, stats[k]))
        else:
            print('Non sarei dovuto arrivare qua')

    return stats

def show_objective(obj):
    if obj is None:
        print('{:10}:{:>10}'.format('objective', 'None'))
    else:
        print('{:10}:{:10d}'.format('objective',obj))


def show_result(result, instance, model_type):
    if not model_type in ['ARR', 'MAT']:
        print("ERROR! show_result() unknown model_type")

    show_statistic(result.statistics)
    show_objective(result.objective)

    print()
    if model_type == 'MAT':
        show_arr_solution(to_sol(result.solution), instance)
    else:
        show_arr_solution(result.solution, instance)



# TODO silenziare i print
def save_result(result, instance, model_type, fpath):
    if not model_type in ['ARR', 'MAT']:
        print("ERROR! save_result() unknown model_type")
    stats = show_statistic(result.statistics)
    obj = result.objective

    if model_type == 'MAT':
        sol = show_arr_solution(to_sol(result.solution), instance)
    else:
        sol = show_arr_solution(result.solution, instance)

    data = {}
    data['model_type'] = model_type
    data['obj'] = obj
    data['stats'] = stats
    data['sol'] = sol

    # TODO try catch
    json.dump(data, open(fpath, 'w+'), indent=True)
    #json.dump(indent=True)


def run_on_all_inputs(model_path, model_type, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    if not output_dir[-1] == '/':
        output_dir += '/'

    fname_prefix = "output_"
    fname_suffix = ".json"

    model = Model(model_path)
    gecode = Solver.lookup("gecode")

    input_num = 0
    while not get_input(input_num) is None:
        instance = Instance(gecode, model)
        initialize(instance, input_num)
        result = instance.solve()

        output_path  = output_dir + fname_prefix
        output_path += '{:02d}'.format(input_num)
        output_path += fname_suffix

        print("Lavoro su input num %d" %(input_num))
        save_result(result, instance, model_type, output_path)

        input_num += 1





if __name__ == '__main__':
#### ROBE DI PROVA ####
    run_on_all_inputs('./covid19.mzn', 'MAT', './mat_outputs')


##input_num = 0
##
### Load model from file
##model = Model("./example_mat_model.mzn"); model_type = 'MAT'
##
### Find the MiniZinc solver configuration for Gecode
##gecode = Solver.lookup("gecode")
##
##instance = Instance(gecode, model)
##initialize(instance, input_num)
##result = instance.solve()
##
##show_result(result, instance, model_type)
##
##
### Load model from file
##model = Model("./example_arr_model.mzn"); model_type = 'ARR'
##
### Find the MiniZinc solver configuration for Gecode
##gecode = Solver.lookup("gecode")
##
##instance = Instance(gecode, model)
##initialize(instance, input_num)
##result = instance.solve()
##
##show_result(result, instance, model_type)
##
