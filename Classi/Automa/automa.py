'''modulo contenente le classi per creare un automa'''

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
        self.stato_corrente=stato_corrente
        self.stati_finali = stati_finali
        self.stati_iniziali = stati_iniziali
        self.stati = stati

    def to_string(self):
        '''Converte automa in una Stringa'''
        stringa = "Nome: "+self.nome+"\n"
        if self.stato_corrente is None:
            stringa=stringa+"Stato corrente: None\n"
        else:
            stringa=stringa+"Stato corrente: "+stati_to_string(self.stato_corrente)+"\n"

        if self.stati_iniziali is None:
            stringa=stringa+"Stato iniziale: None\n"
        else:
            stringa=stringa+"Stato iniziale: "+stati_to_string(self.stati_iniziali)+"\n"

        if (len(self.stati_finali) ==1) and (self.stati_finali[0] is None):
            stringa=stringa+"Stati finali: None\n"
        else:
            stringa=stringa+"Stati finali: "+stati_to_string(self.stati_finali)+"\n"

        if (len(self.stati) == 1) and (self.stati[0] is None):
            stringa = stringa + "Stati: None\n"
        else:
            stringa = stringa + "Stati: " + stati_to_string(self.stati) + "\n"

        stringa=stringa+"Transizioni\n"
        stringa=stringa+transizioni_to_string(get_transizioni(self))



        return stringa

    def stampa(self):
        '''Stampa automa'''
        print(self.to_string())

    def passaggio(self):
        self.stato_corrente[0]=self.stati[1]




def get_transizioni(automa):
    transizioni=[]
    for s in automa.stati:
        transizioni=transizioni+s.transizioni
    return transizioni

def stati_to_string(stati):
    '''data una lista di stati ritorna una stringa
    nome stato 1; nome stato 2; ecc.'''
    stringa=""
    for x in range(len(stati)):
        stringa=stringa+stati[x].to_string()+"; "
    return stringa

def stato_to_string(stato):
    '''dato uno stato stampa il suo nome'''
    return stato.to_string()

def transizioni_to_string(transizioni):
    '''data una lista di transizioni ritorna una stringa'''
    stringa=""
    for x in range(len(transizioni)):
        stringa=stringa+transizioni[x].to_string()+"\n"
    return stringa

def transizione_to_string(transizione):
    '''data una lista di transizioni ritorna una stringa'''
    return transizione.to_string()


class Stato:
    '''Stato di un automa
    nome: Stringa
    transizioni: [Transizione]'''
    def __init__(self, nome, transizioni=[]):
        self.nome = nome
        self.transizioni=transizioni

    def add_transizione(self, transizione):
        self.transizioni=self.transizioni.append(transizione)

    def to_string(self):
        stringa=""
        return stringa+self.nome

class transizione:
    '''Classe rappresentante una transizione di un automa a stati finiti'''
    def __init__(self, nome, stato_sorgente=None, stato_destinazione=None, osservazione=None, rilevanza=None):
        self.nome = nome
        self.stato_sorgente=stato_sorgente
        self.stato_destinazione=stato_destinazione
        self.osservazione=osservazione
        self.rilevanza=rilevanza

    def to_string(self):
        return stato_to_string(self.stato_sorgente)+">"+self.nome+">"+stato_to_string(self.stato_destinazione)


class Link:
    # costruttore con solo il nome
    def __init__(self, nome):
        self.nome = nome

    def stampa(self):
        print("nome: "+self.nome)
        for a in self.automa:
            print("automa: "+a.to_string())