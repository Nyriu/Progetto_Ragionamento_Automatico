##################################################
# Import
##################################################
# Varie
import os, shutil
import re
import json

#import asyncio ## Sperando funzioni per il timeout di clingo... NOPE!
#import threading ## Sperando funzioni per il timeout di clingo... NOPE!
import multiprocessing ## Sperando funzioni per il timeout di clingo... # Workaround ma YES

import time
from math import ceil

# Per Random
from datetime import datetime
from random import randint
import random
random.seed(datetime.now())

# Modelli
from minizinc import Instance, Model, Solver
import clingo


# Le mie globali
from my_globals import *

##DEBUG = True
#import psutil
#import objgraph


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

    def to_str_dzn(self):
        """ Ritorna la stringa dell'istanza in formato dzn """
        assert(self.values['K']>0  and self.values['H']>0  and
               self.values['M']>=0 and self.values['P']>=0 and
               self.values['O']>=0 and self.values['Q']>=0)
        text = ""
        for k in self.values.keys():
            text += str(k) +  "=" + str(self.values[k]) + ";\n"
        return text

    def to_str_lp(self):
        """ Ritorna la strina dell'istanza in formato lp """
        assert(self.values['K']>0  and self.values['H']>0  and
               self.values['M']>=0 and self.values['P']>=0 and
               self.values['O']>=0 and self.values['Q']>=0)

        dzn_ids_to_lp = {
                "K":"corridoi(       ",
                "H":"stanze_per_lato(",
                "M":"soggetto(",
                "P":"soggetto(",
                "O":"soggetto(",
                "Q":"soggetto("
                }
        lp_type_encode = {
                "M":"0",
                "P":"1",
                "O":"2",
                "Q":"3"
                }

        p_num = 1 # numero identificativo persona

        lp_enc = ""
        for k in self.values.keys():
            if self.values[k] != 0:
                lp_enc += dzn_ids_to_lp[k]
                val = self.values[k]
                if not (k == "K" or k == "H"):
                    lp_enc += str(p_num) + ".."
                    p_num += val - 1
                    lp_enc += str(p_num) + ", " + lp_type_encode[k]
                    p_num += 1
                else:
                    lp_enc += str(val)
                lp_enc += ").\n"
        return lp_enc


    def to_str_lp_old(self):
        """ DEPRECATED! Ritorna la strina dell'istanza in formato lp """
        assert(self.values['K']>0  and self.values['H']>0  and
               self.values['M']>=0 and self.values['P']>=0 and
               self.values['O']>=0 and self.values['Q']>=0)
        dzn_ids_to_lp = {
                "K":"corridoi(       ",
                "H":"stanze_per_lato(",
                "M":"malato(1..      ",
                "O":"osservazione(1..",
                "P":"positivo(1..    ",
                "Q":"quarantena(1..  "
                }

        lp_enc = ""
        for k in self.values.keys():
            if self.values[k] != 0:
                lp_enc += dzn_ids_to_lp[k]
                lp_enc += str(self.values[k])
                lp_enc += ").\n"
        return lp_enc

    def write_dzn(self, fpath):
        """ Scrive l'istanza in formato dzn nel path dato """
        assert(self.values['K']>0  and self.values['H']>0  and
               self.values['M']>=0 and self.values['P']>=0 and
               self.values['O']>=0 and self.values['Q']>=0)
        self.fpath=fpath
        f = IOHelper.open_file(fpath, 'w+')
        dzn_enc = self.to_str_dzn()
        f.write(dzn_enc)

    def write_lp(self, fpath):
        """ Scrive l'istanza in formato lp nel path dato """
        assert(self.values['K']>0  and self.values['H']>0  and
               self.values['M']>=0 and self.values['P']>=0 and
               self.values['O']>=0 and self.values['Q']>=0)
        self.fpath=fpath
        f = IOHelper.open_file(fpath, 'w+')
        lp_enc = self.to_str_lp()
        f.write(lp_enc)

    def calc_complexity(self, alpha=.5):
        K = self.values['K']
        H = self.values['H']
        M = self.values['M']
        P = self.values['P']
        O = self.values['O']
        Q = self.values['Q']
        pers = M+P+O+Q
        pers_mezzi = M/2+P/2+O+Q/2
        stanze = 2*K*H

        if stanze < 12:
            return 0

        return alpha*pers_mezzi/stanze + (1-alpha)*(M+P+Q)/pers


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
        if not os.path.isfile(fpath):
            raise Exception("File "+ fpath +" does not exist!")
            return None

        f = IOHelper.open_file(fpath, 'r')

        if INPUT_MZN_EXT in fpath:
            values = MyInstance._read_mzn(f)
        elif INPUT_LP_EXT in fpath:
            values = MyInstance._read_lp(f)
        else:
            raise Exception("File neither .mzn or .lp!")
        ins = MyInstance( k=values['K'], h=values['H'], m=values['M'],
                          p=values['P'], o=values['O'], q=values['Q'])
        ins.fpath=fpath
        return ins

    def _read_mzn(f):
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
                    values[k] = int(v)
        return values

    def _read_lp(f):
        # Not implemented
        # Al momento leggo mzn e lo passo al RunnerLp come MyInstance
        # quindi non serve leggere direttamente i .lp
        raise Exception("_rea_lp not implemented!")




