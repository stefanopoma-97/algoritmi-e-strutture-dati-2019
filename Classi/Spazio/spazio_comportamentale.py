'''Modulo per gestire tutte le operazioni su uno spazio comportamentale'''

from Classi.Automa.automa import *
from Classi.Automa.rete import *

class Spazio_comportamentale:
    '''Classe Spazio comportamentale
    Rappresenta una spazio comportamentale
    nome:stringa
    Nodi_finali:[Nodo]
    Nodi_iniziali:[Nodo]
    nodi:[Nodo]
    transizioni:[Transizioni_spazio]
    spazio_potato: Bool'''

    def __init__(self, nome, nodi_finali=[], nodi_iniziali=[], nodi=[], transizioni=[]):
        self.nome = nome
        self.nodi_finali = nodi_finali
        self.nodi_iniziali = nodi_iniziali
        self.nodi = nodi
        self.transizioni = transizioni
        self.spazio_potato=False

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

    def riassunto(self):
        '''Restituisce una stringa riassuntiva delle informazioni contenute nello spazio'''
        stringa=""
        stringa += "Numero di nodi: "+str(len(self.nodi))+"\n"
        i=1
        for n in self.nodi:
            stringa += "\t"+str(i)+") [ ID = "+n.id+"; "+n.output+"]\n"
            i=i+1

        stringa += "\n Numero transizioni: "+str(len(self.transizioni))+"\n"
        i=1
        for t in self.transizioni:
            stringa += "\t"+str(i)+") ("+t.nodo_sorgente.output+") > "+t.nome+" > ("+t.nodo_destinazione.output+")\n"
            i=i+1
        if self.spazio_potato:
            stringa += "Lo spazio è stato potato"
        else:
            stringa += "Lo spazio NON è stato potato"
        return stringa

    def riassunto_potatura(self):
        '''Se lo spazio è stato potato, questo metodo ritorna una stringa contenente le informazioni
        dell'operazione di potatura'''
        stringa=""
        stringa += "Numero di nodi: "+str(len(self.nodi))+"\n"
        stringa += "Numero di nodi potati: " + str(len([x for x in self.nodi if x.potato == True])) + "\n"
        nodi_rimasti=[x for x in self.nodi if x.potato == False]
        stringa += "Numero di nodi rimasti: " + str(len(nodi_rimasti)) + "\n"

        i=1
        for n in nodi_rimasti:
            stringa += "\t"+str(i)+") [ ID = "+n.id+"; "+n.output+"]\n"
            i=i+1
        stringa += "\nNumero transizioni: "+str(len(self.transizioni))+"\n"
        stringa += "Numero di transizioni potate: " + str(len([x for x in self.transizioni if x.potato == True])) + "\n"
        transizioni_rimaste = [x for x in self.transizioni if x.potato == False]
        stringa += "Numero di transizioni rimaste: " + str(len(transizioni_rimaste)) + "\n"
        i=1
        for t in transizioni_rimaste:
            stringa += "\t"+str(i)+") ("+t.nodo_sorgente.id+") > "+t.nome+" > ("+t.nodo_destinazione.id+")\n"
            i=i+1
        if self.spazio_potato:
            stringa += "Lo spazio è stato potato"
        else:
            stringa += "Lo spazio NON è stato potato"
        return stringa


def get_transizioni_spazio(spazio):
    '''Restituisce tutte le transizioni presenti nello spazio (scorrendo tutti i nodi)'''
    transizioni = []
    for s in spazio.nodi:
        transizioni = transizioni + s.transizioni
    return transizioni

def nodi_to_string(nodi):
    '''Ritorna una stringa contenente le informazioni di tutti i nodi'''
    stringa=""
    for n in nodi:
        stringa += n.to_string()
    return stringa

def transizioni_to_string(transizioni):
    '''ritorna una stringa contenente le informazioni su tutte le transizioni'''
    stringa=""
    for t in transizioni:
        stringa += t.to_string()
    return stringa

def check_a_false(spazio):
    ''''Imposta il la variabile check a False in tutti i nodi dello spazio'''
    for n in spazio.nodi:
        n.check=False

def ripristina_transizione(transizione):
    transizione.potato=True

def ripristina_nodo(nodo):
    '''Ripristina la condizione iniziale di un nodo:
    id=""
    check=False
    potato=True
    passata_osservazione=False
    transizioni:[]'''
    nodo.id=""
    nodo.check=False
    nodo.potato=True

    nodo.passata_osservazione=False
    nodo.transizioni=[]

