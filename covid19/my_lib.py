##################################################
# Import
##################################################
# Varie
import os, shutil
from math import ceil

# Per Random
from datetime import datetime
from random import randint
import random
random.seed(datetime.now())

# Per minizinc
import json
from minizinc import Instance, Model, Solver

# Le mie globali
import my_globals


##################################################
# Input
##################################################
class MyInstance:

    def __init__(self):
        self.values = {'K':-1,'H':-1,'M':-1,'P':-1,'O':-1,'Q':-1}

    """
    #def __init__(self, values):
    #    assert(type(values) == dict)
    #    for key in values.keys():
    #        self.values[key] = values[key]
    """

    def capienza_max(self):
        """ Ritorna il massimo numero di persone sistemabili nelle stanze
            Ipotizzo di poter mettere 2 persone per stanza """
        return 2*values['H']*values['K']*2

    def numero_stanze(self):
        """ Ritorna il numero di stanze """
        return 2*values['H']*values['K']

    def stanze_necessarie(self):
        """ Ritorna il numero di stanze minimo
            per ospitare le persone """
        return ceil(values['M']/2) +\
               ceil(values['P']/2) +\
               values['O'] +\
               ceil(values['Q']/2)

    def write_dzn(self, fpath):
        """ Scrive l'istanza in formato dzn nel path dato """

    def write_lp(self, fpath):
        """ Scrive l'istanza in formato lp nel path dato """

    # Getter e Setter ####################
    def get_corridoi(self,k):
        assert(k>0); return self.values['K']
    def get_stanze_per_lato(self,h):
        assert(h>0); return self.values['H']
    def get_malati(self,m):
        assert(m>=0); return self.values['M']
    def get_positivi(self,p):
        assert(p>=0); return self.values['P']
    def get_osservazione(self,o):
        assert(o>=0); return self.values['O']
    def get_quarantena(self,q):
        assert(q>=0); return self.values['Q']

    def set_corridoi(self,k):
        assert(k>0); self.values['K'] = k
    def set_stanze_per_lato(self,h):
        assert(h>0); self.values['H'] = h
    def set_malati(self,m):
        assert(m>=0); self.values['M'] = m
    def set_positivi(self,p):
        assert(p>=0); self.values['P'] = p
    def set_osservazione(self,o):
        assert(o>=0); self.values['O'] = o
    def set_quarantena(self,q):
        assert(q>=0); self.values['Q'] = q

    # Metodi statici ####################
    def read(fpath):
        """ Ritorna MyIstance del path indicato """
         # TODO qua gestire in automatico i due formati


class MySolution():
    """ Rappresenta la soluzione ad un istanza del problema
        Viene salvata come json con formato unico
        Un campo apposito permette di capire se la soluzione e' stata
        ottenuta con modello mzn o lp """

    def __init__(model_output):
        """ Inizializza MySolution a partire dall'output
            di un modello mzn o lp """
        # TODO if da mzn fai una roba
        # TODO elif da lp fanne un'altra
        # TODO else esplodi

    def write(self, fpath):
        """ Scrive la soluzione in formato json nel path dato """

    # Metodi statici ####################
    def read(fpath):
        """ Ritorna MySolution del path indicato """


    class AbstractConverter():
        """ Usando metodo convert permette di ottenere la codifica univoca
            di una soluzione """
            @abstractmethod
            def convert(self, model_output):
                pass
            def check(self):
                """ Verifica che la conversione sia stata
                    effettuata correttamente """
    class ConverterMzn(AbstractConverter):
        """ Permette di ottenere la codifica univoca di una soluzione di
            un modello mzn """
        def convert(model_output):
            converted = _from_mzn(model_output)
            if check(converted):
                return converted

        def _from_mzn(model_output):
            """ Converte l'output di un modello mzn in quello univoco """

    class ConverterLp(AbstractConverter):
        """ Permette di ottenere la codifica univoca di una soluzione di
            un modello lp """
        def convert(model_output):
            converted = _from_lp(model_output)
            if check(converted):
                return converted

        def _from_lp(model_output):
            """ Converte l'output di un modello lp in quello univoco """





