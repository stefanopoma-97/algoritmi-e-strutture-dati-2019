'''Modulo contenente classi e metodi per creare e gestire Reti e Link'''
from Classi.Automa.automa import *

class Link:
    '''Classe rappresentate un link tra due automi
    nome: Stringa
    automa_sorgente: Automa
    automa_destinazione: Automa
    evento: Evento'''
    def __init__(self, nome, automa_sorgente, automa_destinazione, evento=Evento("")):
        self.nome = nome
        self.automa_sorgente=automa_sorgente
        self.automa_destinazione=automa_destinazione
        self.evento=evento

    def to_string(self):
        '''Converte il link in una stringa facilmente leggibile'''
        if self.evento.nome!="":
            return "Nome link: "+self.nome + "\nautoma sorgente: "+self.automa_sorgente.nome+"\nautoma destinazione: "+self.automa_destinazione.nome+"\nevento: "+self.evento.nome
        else:
            return "Nome link: "+self.nome + "\nautoma sorgente: "+self.automa_sorgente.nome+"\nautoma destinazione: "+self.automa_destinazione.nome+"\nevento: Vuoto"

    def stampa(self):
        print(self.to_string())

    def to_string_txt(self):
        '''Converte il link nella striga utilizzata per importarlo da file txt'''
        stringa=self.automa_sorgente.nome+">"+self.nome+">"+self.automa_destinazione.nome
        return stringa


class Rete:
    '''CLasse rappresentante una Rete, costituita da automi e link
    nome: Stringa
    automi: [Automa]
    links: [Link]'''
    def __init__(self, nome, automi, links):
        self.nome = nome
        self.automi=automi
        self.links=links

    def to_string(self):
        '''Converte la rete in una stringa facilmente leggibile'''
        return "Rete: "+self.nome + "\n\nautomi: \n"+automi_to_string(self.automi)+"\nlinks: \n"+links_to_string(self.links)

    def stampa(self):
        print(self.to_string())

    def to_string_link_txt(self):
        '''Converte i link della rete nella stringa utilizzata per importare i link da file'''
        stringa=""
        for l in self.links:
            stringa += l.automa_sorgente.nome+">"+l.nome+">"+l.automa_destinazione.nome+"\n"
        #stringa = stringa[:-1]
        return stringa

    def to_string_txt(self):
        '''Converte la rete nella stringa utilizzata per importare la rete stessa da file'''
        stringa = self.nome + "\n"
        for a in self.automi:
            for t in get_transizioni(a):
                stringa += a.nome + ","
                stringa += t.nome + ","

                for e in t.input:
                    if (e.nome=="" and e.link==None):
                        stringa += " /"
                    else:
                        stringa += e.nome + "(" + e.link.nome + ")/"

                if t.output[0].nome=="":
                    stringa += "{ },"
                else:
                    stringa += "{"
                    for e in t.output:
                        stringa += e.nome+"("+e.link.nome+");"
                    stringa = stringa[:-1]
                    stringa += "},"
                if t.osservazione is None:
                    stringa += " ,"
                else:
                    stringa += t.osservazione+","

                if t.rilevanza is None:
                    stringa += " \n"
                else:
                    stringa += t.rilevanza+"\n"
        return stringa

    def get_stati(self):
        '''Restituisce tutti gli stati presenti nella rete. Scorrendo quindi gli automi'''
        stati = []
        for a in self.automi:
            stati += a.stati
        return stati

    def get_transizioni(self):
        '''Restituisce tutte le transizioni presenti nella rete'''
        transizioni=[]
        for a in self.automi:
            for s in a.stati:
                transizioni += s.transizioni
        return transizioni

    def get_stati_correnti(self):
        '''Restituisce l'elenco degli stati correnti di tutti gli automi presenti nella rete'''
        stati = []
        for a in self.automi:
            stati.append(a.stato_corrente[0])
        return stati

    def controlla_osservazione(self, osservazioni):
        '''Data in input una lista di osservazioni (Stringhe). Il metodo verifica che le singole stringhe siano effettivamente
        delle osservazioni presenti all'interno delle transizioni della rete'''
        out = True
        tra = []
        oss = []
        #print("OSSERVAZIONI: "+str(osservazioni))
        for a in self.automi:
            for s in a.stati:
                tra += s.transizioni
        for t in tra:
            if t.osservazione != ' ':
                oss.append(t.osservazione)

        #print("OSS: "+str(oss))

        for o in osservazioni:
            #print("Controllo: "+str(o))
            if o not in oss:
                #print("non presente")
                out = False
        return out



def links_to_string(links):
    '''Data una lista di links la stampa in un formato leggibile'''
    stringa = ""
    for x in range(len(links)):
        stringa = stringa + links[x].to_string() + "\n\n"
    return stringa


