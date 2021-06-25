from Classi.Automa.automa import *

class Link:
    def __init__(self, nome, automa_sorgente, automa_destinazione, evento=None):
        self.nome = nome
        self.automa_sorgente=automa_sorgente
        self.automa_destinazione=automa_destinazione
        self.evento=evento

    def to_string(self):
        if self.evento is not None:
            return "Nome link: "+self.nome + "\nautoma sorgente: "+self.automa_sorgente.nome+"\nautoma destinazione: "+self.automa_destinazione.nome+"\nevento: "+self.evento.nome
        else:
            return "Nome link: "+self.nome + "\nautoma sorgente: "+self.automa_sorgente.nome+"\nautoma destinazione: "+self.automa_destinazione.nome+"\nevento: None"

    def stampa(self):
        print(self.to_string())


class Rete:
    '''Rete. costituita da automi e link'''
    def __init__(self, nome, automi, links):
        self.nome = nome
        self.automi=automi
        self.links=links

    def to_string(self):
        return "Rete: "+self.nome + "\nautomi: \n"+automi_to_string(self.automi)+"\nlinks: \n"+links_to_string(self.links)

    def stampa(self):
        print(self.to_string())


def links_to_string(links):
    stringa = ""
    for x in range(len(links)):
        stringa = stringa + links[x].to_string() + "\n"
    return stringa