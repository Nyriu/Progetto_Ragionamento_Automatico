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

    def correct_dir_path(dir_path):
        """ Aggiunge in fondo a dir_path se necessario """
        if not dir_path[-1] == '/':
            return dir_path + '/'
        else:
            return dir_path

    def gen_fpath(num, dir_path, prefix, suffix):
        """ Dato numero, suffiso e prefisso torna la stringa del path formato da
            dir_path + prefix + numero con due cifre + suffix """
        dir_path = IOHelper.correct_dir_path(dir_path)
        fpath = dir_path + prefix
        fpath += '{:02d}'.format(num)
        fpath += suffix
        return fpath

    def open_file(fpath, mode='r'):
        # TODO try catch
        f = open(fpath, mode)
        return f



class MyInstance:

    def __init__(self, k=None,h=None, m=None,p=None,o=None,q=None):
        #self.values = {'K':None,'H':None,'M':None,'P':None,'O':None,'Q':None}
        self.values = { 'K':k,'H':h,'M':m,'P':p,'O':o,'Q':q }

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

        f = IOHelper.open_file(fpath, 'w+')
        for k in self.values.keys():
            text = str(k) +  "=" + str(self.values[k]) + ";\n"
            f.write(text)

    def write_lp(self, fpath):
        """ Scrive l'istanza in formato lp nel path dato """
        raise "Not implemented"


    # Getter e Setter ####################
    def get_corridoi(self):
        assert(self.values['K']>0)
        return self.values['K']
    def get_stanze_per_lato(self,h):
        assert(self.values['H']>0)
        return self.values['H']
    def get_malati(self):
        assert(self.values['M']>0)
        return self.values['M']
    def get_positivi(self):
        assert(self.values['P']>0)
        return self.values['P']
    def get_osservazione(self):
        assert(self.values['O']>0)
        return self.values['O']
    def get_quarantena(self):
        assert(self.values['Q']>0)
        return self.values['Q']

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
         # TODO qua gestire in automatico i due formati

        if not os.path.isfile(fpath):
            return None

        f = IOHelper.open_file(fpath, 'w+')

        comment_char = '%'
        values = {'K':None,'H':None,'M':None,'P':None,'O':None,'Q':None}

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

        ins = MyInstance( k=values['K'], h=values['H'], m=values['M'],
                          p=values['P'], o=values['O'], q=values['Q'])
        return ins


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
        #@abstractmethod
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
    """ Con run si puo' eseguire il modello indicato su tutte le istanze oppure
        su un'istanza specifica
        Si puo' specificare se mostrare la soluzione, salvarla o entrambi """

    #@abstractmethod
    def run(self, instance_num=None, show=False, save=True):
        """ Esegue il modello su tutte le istanze oppure solo quella del numero
            corrispondente
            Se il numero non viene specificato il modello viene eseguito su tutte
            le istanze """
    #    # Devo verificare che sia inizzializzato
    #    if not (got_model() and got_instance()):
    #        #TODO
    #        print("ERRORE")

    #def got_model(self):
    #    """ Return True se il modello e' stato inizializzato correttamente """
    #def got_instance(self):
    #    """ Return True se l'istanza e' stato inizializzato correttamente """


class RunnerMzn(AbstractRunner):
    """ Permette di eseguire un modello mzn su tutte le istanze oppure su un'istanza specificata dal numero """
    def run(self, instance_num=None, show=False, save=True):
        #TODO
        pass

class RunnerLp(AbstractRunner):
    """ Permette di eseguire un modello lp su tutte le istanze oppure su un'istanza specificata dal numero """
    def run(self, instance_num=None, show=False, save=True):
        #TODO
        pass
