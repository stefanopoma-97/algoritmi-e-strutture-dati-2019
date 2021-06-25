from graphviz import Digraph
from Classi.Automa.automa import *
from Classi.Automa.rete import *


def stampa_automa(automa):
    '''stampa l'automa con graphviz'''
    gra = Digraph()
    for s in automa.stati:
        gra.node(s.nome)
    for t in get_transizioni(automa):
        gra.edge(t.stato_sorgente.nome, t.stato_destinazione.nome, label=transizione_to_string(t))

    print(gra.source)

def stampa_automi_su_file(automi, cartella):
    gra = Digraph('automa doppio', filename='automa doppio', format='png')

    for a in automi:
        stampa_automa_su_file_new(gra, a)

    print(gra.source)
    gra.render(directory="Output/grafici_automi/" + cartella)

    stati=[]
    transizioni=[]
    for a in automi:
        stati+=a.stati
        transizioni+=get_transizioni(a)

    riassunto = open("Output/grafici_automi/" + cartella + "/" + 'automa doppio' + "_riassunto.txt", "w")
    riassunto.write("Numero di stati:" + str(len(stati)) + "\n")
    riassunto.write(stati_to_string(stati) + "\n")

    riassunto.write("Numero di transizioni:" + str(len(transizioni)) + "\n")
    riassunto.write(transizioni_to_string(transizioni) + "\n")
    riassunto.close()

def stampa_automa_su_file_new(gra, automa):

    for s in automa.stati:
        gra.node(s.nome, shape='circle')

    if automa.stati_finali[0] is not None:
        for s in automa.stati_finali:
            gra.node(s.nome, shape='doublecircle')

    for t in get_transizioni(automa):
        gra.edge(t.stato_sorgente.nome, t.stato_destinazione.nome, label=transizione_to_string(t))




    # riassunto = open("Output/grafici_automi/" + filename + "/" + filename + "_riassunto.txt", "w")
    # riassunto.write("Numero di stati:" + str(len(automa.stati)) + "\n")
    # riassunto.write(stati_to_string(automa.stati) + "\n")
    #
    # riassunto.write("Numero di transizioni:" + str(len(get_transizioni(automa))) + "\n")
    # riassunto.write(transizioni_to_string(get_transizioni(automa)) + "\n")
    # riassunto.close()

def stampa_automa_su_file(automa, cartella):
    gra = Digraph(automa.nome, filename=automa.nome, format='png')

    for s in automa.stati:
        gra.node(s.nome, shape='circle')

    if automa.stati_finali[0] is not None:
        for s in automa.stati_finali:
            gra.node(s.nome, shape='doublecircle')

    for t in get_transizioni(automa):
        gra.edge(t.stato_sorgente.nome, t.stato_destinazione.nome, label=transizione_to_string(t))

    print(gra.source)

    gra.render(directory="Output/grafici_automi/"+cartella)

    riassunto = open("Output/grafici_automi/"+cartella+"/"+automa.nome+"_riassunto.txt", "w")
    riassunto.write("Numero di stati:"+str(len(automa.stati))+"\n")
    riassunto.write(stati_to_string(automa.stati)+"\n")

    riassunto.write("Numero di transizioni:" + str(len(get_transizioni(automa))) + "\n")
    riassunto.write(transizioni_to_string(get_transizioni(automa))+"\n")
    riassunto.close()

def stampa_rete_su_file(rete, cartella):
    gra = Digraph("rete", filename=rete.nome, format='png')

    for automa in rete.automi:
        gra.node(automa.nome, shape='box')

    for link in rete.links:
        gra.edge(link.automa_sorgente.nome, link.automa_destinazione.nome, link.nome)

    print(gra.source)

    gra.render(directory="Output/grafici_automi/" + cartella)

    riassunto = open("Output/grafici_automi/"+cartella+"/"+rete.nome+"_riassunto.txt", "w")
    riassunto.write("Numero di automi:" + str(len(rete.automi)) + "\n")
    riassunto.write("Numero di link:" + str(len(rete.links)) + "\n")
    riassunto.close()
