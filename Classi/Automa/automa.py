'''modulo contenente le classi per creare un automa'''
import pickle


class Automa:
    '''Classe Automa
    Rappresenta una macchina a stati finiti
    nome:stringa
    stato_corrente:Stato
    stati_finali:[Stato]
    stato_iniziale:Stato
    stati:[Stato]'''

    def __init__(self, nome, stato_corrente=None, stati_finali=[None], stati_iniziali=None, stati=[None]):
        self.nome = nome
        self.stato_corrente = stato_corrente
        self.stati_finali = stati_finali
        self.stati_iniziali = stati_iniziali
        self.stati = stati

    def to_string(self):
        '''Converte automa in una Stringa'''
        stringa = "Nome: " + self.nome + "\n"
        if self.stato_corrente is None:
            stringa = stringa + "Stato corrente: None\n"
        else:
            stringa = stringa + "Stato corrente: " + stati_to_string(self.stato_corrente) + "\n"

        if self.stati_iniziali is None:
            stringa = stringa + "Stato iniziale: None\n"
        else:
            stringa = stringa + "Stato iniziale: " + stati_to_string(self.stati_iniziali) + "\n"

        if (len(self.stati_finali) == 1) and (self.stati_finali[0] is None):
            stringa = stringa + "Stati finali: None\n"
        else:
            stringa = stringa + "Stati finali: " + stati_to_string(self.stati_finali) + "\n"

        if (len(self.stati) == 1) and (self.stati[0] is None):
            stringa = stringa + "Stati: None\n"
        else:
            stringa = stringa + "Stati: " + stati_to_string(self.stati) + "\n"

        stringa = stringa + "Transizioni\n"
        stringa = stringa + transizioni_to_string(get_transizioni(self))

        return stringa

    def to_string_txt(self):
        '''Converte automa nella stringa utilizzata per importarlo dal file .txt'''
        stringa = self.nome + "\n"

        if (len(self.stati) == 1) and (self.stati[0] is None):
            stringa = stringa + "\n"
        else:
            for s in self.stati:
                stringa += s.nome+","
            stringa = stringa[:-1]
            stringa += "\n"

        if (len(self.stati_finali) == 1) and (self.stati_finali[0] is None):
            stringa = stringa + "\n"
        else:
            for s in self.stati_finali:
                stringa += s.nome+","
            stringa = stringa[:-1]
            stringa += "\n"

        for t in get_transizioni(self):
            stringa += t.stato_sorgente.nome+">"+t.nome+">"+t.stato_destinazione.nome+","
        stringa = stringa[:-1]
        return stringa

    def stampa(self):
        '''Stampa automa'''
        print(self.to_string())

    def passaggio(self):
        self.stato_corrente[0] = self.stati[1]


class Stato:
    '''Stato di un automa
    nome: Stringa
    transizioni: [Transizione]'''

    def __init__(self, nome, transizioni=[]):
        self.nome = nome
        self.transizioni = transizioni

    def add_transizione(self, transizione):
        self.transizioni = self.transizioni.append(transizione)

    def to_string(self):
        stringa = ""
        return stringa + self.nome


class Transizione:
    '''Classe rappresentante una transizione di un automa a stati finiti'''

    def __init__(self, nome, stato_sorgente=None, stato_destinazione=None, osservazione=None, rilevanza=None,
                 input=None, output=None):
        '''una transizione è costituita da
        Nome
        stato sorgente
        stato destinazione
        etichetta di osservazione
        etichetta di rilevanza
        eventi in input
        eventi in output'''
        self.nome = nome
        self.stato_sorgente = stato_sorgente
        self.stato_destinazione = stato_destinazione
        self.osservazione = osservazione
        self.rilevanza = rilevanza
        self.input = input
        self.output = output

    def oss_ril_to_string(self):
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

    def eventi_to_string(self, eventi):
        out="{"

        if eventi is None:
            out+=" : }"
        else:
            for e in eventi:
                out+=e.to_string()+";"
            out+="}"

        return out

    def to_string(self):
        return stato_to_string(self.stato_sorgente) + ">" + self.nome + ">" + stato_to_string(
            self.stato_destinazione) + self.oss_ril_to_string()+" " + self.eventi_to_string(self.input) + " " + self.eventi_to_string(self.output)


class Evento:
    '''Classe rappresentante l'evento (input e output di una transizione)'''

    def __init__(self, nome, link=None):
        '''L'eventi è costituito da
        nome: stringa
        link: Link'''
        self.nome = nome
        self.link = link

    def to_string(self):
        return self.link.nome + ":" + self.nome


def get_transizioni(automa):
    transizioni = []
    for s in automa.stati:
        transizioni = transizioni + s.transizioni
    return transizioni


def stati_to_string(stati):
    '''data una lista di stati ritorna una stringa
    nome stato 1; nome stato 2; ecc.'''
    stringa = ""
    for x in range(len(stati)):
        stringa = stringa + stati[x].to_string() + "; "
    return stringa


def stato_to_string(stato):
    '''dato uno stato stampa il suo nome'''
    return stato.to_string()


def transizioni_to_string(transizioni):
    '''data una lista di transizioni ritorna una stringa'''
    stringa = ""
    for x in range(len(transizioni)):
        stringa = stringa + transizioni[x].to_string() + "\n"
    return stringa


def transizione_to_string(transizione):
    '''data una lista di transizioni ritorna una stringa'''
    return transizione.to_string()

def automi_to_string(automi):
    stringa = ""
    for x in range(len(automi)):
        stringa = stringa + automi[x].to_string() + "\n"
    return stringa

def salva_automa_su_file(automa, cartella, filename):
    with open('Output/'+cartella+'/'+filename, 'wb') as config_dictionary_file:
        # Step 3
        pickle.dump(automa, config_dictionary_file)

def carica_automa_da_file(cartella, filename):
    with open('Output/'+cartella+'/'+filename, 'rb') as config_dictionary_file:
        automa_load = pickle.load(config_dictionary_file)
        return automa_load