class Nodo:
    '''Nodo di un spazio comportamentale
    stati: [Stato]
    links: dict([link, stringa])
    output: Stringa
    check: Bool
    finale: Bool
    iniziale: Bool
    transizioni: [Transizione_spazio]

    potato=True
    lunghezza_osservazione: Stringa
    passata_osservazione: bool
    output: Stringa'''

    def __init__(self, stati, check, links, iniziale, transizioni=[], *args):
        self.id = ""
        self.transizioni = transizioni
        self.transizioni_sorgente = []
        self.transizioni_auto = []
        self.check = check
        self.stati = stati
        self.links = links
        #costituiti da dict([link, stringa])
        #questo serve ad associare ad ogni nodo una lista di Link e per ogni Link stabilire il valore dell'evento contenuto (stringa)
        #Es. [Link1, "e1"], [Link2, "e2"], [Link3, ""]
        self.iniziale = iniziale
        self.finale = self.is_finale()
        self.potato = True
        self.old_id = ""
        self.lunghezza_osservazione = ""
        #il valore lunghezza_osservazione serve ad indicare a che punto dell'osservazione lineari si è arrivati durante
        #la procedura di creazione di uno spazio comportamentale relativo ad un'osservazione lineare
        #nodi identici, che però differiscono per il valore lunghezza_osservazione, verranno considerati come nodi distinti
        if (len(args)) == 1:
            self.lunghezza_osservazione=args[0]
        self.passata_osservazione = False

        # TODO scrivere a cosa serve
        self.output = self.get_output()




    def is_finale(self):
        '''Ritorna True se il Nodo è finale (non considerando un'osservazione lineare)
        per essere finale non deve essere iniziale
        e il valore dell'evento cotenuto nel dizzionario Links deve essere sempre vuoto

        es. [Link1, ""], [Link2, ""] ecc.'''
        r = True
        if self.iniziale:
            return False
        for key, l in self.links.items():
            if l[1]!="":
                r = False
        return r

    def is_finale_oss(self, lunghezza):
        '''Ritorna True se il Nodo è finale (considerando un'osservazione lineare)
        per essere finale
        1)non deve essere iniziale
        2)il valore dell'evento cotenuto nel dizzionario Links deve essere sempre vuoto
        es. [Link1, ""], [Link2, ""] ecc.
        3)il valore lunghezza_osservazione deve essere uguale alla lunghezza dell'osservazione lineare che si sta considerando

        '''
        r = True
        if self.iniziale:
            return False
        for key, l in self.links.items():
            if l[1]!="":
                r = False
        if lunghezza!=self.lunghezza_osservazione:
            r=False
        return r

    def get_output(self):
        '''Ritorna la stringa contenente il valore di output
        (nome stato1, nome stato2, ecc, evento in link1, evento in link2, ecc, lunghezza_osservazione)'''
        stringa=""
        for s in self.stati:
            stringa += s.nome+", "

        for key, value in self.links.items():
            stringa += value[1] + ", "
        stringa = stringa[:-2]

        if self.lunghezza_osservazione != "":
            stringa += ", "+str(self.lunghezza_osservazione)

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
        if self.transizioni=="":
            stringa = "ID: "+self.id+", output: ["+self.output+"], check: "+str(self.check)+", finale: "+str(self.finale)+", iniziale: "+str(self.iniziale)
        else:
            stringa = "ID: "+self.id+", output: ["+self.output+"], check: "+str(self.check)+", finale: "+str(self.finale)+", iniziale: "+str(self.iniziale)+", lunghezza oss: "+str(self.lunghezza_osservazione)

        return stringa

def contiene_nodo(nodo, nodi):
    '''valuta se nodo è contenuto in nodi sulla base del suo valore di output'''
    out = nodo.get_output()
    for n in nodi:
        if (n.get_output() == out):
            return n
    return False

def contiene_nodo_con_osservazione(nodo, nodi):
    '''valuta se nodo è contenuto in nodi considerando il suo valore di output e anche il valore di lunghezza_osservazione'''
    out = nodo.get_output()
    l_osservazione = nodo.lunghezza_osservazione
    for n in nodi:
        if n.get_output() == out and n.lunghezza_osservazione == l_osservazione:
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
        self.potato = True


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