class MySolution():
    """ Rappresenta la soluzione ad un istanza del problema
        Viene salvata come json con formato unico
        Un campo apposito permette di capire se la soluzione e' stata
        ottenuta con modello mzn o lp """

    def __init__(self):
        """ Inizializza una MySolution vuota """
        self.model_type = "" # can be "MZN" or "LP"
        self.sat        = False
        self.timeouted  = False
        self.obj        = -1
        self.solveTime  = -1.0
        self.time       = -1.0
        #self.sols_num   = 0
        self.solution   = {"K":0,"H":0, "M":[],"P":[],"O":[],"Q":[]}


    def write(self, fpath):
        """ Scrive la soluzione in formato json nel path dato """
        data = {}
        data["model_type"] = self.model_type
        data["sat"]        = self.sat
        data["timeouted"]  = self.timeouted
        data["obj"]        = self.obj
        data["solveTime"]  = self.solveTime
        data["time"]       = self.time
        data["sol"]        = self.solution

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
        elif (self.solution['O'].count(s) == 2):
            symb = SYMBOLS['osservazioni']

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
            t = ""
            t += "model_type " + "= " + str(self.model_type) + "\n"
            t += "No solution"
            if (self.timeouted):
                t += " (TIMEOUT)" + "\n"
            else:
                t += " (UNSAT)" + "\n"
            #t += "solveTime  " + "=" + "{:10f}".format(self.solveTime) + "\n"
            #t += "time       " + "=" + "{:10f}".format(self.time) + "\n"
            t += 2*"\n"
            return t

        t = ""
        t += "model_type " + "=" + "{:>10s}".format(self.model_type) + "\n"
        t += "sat        " + "=" + "{:10d}".format(self.sat) + "\n"
        t += "timeouted  " + "=" + "{:10d}".format(self.timeouted) + "\n"
        t += "obj        " + "=" + "{:10d}".format(self.obj) + "\n"

        t += "solveTime  " + "=" + "{:10f}".format(self.solveTime) + "\n"
        t += "time       " + "=" + "{:10f}".format(self.time) + "\n"
        t += 2*"\n"


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
        msol = MySolution()
        data = json.load(open(fpath))

        msol.model_type = data["model_type"]
        msol.sat        = data["sat"]
        msol.timeouted  = data["timeouted"]
        msol.obj        = data["obj"]
        msol.solveTime  = data["solveTime"]
        msol.time       = data["time"]
        #msol.sols_num   = 0
        msol.solution   = data["sol"]
        return msol

    def from_mzn(res,ins):
        """ Presa una soluzione e relativa istanza di un modello mzn ritorna
            la MySolution equivalente """

        msol = MySolution()
        msol.model_type = "MZN"
        sol = res.solution
        if sol is None:
            msol.sat = False
            msol.solution = None
            msol.timeouted = False
            if ("UNKNOWN" == res.status.name):
                msol.timeouted = True
            return msol
        # else
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

    def from_lp(res_model,ctl):
        """ Preso un modello soluzione e il controller di istanza
            di un modello lp ritorna la MySolution equivalente """
        msol = MySolution()
        msol.model_type = "LP"

        if res_model is None: # Il modello e' UNSAT
            msol.sat = False
            msol.solution = None
            return msol

        # Lista di coppie (nome, len(args)) dei predicati e
        # del loro numero di argomenti da usare per la soluzione
        to_consider = [
          ("corridoi",1),
          ("stanze_per_lato",1),

          ("in_stanza",      3),
        ]

        sol = {
          "K":0,
          "H":0,

          "M":[],
          "P":[],
          "O":[],
          "Q":[]
        }

        type_num_to_letter = {
          0:"M",
          1:"P",
          2:"O",
          3:"Q"
        }

        for symb in res_model:
            name = symb.name
            args = symb.arguments
            if (name, len(args)) in to_consider:
                if name == "corridoi":
                    sol["K"]=args[0].number
                elif name == "stanze_per_lato":
                    sol["H"]=args[0].number
                #elif "in_stanza" in name:
                else:
                    #p_id   = args[0].number
                    p_type = type_num_to_letter[args[1].number]
                    s      = args[2].number
                    sol[p_type].append(s)

        statistics=ctl.statistics

        msol.sat = True
        msol.obj = int(statistics["summary"]["costs"][0])

        msol.time = statistics["summary"]["times"]["total"]
        msol.solveTime = statistics["summary"]["times"]["solve"]
        #msol.sols_num = int(res.statistics['solutions'])

        msol.solution['K'] = sol['K']
        msol.solution['H'] = sol['H']

        msol.solution['M'] = sol['M']
        msol.solution['P'] = sol['P']
        msol.solution['O'] = sol['O']
        msol.solution['Q'] = sol['Q']


        return msol

    def from_lp_old(res_model,ctl):
        """ DEPRECATED Preso un modello soluzione e il controller di istanza
            di un modello lp ritorna la MySolution equivalente """
        msol = MySolution()
        msol.model_type = "LP"

        if res_model is None: # Il modello e' UNSAT
            msol.sat = False
            msol.solution = None
            return msol

        # Lista di coppie (nome, len(args)) dei predicati e
        # del loro numero di argomenti da usare per la soluzione
        to_consider = [
          ("corridoi",1),
          ("stanze_per_lato",1),

          ("malato",       2),
          ("positivo",     2),
          ("osservazione", 2),
          ("quarantena",   2)
        ]

        sol = {
          "K":0,
          "H":0,

          "M":[],
          "P":[],
          "O":[],
          "Q":[]
        }

        for symb in res_model:
            name = symb.name
            args = symb.arguments
            if (name, len(args)) in to_consider:
                if name == "corridoi":
                    sol["K"]=args[0].number
                elif name == "stanze_per_lato":
                    sol["H"]=args[0].number
                ## BEGIN DEBUG
                elif "vicini" in name:
                    s1 = args[0].number
                    s2 = args[1].number
                    sol[name].append((s1,s2))
                ## END DEBUG
                else:
                    sol[name[0].upper()].append(args[1].number)

        statistics=ctl.statistics

        msol.sat = True
        msol.obj = int(statistics["summary"]["costs"][0])

        msol.time = statistics["summary"]["times"]["total"]
        msol.solveTime = statistics["summary"]["times"]["solve"]
        #msol.sols_num = int(res.statistics['solutions'])

        msol.solution['K'] = sol['K']
        msol.solution['H'] = sol['H']

        msol.solution['M'] = sol['M']
        msol.solution['P'] = sol['P']
        msol.solution['O'] = sol['O']
        msol.solution['Q'] = sol['Q']
        return msol



    # Metodi debug ####################
    def _debug_vicini1(self):
        v1 = self.solution['vicini1']
        v1.sort()
        old_s1 = v1[0][0]
        for s in v1:
            s1 = s[0]
            if s1 != old_s1:
                print(5*"-")
                old_s1 = s1
            print(s)

    def _debug_vicini2(self):
        v2 = self.solution['vicini2']
        v2.sort()
        old_s1 = v2[0][0]
        for s in v2:
            s1 = s[0]
            if s1 != old_s1:
                print(5*"-")
                old_s1 = s1
            print(s)

    def _debug_s_num(self):
        if self.sat == False:
            t = "No solution"
            return t
        t=""
        K = self.solution['K']
        H = self.solution['H']
        s = 0
        for k in range(K):
            for h in range(2*H):
                #code = self._get_symbol(s)
                code = '{:02d}'.format(s)
                e = " "
                if (h==H-1 or h==2*H-1 or h==2*H*K-1):
                    e = "\n"
                if (h==H-1):
                    code += "\t" + str(k)

                t += code + e
                s+=1
            t += '\n'
        print(t)




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
        else:
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

        if delete_old:
            IOHelper.del_dir(INPUT_MZN_DIR)
            IOHelper.del_dir(INPUT_LP_DIR)

        if write:
            IOHelper.create_dir(INPUT_MZN_DIR)
            IOHelper.create_dir(INPUT_LP_DIR)
            for i,ins in enumerate(inss):
                fpath = IOHelper.gen_fpath(i,
                        INPUT_MZN_DIR, INPUT_MZN_PREFIX, INPUT_MZN_EXT)
                ins.write_dzn(fpath)

                fpath = IOHelper.gen_fpath(i,
                        INPUT_LP_DIR, INPUT_LP_PREFIX, INPUT_LP_EXT)
                ins.write_lp(fpath)

        return inss



    def _gen_istanze(n, k_min,h_min, k_max,h_max):
        """ Torna una lista di n istanze casuali con
            k in range(k_min,k_max) e h in range(h_min,h_max) """
        inss = []
        for k in range(k_min,k_max):
            for h in range(h_min,h_max):
                for i in range(n):
                    inss.append(InputGenerator.gen_istanza_casuale(k,h))
        return inss