class InputGenerator:

    def satura_stanze(MyInstance):
        """ Data una MyInstance torna una MyInstance in cui i valori
            degli ospiti sono stati modificati per occupare tutte le stanze """

    def istanza_casuale(k=None,h=None):
        """ Se k e h non vengono specificati torna una MyInstance casuale
            Altrimenti torna un'istanza casuale per k e h dati """

    def write_istanze(n, k_min,h_min, k_max,h_max,
            order=None, delete_old=True):
        """ Genera n istanze causali con k e h nei range dati poi
            le salva nei formati .dzn e .lp nelle cartelle
            INPUT_MZN_DIR INPUT_LP_DIR rispettivamente
            Se delete_old=True allora svuota le cartelle prima di generare
            """

    def _gen_istanze(n, k_min,h_min, k_max,h_max):
        """ Torna una lista di n istanze casuali con
            k in range(k_min,k_max) e h in range(h_min,h_max) """

    def _del_inputs(input_dir = INPUT_DIR):
        shutil.rmtree(input_dir, ignore_errors=True)



class BatchCoordinator:
    """ Un Batch e' l'insieme:
        - dei modelli mzn e lp
        - delle cartelle di input e output sia mzn che lp
        - di grafici relativi a modelli e input/output

        BatchCoordinator si preoccupa di generare e salvare
        un Batch correttamente
        """
    class Batch:
        def __init__(self):
            self.num =None
            self.path=None


    def _biggest_batch_num():
        """ Verifica quali batch sono gia' stati creati e ritorna quello
            con il numero piu' grande """

    def save_as_batch(dir_to_save):
        """ Raccoglie tutte le informazioni relative ad un
            Batch all'interno della cartella data e le salva
            come Batch in una sottocartella di BATCH_ROOT_DIR """


class AbstractRunner:
    """ Con run si puo' eseguire il modello indicato su tutti le istanze oppure
        su un'istanza specifica
        Si puo' specificare se mostrare la soluzione, salvarla o entrambi """

    @abstractmethod
    def 






# Dato un numero e suffisi e prefissi torna
# directory + fname_prefix + numero in formato {:02d} + fname_suffix
def gen_fpath(num, directory, prefix, suffix):
    fpath = directory + prefix
    fpath += '{:02d}'.format(num)
    fpath += suffix
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

    #def __init__(self, values):
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
def get_input(num, dest_dir=INPUT_DIR):
    #if num >  100:
    #    print("ERROR! get_input() num troppo grande")
    #    exit(2)
    fpath = gen_fpath(num, dest_dir, INPUT_PREFIX, INPUT_EXT)
    # TODO try catch
    return read_dzn(fpath)

# Dato un numero ritorna il testo dell'input relativo
def get_input_text(num, dest_dir=INPUT_DIR):
    #if num >  100:
    #    t = "ERROR! get_input() num troppo grande"
    #    print(t)
    #    return t

    fpath = gen_fpath(num, dest_dir, INPUT_PREFIX, INPUT_EXT)

    if not os.path.isfile(fpath):
        t = "ERROR! File does not exists!"
        print(t)
        return t

    f = open(fpath)
    t = f.read()
    return t







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


    # Se nessun valore e' > 0 ... qualcosa non va
    qulcs_non_va = True
    for key in keys:
        qulcs_non_va = qulcs_non_va and (values[key] == 0)
    if qulcs_non_va:
        print("ERROR! Qualcosa non va... Values tutti == 0")

    # Verifico che ci sia almeno un malato
    # Se non c'e' allora converto uno degli altri in malato
    if values['M'] == 0:
        key = keys[randint(0,len(keys)-1)]
        while not values[key] > 0:
            key = keys[randint(0,len(keys)-1)]
        if values[key] > 0:
            values[key] -=1
            values['M'] +=1
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
        K_min=1,H_min=2,
        dest_dir = INPUT_DIR, input_prefix=INPUT_PREFIX,
        input_extension=INPUT_EXT):

    os.makedirs(dest_dir, exist_ok=True)

    num=0 # numero istanza corrente
    for k in range(K_max,K_max+1):
        for h in range(H_min, H_max+1):
            values = {'K':k,'H':h,'M':0,'P':0,'O':0,'Q':0}
            for i in range(n):
                ist = istanza_casuale(values)

                fpath = gen_fpath(num, dest_dir,
                        input_prefix, input_extension)
                write_dzn(ist,fpath)

                num += 1
    print("Generati %d input nella cartella %s" %(num, dest_dir))

