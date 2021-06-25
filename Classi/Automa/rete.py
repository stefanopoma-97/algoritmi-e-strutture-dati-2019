

class Link:
    # costruttore con solo il nome
    def __init__(self, nome):
        self.nome = nome

    def stampa(self):
        print("nome: "+self.nome)
        for a in self.automa:
            print("automa: "+a.to_string())