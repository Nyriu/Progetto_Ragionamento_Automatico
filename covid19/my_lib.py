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
from my_globals import *


class IOHelper:
    """ Classe statica ausiliaria per gestire meglio la generazione/distruzione
        di cartelle o file """

    # On strings ####################
    def correct_dir_path(dir_path):
        """ Aggiunge in fondo a dir_path se necessario """
        if not dir_path[-1] == '/':
            return dir_path + '/'
        else:
            return dir_path

    def gen_fpath(num, dir_path, prefix, suffix):
        """ Dato numero, suffiso e prefisso torna la stringa del path formato da
            dir_path + prefix + numero con due cifre + suffix """
        #num = int(num)

        dir_path = IOHelper.correct_dir_path(dir_path)
        fpath = dir_path + prefix
        fpath += '{:02d}'.format(num)
        fpath += suffix
        return fpath


    # On files ####################
    def open_file(fpath, mode='r'):
        # TODO try catch
        f = open(fpath, mode)
        return f

    # On dirs ####################
    def create_dir(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    def del_dir(target_dir):
        shutil.rmtree(target_dir, ignore_errors=True)


class MyInstance:

    def __init__(self, k,h, m=0,p=0,o=0,q=0):
        #self.values = {'K':None,'H':None,'M':None,'P':None,'O':None,'Q':None}
        self.values = { 'K':k,'H':h,'M':m,'P':p,'O':o,'Q':q }
        self.fpath = None

    """
    #def __init__(self, values):
    #    assert(type(values) == dict)
    #    for key in values.keys():
    #        self.values[key] = values[key]
    """

    def capienza_max(self):
        """ Ritorna il massimo numero di persone sistemabili nelle stanze
            Ipotizzo di poter mettere 2 persone per stanza """
        assert(self.values['K']>0 and self.values['H']>0)
        return 2*self.values['H']*self.values['K']*2

    def numero_stanze(self):
        """ Ritorna il numero di stanze """
        assert(self.values['K']>0 and self.values['H']>0)
        return 2*self.values['H']*self.values['K']

    def stanze_necessarie(self):
        """ Ritorna il numero di stanze minimo
            per ospitare le persone """
        assert(self.values['M']>=0 and self.values['P']>=0 and
               self.values['O']>=0 and self.values['Q']>=0)
        return ceil(self.values['M']/2) +\
               ceil(self.values['P']/2) +\
               self.values['O']         +\
               ceil(self.values['Q']/2)

    def write_dzn(self, fpath):
        """ Scrive l'istanza in formato dzn nel path dato """
        assert(self.values['K']>0  and self.values['H']>0  and
               self.values['M']>=0 and self.values['P']>=0 and
               self.values['O']>=0 and self.values['Q']>=0)
        self.fpath=fpath

        f = IOHelper.open_file(fpath, 'w+')
        for k in self.values.keys():
            text = str(k) +  "=" + str(self.values[k]) + ";\n"
            f.write(text)

    def write_lp(self, fpath):
        """ Scrive l'istanza in formato lp nel path dato """
        raise Exception("Not implemented")


    # Getter e Setter ####################
    def get_corridoi(self):
        assert(self.values['K']>0)
        return self.values['K']
    def get_stanze_per_lato(self):
        assert(self.values['H']>0)
        return self.values['H']
    def get_malati(self):
        assert(self.values['M']>=0)
        return self.values['M']
    def get_positivi(self):
        assert(self.values['P']>=0)
        return self.values['P']
    def get_osservazione(self):
        assert(self.values['O']>=0)
        return self.values['O']
    def get_quarantena(self):
        assert(self.values['Q']>=0)
        return self.values['Q']
    def get_path(self):
        return self.fpath

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


    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return str(self.values)

    # Metodi statici ####################
    def read(fpath):
        """ Ritorna MyIstance leggendo il file al path indicato """
        #TODO qua gestire in automatico i due formati
        #TODO warning se e' mal formato
        if not os.path.isfile(fpath):
            raise Exception("File does not exist!")
            return None

        f = IOHelper.open_file(fpath, 'r')

        comment_char = '%'
        values = {'K':0,'H':0,'M':0,'P':0,'O':0,'Q':0}

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

        ins = MyInstance( k=values['K'], h=values['H'], m=values['M'],
                          p=values['P'], o=values['O'], q=values['Q'])
        ins.fpath=fpath
        return ins


class MySolution():
    """ Rappresenta la soluzione ad un istanza del problema
        Viene salvata come json con formato unico
        Un campo apposito permette di capire se la soluzione e' stata
        ottenuta con modello mzn o lp """

    # TODO gestire il timeout

    #def __init__(model_output):
    #    """ Inizializza MySolution a partire dall'output
    #        di un modello mzn o lp """
    #    # TODO if da mzn fai una roba
    #    # TODO elif da lp fanne un'altra
    #    # TODO else esplodi
    def __init__(self):
        """ Inizializza una MySolution vuota """
        self.model_type = "" # can be "MZN" or "LP"
        self.sat        = False
        self.obj        = -1
        self.solveTime  = -1.0
        self.time       = -1.0
        #self.sols_num   = 0
        self.solution   = {"K":0,"H":0, "M":[],"P":[],"O":[],"Q":[]}


    def write(self, fpath):
        """ Scrive la soluzione in formato json nel path dato """
        data = {}
        data["model_type"] =self.model_type
        data["sat"]        =self.sat
        data["obj"]        =self.obj
        data["solveTime"]  =self.solveTime
        data["time"]       =self.time
        data["sol"]        = self.solution

        # TODO try catch
        json.dump(data, open(fpath, 'w+'), indent=True)


    def _get_symbol(self, s):
        """ Dato un numero di una stanza ritorna il simbolo corretto """
        if (self.solution['M'].count(s) == 1):
            symb = SYMBOLS['malato']
        elif (self.solution['M'].count(s) == 2):
            symb = SYMBOLS['malati']

        elif (self.solution['P'].count(s) == 1):
            symb = SYMBOLS['positivo']
        elif (self.solution['P'].count(s) == 2):
            symb = SYMBOLS['positivi']

        elif (self.solution['O'].count(s) == 1):
            symb = SYMBOLS['osservazione']

        elif (self.solution['Q'].count(s) == 1):
            symb = SYMBOLS['quarantena']
        elif (self.solution['Q'].count(s) == 2):
            symb = SYMBOLS['quaranteni']
        else:
            symb = SYMBOLS['empty']
        return symb;

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        if self.sat == False:
            t = "No solution"
            return t
        t = ""

        K = self.solution['K']
        H = self.solution['H']
        s = 0
        for k in range(K):
            for h in range(2*H):
                code = self._get_symbol(s)
                e = " "
                if (h==H-1 or h==2*H-1 or h==2*H*K-1):
                    e = "\n"
                if (h==H-1):
                    code += "\t" + str(k)

                t += code + e
                s+=1
            t += '\n'
        return t

    # Metodi statici ####################
    def read(fpath):
        """ Ritorna MySolution del path indicato """

    def from_mzn(res,ins):
        """ Presa una soluzione e relativa istanza di un modello mzn ritorna
            la MySolution equivalente """
        msol = MySolution()
        sol = res.solution
        if sol is None: # TODO check if UNSAT
            msol.model_type = "MZN"
            msol.sat = False
            msol.solution = None
            return msol
        # else
        msol.model_type = "MZN"
        msol.sat = True
        msol.obj = int(res.objective)
        msol.time = float(res.statistics['time'].total_seconds())
        msol.solveTime = float(res.statistics['solveTime'].total_seconds())
        #msol.sols_num = int(res.statistics['solutions'])

        msol.solution['K'] = ins['K']
        msol.solution['H'] = ins['H']

        msol.solution['M'] = sol.malati
        msol.solution['P'] = sol.positivi
        msol.solution['O'] = sol.osservazione
        msol.solution['Q'] = sol.quarantena
        return msol



class InputGenerator:

    def satura_stanze(ins):
        """ Modifica lo stato della MyInstance aggiungendo casualmente persone
            fino a riempire tutte le stanze disponibili """
        assert(ins.stanze_necessarie() <= ins.numero_stanze())

        getters = [
                ins.get_malati,
                ins.get_positivi,
                ins.get_osservazione,
                ins.get_quarantena
                ]
        setters = [
                ins.set_malati,
                ins.set_positivi,
                ins.set_osservazione,
                ins.set_quarantena
                ]
        while ins.stanze_necessarie() <= ins.numero_stanze():
            num = randint(0,len(getters)-1)
            g,s = list(zip(getters,setters))[num]
            val = g()
            s(val+1)
            last_num = num

        val = getters[last_num]()
        setters[last_num](val-1)
        # Se ho valori dispari significa che ho una sola persona
        # dove potrebbero essercene due (da escludere quelli in osservazione)
        getters.remove(ins.get_osservazione)
        setters.remove(ins.set_osservazione)
        for g,s in list(zip(getters,setters)):
            val = g()
            if val%2 == 1:
                s(val+1)

        assert(ins.stanze_necessarie() <= ins.numero_stanze())


    def gen_istanza_casuale(k,h):
        """ Torna un'istanza casuale per k e h dati """
        ins = MyInstance(k,h)
        InputGenerator.satura_stanze(ins)

        getters = [
                ins.get_malati,
                ins.get_positivi,
                ins.get_osservazione,
                ins.get_quarantena
                ]
        setters = [
                ins.set_malati,
                ins.set_positivi,
                ins.set_osservazione,
                ins.set_quarantena
                ]

        if randint(0,2) != 2: # due volte su tre
            # rimuovo al piu' 1/4 di persone a caso
            n_rimuovere = randint(1, ins.capienza_max()//4)
            rimosse=0
            while rimosse != n_rimuovere:
                num = randint(0,len(getters)-1)
                da_rimuovere = randint(1,n_rimuovere-rimosse)
                g,s = list(zip(getters,setters))[num]
                val = g()
                if val >= da_rimuovere:
                    s(val-da_rimuovere)
                    rimosse += da_rimuovere
        else: # TODO verificare se possibile fare altre modifiche
            # dimezzo Malati, Positivi o Quarantena
            getters.remove(ins.get_osservazione)
            setters.remove(ins.set_osservazione)

            num = randint(0,len(getters)-1)
            g,s = list(zip(getters,setters))[num]
            val = g()

            s(val//2 + val%2) #mantengo dispari se era disp


        # Verifico che ci sia almeno un malato
        getters.append(ins.get_osservazione)
        setters.append(ins.set_osservazione)
        getters.remove(ins.get_malati)
        setters.remove(ins.set_malati)
        if ins.get_malati() == 0:
            # Converto un ospite in malato
            while not ins.get_malati() > 0:
                num = randint(0,len(getters)-1)
                g,s = list(zip(getters,setters))[num]
                val = g()
                if val > 0:
                    s(val-1)
                    ins.set_malati(ins.get_malati()+1)
            # Se ora le stanze non sono sufficienti, continuo a convertire
            while not (ins.stanze_necessarie() <= ins.numero_stanze()):
                num = randint(0,len(getters)-1)
                g,s = list(zip(getters,setters))[num]
                val = g()
                if val > 0:
                    s(val-1)
                    ins.set_malati(ins.get_malati()+1)


        assert(ins.get_malati() > 0)
        assert(ins.stanze_necessarie() <= ins.numero_stanze())
        return ins


    def gen_istanze(n, k_min,h_min, k_max,h_max,
            order=None, delete_old=False, write=False):

        """ Ritorna n istanze causali con k e h nei range(*_min,*_max)
            se write=True le salva nei formati .dzn e .lp nelle cartelle
            INPUT_MZN_DIR INPUT_LP_DIR rispettivamente
            Se delete_old=True allora svuota le cartelle prima di generare
            """
        # Dente di sega
        inss = InputGenerator._gen_istanze(n, k_min,h_min, k_max,h_max)
        # TODO order

        if delete_old:
            IOHelper.del_dir(INPUT_MZN_DIR)
            IOHelper.del_dir(INPUT_LP_DIR)

        if write:
            IOHelper.create_dir(INPUT_MZN_DIR)
            IOHelper.create_dir(INPUT_LP_DIR) # TODO
            for i,ins in enumerate(inss):
                fpath = IOHelper.gen_fpath(i,
                        INPUT_MZN_DIR, INPUT_MZN_PREFIX, INPUT_MZN_EXT)
                ins.write_dzn(fpath)

                # TODO
                #fpath = IOHelper.gen_fpath(i,
                #        INPUT_LP_DIR, INPUT_LP_PREFIX, INPUT_LP_EXT)
                #ins.write_lp(fpath)

        return inss



    def _gen_istanze(n, k_min,h_min, k_max,h_max):
        """ Torna una lista di n istanze casuali con
            k in range(k_min,k_max) e h in range(h_min,h_max) """
        inss = []
        for i in range(n):
            for k in range(k_min,k_max):
                for h in range(h_min,h_max):
                    inss.append(InputGenerator.gen_istanza_casuale(k,h))
        return inss




class BatchCoordinator: # TODO
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
    """ Con run si puo' eseguire il modello indicato su tutte le istanze oppure
        su un'istanza specifica
        Si puo' specificare se mostrare la soluzione, salvarla o entrambi """

    def __init__(self, model_path):
        self.model_path=model_path
        self.model=None
        self.load_model(model_path)

        self.input_dir    = None
        self.input_prefix = None
        self.input_ext    = None

        self.output_dir    = None
        self.output_prefix = None
        self.output_ext    = None



    def load_model(self, model_path=None):
        """ Carica modello del path indicato, se non viene specificato
            usa il campo self.model_path """

    #@abstractmethod
    def add_instance(self, fpath):
        """ Aggiunge l'istanza al modello """



    #@abstractmethod
    def run(self, instance_num, show=True, save=False):
        """ Esegue il modello sull'istanza corrispondente al numero dato """
        if not self.runnable():
            raise Exception("Model unrunnable!")

    #@abstractmethod
    def runs(self, myIns, show=True):
        """ Esegue il modello sulla MyInstance data """
        if not self.runnable():
            raise Exception("Model unrunnable!")

    #@abstractmethod
    def runnable(self):
        """ Ritorna True se il modello puo' essere eseguito """
        return(not self.model         is None and
               not self.input_dir     is None and
               not self.input_prefix  is None and
               not self.input_ext     is None and
               not self.output_dir    is None and
               not self.output_prefix is None and
               not self.output_ext    is None)


class RunnerMzn(AbstractRunner):
    """ Permette di eseguire un modello mzn su tutte le istanze oppure
        su un'istanza specificata dal numero """
    def __init__(self, model_path, solver_name="gecode"):
        self.model_path=model_path
        self.solver_name=solver_name
        self.model=None
        self.solver=None

        self.load_model(model_path)
        self.load_solver(solver_name)

        self.input_dir    = INPUT_MZN_DIR
        self.input_prefix = INPUT_MZN_PREFIX
        self.input_ext    = INPUT_MZN_EXT

        self.output_dir    = OUTPUT_MZN_DIR
        self.output_prefix = OUTPUT_MZN_PREFIX
        self.output_ext    = OUTPUT_MZN_EXT


    def load_model(self, model_path=None):
        """ Carica modello del path indicato, se non viene specificato
            usa il campo self.model_path """
        if self.solver_name is None:
            self.model = Model(self.model_path)
        else:
            self.model = Model(model_path)
            self.model_path = model_path

    def load_solver(self, solver_name=None):
        """ Carica il solver indicato, se non viene specificato
            usa il campo self.solver_name """
        if solver_name is None:
            self.solver = Solver.lookup(self.solver_name)
        else:
            self.solver = Solver.lookup(solver_name)
            self.solver_name = solver_name


    def run(self, instance_num, show=True, save=False):
        """ Esegue il modello sull'istanza corrispondente al numero dato """
        assert(type(instance_num) == int)
        super().run(instance_num,show,save)
        fpath = IOHelper.gen_fpath(instance_num, self.input_dir,
                                   self.input_prefix, self.input_ext)
        myIns = MyInstance.read(fpath)
        return self.runs(myIns,show)

    def runs(self, myIns, show=True):
        """ Esegue il modello sulla MyInstance data """
        assert(type(myIns) == MyInstance)
        super().runs(myIns,show,save)
        fpath = myIns.get_path()
        instance = self.initialize_instance(myIns)
        result = instance.solve()

        msol = MySolution.from_mzn(result,instance)
        if show:
            print(fpath)
            print(msol)
        return msol


    def runnable(self):
        return( super().runnable()         and
                not self.solver    is None)

    def initialize_instance(self, myIns):
        """ Data una MyInstance ritorna una Instance equivalente """
        assert(not self.model is None)
        assert(not self.solver is None)

        if myIns is None:
            raise Exception("myIns is None")

        instance = Instance(self.solver, self.model)
        instance["K"]= myIns.get_corridoi()
        instance["H"]= myIns.get_stanze_per_lato()

        instance["M"]= myIns.get_malati()
        instance["P"]= myIns.get_positivi()
        instance["O"]= myIns.get_osservazione()
        instance["Q"]= myIns.get_quarantena()
        return instance


class RunnerLp(AbstractRunner):
    """ Permette di eseguire un modello lp su tutte le istanze oppure
        su un'istanza specificata dal numero """
    def load_model(self, model_path=None):
        self.model="lp"

    def run(self, instance_num=None, show=False, save=True):
        #TODO
        pass
