from Classi.Automa.automa import *
from Classi.Automa.rete import *

class Spazio_comportamentale:
    '''Classe Spazio comportamentale
    Rappresenta una spazio comportamentale
    nome:stringa
    Nodi_finali:[Nodo]
    Nodi_iniziali:[Nodo]
    nodi:[Nodo]
    transizioni:[Transizioni_spazio]'''

    def __init__(self, nome, nodi_finali=[], nodi_iniziali=[], nodi=[], transizioni=[]):
        self.nome = nome
        self.nodi_finali = nodi_finali
        self.nodi_iniziali = nodi_iniziali
        self.nodi = nodi
        self.transizioni = transizioni

    def to_string(self):
        '''Converte spazio comportamentale in una Stringa'''
        stringa = "Nome: " + self.nome + "\n"

        if self.nodi_iniziali[0] is None:
            stringa = stringa + "Nodi iniziale: None\n"
        else:
            stringa = stringa + "Nodi iniziale: " + nodi_to_string(self.nodi_iniziali) + "\n"

        if (len(self.nodi_finali) == 1) and (self.nodi_finali[0] is None):
            stringa = stringa + "Nodi finali: None\n"
        else:
            stringa = stringa + "Nodi finali: " + nodi_to_string(self.nodi_finali) + "\n"

        if (len(self.nodi) == 1) and (self.nodi[0] is None):
            stringa = stringa + "Nodi: None\n"
        else:
            stringa = stringa + "Nodi: " + stati_to_string(self.nodi) + "\n"

        stringa = stringa + "Transizioni\n"
        stringa = stringa + transizioni_to_string(self.transizioni)

        return stringa

def get_transizioni_spazio(spazio):
    transizioni = []
    for s in spazio.nodi:
        transizioni = transizioni + s.transizioni
    return transizioni

def nodi_to_string(nodi):
    stringa=""
    for n in nodi:
        stringa += n.to_string()
    return stringa

def transizioni_to_string(transizioni):
    stringa=""
    for t in transizioni:
        stringa += t.to_string()
    return stringa

class Nodo:
    '''Nodo di un spazio comportamentale
    stati: [Stato]
    links: dict([link, stringa])
    output: Stringa
    check: Bool
    finale: Bool
    transizioni: [Transizione_spazio]'''

    def __init__(self, stati, check, links, iniziale, transizioni=[]):
        self.id = ""
        self.transizioni = transizioni
        self.check = check
        self.stati = stati
        self.links = links
        self.iniziale = iniziale
        self.output = self.get_output()
        self.finale = self.is_finale()


    def is_finale(self):
        r = True
        if self.iniziale:
            return False
        for key, l in self.links.items():
            if l[1]!="":
                r = False
        return r

    def get_output(self):
        stringa=""
        for s in self.stati:
            stringa += s.nome+", "

        for key, value in self.links.items():
            stringa += value[1] + ", "
        stringa = stringa[:-2]

        return stringa


    def add_transizione(self, transizione):
        '''Aggiunge una transizione al nodo'''
        elenco = self.transizioni
        lista = []
        for t in elenco:
            lista.append(t)
        lista.append(transizione)
        self.transizioni=lista

    def to_string(self):
        self.output = self.get_output()
        stringa = "ID: "+self.id+", output: ["+self.output+"], check: "+str(self.check)+", finale: "+str(self.finale)+", iniziale: "+str(self.iniziale)
        return stringa

def contiene_nodo(nodo, nodi):
    out = nodo.get_output()
    for n in nodi:
        if (n.get_output() == out):
            return n
    return False


class Transizione_spazio:
    '''Classe rappresentante una transizione di uno spazio comportamentale'''

    def __init__(self, nome, nodo_sorgente=None, nodo_destinazione=None, osservazione=None, rilevanza=None):
        '''una transizione è costituita da
        Nome
        stato sorgente
        stato destinazione
        etichetta di osservazione
        etichetta di rilevanza
        '''
        self.nome = nome
        self.nodo_sorgente = nodo_sorgente
        self.nodo_destinazione = nodo_destinazione
        self.osservazione = osservazione
        self.rilevanza = rilevanza


    def oss_ril_to_string(self):
        '''Stampa le etichette di osservabilità e rilevanza'''
        out = "[Oss: "
        if self.osservazione is not None:
            out = out + self.osservazione
        else:
            out = out + "None"
        out = out + "; ril: "
        if self.rilevanza is not None:
            out = out + self.rilevanza
        else:
            out = out + "None"

        out = out + "]"
        return out



    def to_string(self):
        '''converte la transizione in una stringa facilmente leggibile'''
        return self.nodo_sorgente.to_string() + "\n\t>>>>>" + "\t"+self.nome + "\t>>>>>\n" + self.nodo_destinazione.to_string() +"\n"+\
            "\t"+self.oss_ril_to_string()