# Elimina la cartella degli input
def del_inputs(input_dir = INPUT_DIR):
    #TODO try catch?
    shutil.rmtree(input_dir, ignore_errors=True)

# Elimina la cartella degli outpus
def del_outputs(output_dir = OUTPUT_DIR):
    #TODO try catch?
    shutil.rmtree(output_dir, ignore_errors=True)


##################################################
# Minizinc Models and Intances Stuff
##################################################

# Dati instanza e numero dell'input recupera dzn relativo
# a num e lo carica nell'istanza
def initialize_instance(instance, num, dest_dir=INPUT_DIR):
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
def get_sol(solution,instance, show=False):
    if solution == None:
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

    if show:
        show_sol(sol)
    return sol

# Date le statistics torna il dizionario stats
def get_stats(statistics):
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

    return stats

def show_sol(sol):
    if sol == None:
        print("No solution")
        return
    if type(sol) != dict:
        print("ERROR! In show_sol solution deve essere dict")
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

def to_string_sol(sol):
    if sol == None:
        t = "No solution"
        print(t)
        return t
    if type(sol) != dict:
        t = "ERROR! In show_sol solution deve essere dict"
        print(t)
        return t


    t = ""

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

            t += code + e
            s+=1
        t += '\n'
    return t

def show_objective(obj):
    if obj is None:
        print('{:10}:{:>10}'.format('objective', 'None'))
    else:
        print('{:10}:{:10d}'.format('objective',obj))

def get_objective(obj):
    if obj is None:
        return str('{:10}:{:>10}'.format('objective', 'None'))
    else:
        return str('{:10}:{:10d}'.format('objective',obj))

def show_statistic(statistics):
    # TODO fix se statistics non e stats
    if not type(statistics) == dict:
        stats = get_stats(statistics)
    else:
        stats = statistics

    for k in stats.keys():
        val = stats[k]
        if type(val) == str:
            print("{:10}:{:>10}".format(k, stats[k]))
        elif type(val) == float:
            print("{:10}:{:10f}".format(k, stats[k]))
        elif type(val) == int:
            print("{:10}:{:10d}".format(k, stats[k]))
        elif type(val) == None:
            print("None")
        else:
            print("ERROR! in show_statistic %s tipo chiave imprevisto!" %(str(type(val))))

def to_string_statistic(statistics):
    # TODO fix se statistics non e stats
    if not type(statistics) == dict:
        stats = get_stats(statistics)
    else:
        stats = statistics
    t = ""
    for k in stats.keys():
        val = stats[k]
        if type(val) == str:
            t += str("{:10}:{:>10}".format(k, stats[k]))
            t += '\n'
        elif type(val) == float:
            t += str("{:10}:{:10f}".format(k, stats[k]))
            t += '\n'
        elif type(val) == int:
            t += str("{:10}:{:10d}".format(k, stats[k]))
            t += '\n'
        else:
            t += str("error! in to_string_statistic tipo chiave imprevisto!")
            t += '\n'
    return t


# Dati result ed instance stampa il recap della soluzione trovata
def show_result(result, instance):
    show_statistic(result.statistics)
    show_objective(result.objective)
    print()
    get_sol(result.solution, instance, show=True)