class BatchCoordinator:
    """ Un batch e' l'insieme degli elementi che matchano le regex
        contenute in BATCH_COMPONENTS.
        BatchCoordinator si preoccupa salvare un batch correttamente
        """

    def _biggest_batch_num():
        """ Verifica quali batch sono gia' stati creati e ritorna quello
            con il numero piu' grande """

        IOHelper.create_dir(BATCH_ROOT_DIR)
        batches_names = os.listdir(BATCH_ROOT_DIR)

        max_num=0
        for bat in batches_names:
            num = int(bat.replace(BATCH_DIR_PREFIX, ""))
            if num > max_num:
                max_num = num

        return max_num

    def save_as_batch(dir_to_save="./"):
        """ Raccoglie tutte le informazioni relative ad un
            batch all'interno della cartella data e le salva
            come batch in una sottocartella di BATCH_ROOT_DIR """
        dir_to_save=IOHelper.correct_dir_path(dir_to_save)
        IOHelper.create_dir(BATCH_ROOT_DIR)

        batchnum = BatchCoordinator._biggest_batch_num() + 1

        batch_path = BATCH_ROOT_DIR + BATCH_DIR_PREFIX + str(batchnum)
        batch_path = IOHelper.correct_dir_path(batch_path)

        IOHelper.create_dir(batch_path)

        listdir = os.listdir(dir_to_save)

        for name in listdir:
            isdir = os.path.isdir(dir_to_save+name)
            if isdir:
                name = IOHelper.correct_dir_path(name)
            move = False
            for reg in BATCH_COMPONENTS:
                x = re.search(reg, name)
                move = move or (not x is None)
            if move:
                src_path = dir_to_save+name
                dst_path = batch_path+name
                if isdir:
                    shutil.copytree(src_path,dst_path)
                else:
                    shutil.copy(src_path,dst_path)






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



    #@absttractmethod
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
        msol = self.runs(myIns,show)
        if save:
            IOHelper.create_dir(self.output_dir)
            fpath = IOHelper.gen_fpath(instance_num, self.output_dir,
                                   self.output_prefix, self.output_ext)
            msol.write(fpath)

        return msol

    def runs(self, myIns, show=True):
        """ Esegue il modello sulla MyInstance data """
        assert(type(myIns) == MyInstance)
        super().runs(myIns,show)
        fpath = myIns.get_path()
        instance = self.initialize_instance(myIns)

        result = instance.solve(timeout=TIMEOUT)

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
    def __init__(self, model_path, solver_name="gecode"):
        self.model_path=model_path

        self.load_model(model_path)

        self.input_dir    = INPUT_LP_DIR
        self.input_prefix = INPUT_LP_PREFIX
        self.input_ext    = INPUT_LP_EXT

        self.output_dir    = OUTPUT_LP_DIR
        self.output_prefix = OUTPUT_LP_PREFIX
        self.output_ext    = OUTPUT_LP_EXT

    def load_model(self, model_path=None):
        ctl = clingo.Control(message_limit=0)
        #ctl.configuration.configuration = 'tweety'
        ctl.load(model_path)
        self.model=ctl


    def run(self, instance_num, show=True, save=False):
        """ Esegue il modello sull'istanza corrispondente al numero dato """
        assert(type(instance_num) == int)
        super().run(instance_num,show,save)
        fpath = IOHelper.gen_fpath(instance_num, self.input_dir,
                                   self.input_prefix, self.input_ext)

        global dummy_res_model
        dummy_res_model = None
        global dummy_t0
        dummy_t0 = time.time()
        global max_models_to_consider
        max_models_to_consider=0
        def dummy_on_model(m):
            dummy_res_model = m.symbols(shown=True)
            #dummy_t1 = time.time()
            #dummy_delt = dummy_t1 - dummy_t0
            global max_models_to_consider
            max_models_to_consider+=1
            #return dummy_delt < TIMEOUT.total_seconds()
            return True

        ################################################################################
        # LAVORO SU TIMEOUT DEL GROUDING+SOLVE
        ################################################################################
        # Workaround per il timeout
        # + lancio il grounding in un processo secondario
        # + nel processo principale verifico se il secondario ha finito il grounding e
        #   tengo conto del tempo che passa
        # + se il grounding finisce entro il TIMEOUT allora lancio il grounding in locale (nel processo principale)
        # + se ho TIMEOUT allora devo gestire la creazione di una soluzione particolare

        # Pro: funziona, dato che nessuno degli altri metodi funziona
        #      (Control non e' serializzabile quindi niente passaggio tra thread/processi)

        # Cons: alla peggio si rischia di aspettare 2*(TIMEOUT-e) con e piccolo a piacere
        #       si perde eventuale soluzione parziale


        self.load_model(self.model_path)
        ctl=self.model
        ctl.load(fpath)

        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        return_dict[0] = False
        return_dict[1] = 0

        def killable_ground_solution(ctl,return_dict):
            return_dict[0] = False
            ctl.ground([("base", [])])
            ctl.solve(on_model=dummy_on_model)
            return_dict[0] = True
            return_dict[1] = max_models_to_consider

        process = multiprocessing.Process(target=killable_ground_solution, args=(ctl,return_dict))
        process.start()

        time.sleep(1)

        kill_t0 = time.time()
        kill_t1 = time.time()
        solvable_in_time = False
        while (not solvable_in_time) and (kill_t1 - kill_t0 < TIMEOUT.total_seconds()):
            time.sleep(1)
            kill_t1 = time.time()
            solvable_in_time = return_dict[0]
        ################################################################################
        # FINE # LAVORO SU TIMEOUT DEL GROUDING+SOLVE
        ################################################################################

        msol = MySolution()

        solvable_in_time = return_dict[0]
        max_models_to_consider = return_dict[1]
        if (not solvable_in_time) and (max_models_to_consider<2):
            #print("\ndon't even try...")
            msol.model_type = "LP"
            msol.sat        = False
            msol.timeouted  = True
            msol.solution   = None
        else:
            global res_model
            res_model = None
            global models_considered
            models_considered=0

            #print("let's try...")

            def on_model(m):
                global res_model
                res_model = m.symbols(shown=True)
                global max_models_to_consider
                global models_considered
                models_considered+=1
                return models_considered <= max_models_to_consider

            self.load_model(self.model_path)
            ctl=self.model
            ctl.load(fpath)
            ctl.ground([("base", [])])
            ctl.solve(on_model=on_model)
            msol = MySolution.from_lp(res_model,ctl)

        if show:
            print(fpath)
            print(msol)
        if save:
            IOHelper.create_dir(self.output_dir)
            fpath = IOHelper.gen_fpath(instance_num, self.output_dir,
                                   self.output_prefix, self.output_ext)
            msol.write(fpath)

        terminate_process_children()

        # Devo ricaricarlo ogni volta perche' l'ho sporcato con
        # l'istanza in input. ctl non si puo' copiare/clonare...
        self.load_model(self.model_path)
        return msol


    def runs(self, myIns, show=True):
        """ Esegue il modello sulla MyInstance data """
        assert(type(myIns) == MyInstance)
        super().runs(myIns,show)

        myIns.write_lp("tmp.lp")

        ctl=self.model
        ctl.load("tmp.lp")
        ctl.ground([("base", [])])

        res_model = None
        with ctl.solve(on_model=lambda m: print(end=""), yield_=True) as handle:
          for m in handle:
              res_model = m.symbols(atoms=True)

        msol = MySolution.from_lp(res_model,ctl)
        if show:
            print(msol)

        # Devo ricaricarlo ogni volta perche' l'ho sporcato con
        # l'istanza in input. ctl non si pu' copiare/clonare...
        self.load_model(self.model_path)
        return msol



    def runnable(self):
        return( super().runnable() )




