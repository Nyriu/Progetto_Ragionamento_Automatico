import sys
import json

UNSAT = '=====UNSATISFIABLE=====\n'

def format_as_json(text):
    if text==UNSAT:
        print(UNSAT)
        exit(1)

    text = '[\n' + text
    if (10*'=' in text):
        text = text.replace(10*'-',',')
        text = text.replace(10*'=',']')
        #text = text.replace('\n]\n,\n]','\n]\n]')
        i = 10
        last_i = text[-i:]
        text = text[:-i]
        text = text + last_i.replace('\n,\n','\n')
    else: # ho una soluzione singola
        text = text.replace(10*'-',']')

    return text

def show_raw_solutions(fname):
    # TODO try catch
    f = open(fname)
    text = f.read()

    solutions = json.loads(format_as_json(text))
    for sol in solutions:
        print(sol)

def get_solutions(fname):
    # TODO try catch
    f = open(fname)
    text = f.read()

    solutions = json.loads(format_as_json(text))
    return solutions



symbols = {
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
        symb = symbols['malato']
    elif (sol['M'].count(s) == 2):
        symb = symbols['malati']

    elif (sol['P'].count(s) == 1):
        symb = symbols['positivo']
    elif (sol['P'].count(s) == 2):
        symb = symbols['positivi']

    elif (sol['O'].count(s) == 1):
        symb = symbols['osservazione']

    elif (sol['Q'].count(s) == 1):
        symb = symbols['quarantena']
    elif (sol['Q'].count(s) == 2):
        symb = symbols['quaranteni']

    else:
        symb = symbols['empty']

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


f_00 = "output_00.txt"
f_03 = "output_03.txt"
f_04 = "output_04.txt"
f_05 = "output_05.txt"
f_06 = "output_06.txt"


def main():

    args = sys.argv
    if len(args) < 2:
        print("Put one argument!!")
        exit(1)

    solutions = get_solutions(args[1])
    for i,sol in enumerate(solutions):
        print(10*'-', "Solution",i, 10*'-')
        show_solution(sol)


if __name__ == '__main__':
    main()
