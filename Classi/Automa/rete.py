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

    def to_string_link_txt(self):
        stringa=""
        for l in self.links:
            stringa += l.automa_sorgente.nome+">"+l.nome+">"+l.automa_destinazione.nome+"\n"
        stringa = stringa[:-1]
        return stringa

    def to_string_txt(self):
        stringa=""
        for a in self.automi:
            for t in get_transizioni(a):
                stringa += a.nome + ","
                stringa += t.nome + ":"

                if t.input is None:
                    stringa += " /"
                else:
                    for e in t.input:
                        stringa += e.nome+"("+e.link.nome+")/"

                if t.output is None:
                    stringa += "{ },"
                else:
                    stringa += "{"
                    for e in t.output:
                        stringa += e.nome+"("+e.link.nome+"),"
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


def links_to_string(links):
    stringa = ""
    for x in range(len(links)):
        stringa = stringa + links[x].to_string() + "\n"
    return stringa