### TODO refactor in MySolution ##########################################################
### TODO refactor in MySolution ##########################################################
### TODO refactor in MySolution ##########################################################

def get_output(num, directory=OUTPUT_MZN_DIR):
    fpath = IOHelper.gen_fpath(num, directory, OUTPUT_PREFIX, OUTPUT_EXT)
    data = MySolution.read(fpath)
    # output = ""

    # output += str(to_string_statistic(data['stat']))
    # output += str(get_objective(data['obj']))
    # output += '\n\n'

    # output += str(to_string_sol(data['sol']))
    # output += '\n'

    output = str(data)
    return output



# Dato un numero ritorna il dizionario dell'input relativo
def get_input(num, dest_dir=INPUT_DIR):
    #if num >  100:
    #    print("ERROR! get_input() num troppo grande")
    #    exit(2)
    fpath = IOHelper.gen_fpath(num, dest_dir, INPUT_PREFIX, INPUT_EXT)
    # TODO try catch
    return read_dzn(fpath)

# Dato un numero ritorna il testo dell'input relativo
def get_input_text(num, dest_dir=INPUT_DIR):
    #if num >  100:
    #    t = "ERROR! get_input() num troppo grande"
    #    print(t)
    #    return t

    fpath = IOHelper.gen_fpath(num, dest_dir, INPUT_MZN_PREFIX, INPUT_MZN_EXT)
    print("fpath " + fpath, file=open('tmp.txt', 'a+'))

    if not os.path.isfile(fpath):
        t = "ERROR! File does not exists!"
        print(t)
        return t

    f = open(fpath)
    t = f.read()
    return t



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


def terminate_process_children():
    current_process = psutil.Process()
    #os.system('pstree -p ' + str(current_process.pid))
    children = current_process.children(recursive=True)
    for child in children:
        #print('Child pid is {}'.format(child.pid))
        child.terminate()
