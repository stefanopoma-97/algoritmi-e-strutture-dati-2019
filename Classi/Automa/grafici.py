from graphviz import Digraph
from Classi.Automa.automa import *


def stampa_automa(automa):
    '''stampa l'automa con graphviz'''
    gra = Digraph()
    for s in automa.stati:
        gra.node(s.nome)
    for t in get_transizioni(automa):
        gra.edge(t.stato_sorgente.nome, t.stato_destinazione.nome)

    print(gra.source)

def stampa_automa_su_file(automa, filename):
    gra = Digraph('nome automa', filename=filename, format='png')

    for s in automa.stati:
        gra.node(s.nome, shape='circle')

    if automa.stati_finali[0] is not None:
        for s in automa.stati_finali:
            gra.node(s.nome, shape='doublecircle')

    for t in get_transizioni(automa):
        gra.edge(t.stato_sorgente.nome, t.stato_destinazione.nome, t.nome)

    print(gra.source)

    gra.render(directory="Output/grafici_automi/"+filename)

    riassunto = open("Output/grafici_automi/"+filename+"/"+filename+"_riassunto.txt", "w")
    riassunto.write("Numero di stati:"+str(len(automa.stati))+"\n")
    riassunto.write(stati_to_string(automa.stati)+"\n")

    riassunto.write("Numero di transizioni:" + str(len(get_transizioni(automa))) + "\n")
    riassunto.write(transizioni_to_string(get_transizioni(automa))+"\n")
    riassunto.close()