# Dati result, instance ed un file path salva il
# dizionario relativo nel path
def write_output(result, instance, fpath):
    stats = get_stats(result.statistics)
    obj = result.objective
    sol = get_sol(result.solution, instance)

    data = {}
    data['obj'] = obj
    data['stats'] = stats
    data['sol'] = sol

    # TODO try catch
    json.dump(data, open(fpath, 'w+'), indent=True)

# Dati il numero e la dir carica ritorna il dizionario
# della soluzione relativa all input col numero dato
# Se il file non esiste retun None
def read_output(num, directory=OUTPUT_DIR, suppress_error=False):
    if not directory[-1] == '/':
        directory = directory + '/'
    fpath = gen_fpath(num, directory, OUTPUT_PREFIX, OUTPUT_EXT)
    if not os.path.isfile(fpath):
        if not suppress_error:
            print("File does not exist!\n path: %s " %(fpath))
        return None

    return json.load(open(fpath))


def get_output(num, directory=OUTPUT_DIR):
    data = read_output(num, directory)
    output = ""

    output += str(to_string_statistic(data['stats']))
    output += str(get_objective(data['obj']))
    output += '\n\n'

    output += str(to_string_sol(data['sol']))
    output += '\n'
    return output

def show_output(num, directory=OUTPUT_DIR):
    data = read_output(num, directory)
    print(data)
    print()
    show_statistic(data['stats'])
    show_objective(data['obj'])
    print()
    show_sol(data['sol'])
    print()

def dir_exists(directory, label="dir", verbose=True):
    b = os.path.exists(directory)
    if ((not b) and verbose):
        print("ERRORE! La %s %s non esiste!" %(label, input_dir))
    return b


# Carica il modello del path dato e lo esegue sull'input del num dato
def run_on_input(model_path, input_num, input_dir=INPUT_DIR):
    if not dir_exists(input_dir, label='input_dir', verbose=True):
        return
    # TODO try catch
    model = Model(model_path)
    gecode = Solver.lookup("gecode")

    instance = Instance(gecode, model)
    initialize_instance(instance, input_num)
    result = instance.solve()

    show_result(result, instance)



# Carica il modello del path dato e lo esegue su tutti gli input
# per ciascuno salva un json nella cartella data
def run_on_all_inputs(model_path, output_dir, input_dir=INPUT_DIR):
    if not dir_exists(input_dir, label='input_dir', verbose=True):
        return

    if not output_dir[-1] == '/':
        output_dir += '/'
    os.makedirs(output_dir, exist_ok=True)

    model = Model(model_path)
    gecode = Solver.lookup("gecode")

    input_num = 0
    while not get_input(input_num) is None:
        # Se l'output e' gia' stato calcolato non ricalcolo
        if read_output(input_num,suppress_error=True) == None:
            print("Lavoro su input num %d" %(input_num))
            instance = Instance(gecode, model)
            initialize_instance(instance, input_num)
            result = instance.solve()

            output_fpath = gen_fpath(input_num, output_dir,
                    OUTPUT_PREFIX, OUTPUT_EXT)

            write_output(result, instance, output_fpath)
        else:
            print("Trovato output per input num %d. Skip" %(input_num))

        input_num += 1


def run_minizinc_model(num=-1, show_output=True):
    model_path= './covid19.mzn'
    out_dir='./outputs/'
    in_dir='./inputs/'

    if num <= -1:
        print("Running:\nmodel_path=%s\noutput_dir=%s\ninput_dir=%s"\
                %(model_path,out_dir,in_dir))

        run_on_all_inputs(model_path, out_dir, in_dir)
    else:
        print("Running:\nmodel_path=%s\nOn input num=%d" \
                %(model_path,num))
        run_on_input(model_path, num, in_dir)



##################################################
# Main
##################################################
def main():
    print("Main non ancora implementato")
    print("Probabilmente fara' dei test")
    #run_minizinc_model()

if __name__ == "__main__":
    main()
