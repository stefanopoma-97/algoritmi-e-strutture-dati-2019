'''Modulo per gestire tutta la componente di creazione di grafici e esportazione in file .PNG'''

from graphviz import Digraph
from Classi.Automa.automa import *
from Classi.Automa.rete import *
from  Classi.Spazio.spazio_comportamentale import *
import os

class Colour:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def stampa_automa(automa):
    '''stampa l'automa con graphviz
    l'output è presentato su riga di comando'''
    gra = Digraph()
    for s in automa.stati:
        gra.node(s.nome)
    for t in get_transizioni(automa):
        gra.edge(t.stato_sorgente.nome, t.stato_destinazione.nome, label=transizione_to_string(t))

    #print(gra.source)

#non usato per ora
def stampa_automi_su_file(automi, cartella):
    '''Vengono stampati gli automi dato in input e salvato nella cartella specificata'''
    gra = Digraph('automa doppio', filename='automa doppio', format='png')

    for a in automi:
        stampa_automa_su_file_new(gra, a)

    #print(gra.source)
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


def stampa_automa_su_file(automa, cartella):
    '''Stampa l'automa su un file PNG
    Input: automa, nome cartella di output
    Output: viene generato un file .png nella cartella selezionata
    viene anche creato un file nome_automa_riassunto.txt contenente le informazioni sull'automa in questione'''
    gra = Digraph(automa.nome, filename=automa.nome+"_grafico", format='png')

    for s in automa.stati:
        gra.node(s.nome, shape='circle')
    gra.node("start", shape="point", label="")

    gra.node(automa.stato_corrente[0].nome, shape='circle', color='red')

    if automa.stati_finali[0] is not None or automa.stati_finali[0]!="":
        for s in automa.stati_finali:
            if s.nome!="":
                gra.node(s.nome, shape='doublecircle')

    for t in get_transizioni(automa):
        gra.edge(t.stato_sorgente.nome, t.stato_destinazione.nome, label=t.nome)

    gra.edge("start", automa.stati_iniziali[0].nome, label="")

    #print(gra.source)

    gra.render(directory="Output/"+cartella)

    riassunto = open("Output/"+cartella+"/"+automa.nome+"_riassunto.txt", "w")
    riassunto.write("Numero di stati:"+str(len(automa.stati))+"\n")
    riassunto.write(stati_to_string(automa.stati)+"\n")

    riassunto.write("Numero di transizioni:" + str(len(get_transizioni(automa))) + "\n")
    #riassunto.write(transizioni_to_string(get_transizioni(automa))+"\n")
    for t in get_transizioni(automa):
        riassunto.write("\t"+t.to_string() + "\n")
    riassunto.close()


def stampa_spazio_su_file(spazio, cartella, *args):
    '''Stampa l'automa su un file PNG
    Input: automa, nome cartella di output
            *args permette di specificare una stringa aggiuntiva da mettere in coda al nome del file generato
    Output: viene generato un file .png nella cartella selezionata
    viene anche creato un file nome_automa_riassunto.txt contenente le informazioni sull'automa in questione'''


    if len(args)==1:
        aggiunta=args[0]
    else:
        aggiunta=""

    gra = Digraph(spazio.nome, filename=spazio.nome+"_grafico"+aggiunta, format='png')

    for s in spazio.nodi:
        gra.node(s.output, shape='circle')

    gra.node("start", shape="point", label="")
    if len(spazio.nodi_finali)>0:
        if spazio.nodi_finali[0] is not None or spazio.nodi_finali[0]!="":
            for s in spazio.nodi_finali:
                if s.output!="":
                    gra.node(s.output, shape='doublecircle')

    for t in spazio.transizioni:
        nome = "<"+t.nome+" ["+'<FONT COLOR="green">' + t.osservazione + '</FONT>'+", "+'<FONT COLOR="red">' + t.rilevanza + '</FONT>'+"]>"
        gra.edge(t.nodo_sorgente.output, t.nodo_destinazione.output, label=nome)

    gra.edge("start", spazio.nodi_iniziali[0].output, label="")

    #print(gra.source)

    gra.render(directory="Output/"+cartella)

    riassunto = open("Output/"+cartella+"/"+spazio.nome+"_riassunto"+aggiunta+".txt", "w")
    riassunto.write(spazio.riassunto())
    riassunto.close()

def stampa_spazio_ridenominato_su_file(spazio, cartella, *args):
    '''Stampa l'automa su un file PNG
    Input: automa, nome cartella di output
            *args permette di specificare una stringa aggiuntiva da mettere in coda al nome del file generato
    Output: viene generato un file nome_ridenominazione_grafico.png nella cartella selezionata
    viene anche creato un file nome automa_riassunto.txt contenente le informazioni sull'automa in questione'''

    if len(args)==1:
        aggiunta=args[0]
    else:
        aggiunta=""

    gra = Digraph(spazio.nome, filename=spazio.nome + "_ridenominazione_grafico"+aggiunta, format='png')

    for s in spazio.nodi:
        gra.node(s.id, shape='circle')

    gra.node("start", shape="point", label="")
    if len(spazio.nodi_finali) > 0:
        if spazio.nodi_finali[0] is not None or spazio.nodi_finali[0] != "":
            for s in spazio.nodi_finali:
                if s.output != "":
                    gra.node(s.id, shape='doublecircle')

    for t in spazio.transizioni:
        nome = "<" + t.nome + " [" + '<FONT COLOR="green">' + t.osservazione + '</FONT>' + ", " + '<FONT COLOR="red">' + t.rilevanza + '</FONT>' + "]>"
        gra.edge(t.nodo_sorgente.id, t.nodo_destinazione.id, label=nome)

    if (len(spazio.nodi_iniziali))==1:
        gra.edge("start", spazio.nodi_iniziali[0].id, label="")

    gra.render(directory="Output/"+cartella)


def stampa_spazio_potato_su_file(spazio, cartella, *args):
    '''Stampa l'automa su un file PNG
    Input: automa, nome cartella di output
            *args permette di specificare una stringa aggiuntiva da mettere in coda al nome del file generato
    Output: viene generato un file nome_potatura_grafico.png nella cartella selezionata
    viene anche creato un file nome_riassunto.txt contenente le informazioni sull'automa in questione'''
    if (len(args)==1):
        aggiunta=args[0]
    else:
        aggiunta=""

    gra = Digraph(spazio.nome, filename=spazio.nome+"_potatura_grafico"+aggiunta, format='png')

    #print("INSERISCO NODI")
    for s in spazio.nodi:
        if s.potato == False:
            #print(s.to_string())
            gra.node(s.id, shape='circle')

    gra.node("start", shape="point", label="")

    if (len(spazio.nodi_finali)>0):
        if spazio.nodi_finali[0] is not None or spazio.nodi_finali[0]!="":
            for s in spazio.nodi_finali:
                if s.id!="":
                    gra.node(s.id, shape='doublecircle')
    i = 0
    for t in spazio.transizioni:
        #print("\n\n\n")
        #print(str(i)+") "+"ID: "+t.nodo_sorgente.id+"("+str(t.nodo_sorgente.potato)+") - "+t.nome+" potata: "+str(t.potato)+", "+str(t.nodo_destinazione.id)+"("+str(t.nodo_destinazione.potato)+")")
        i=i+1
        if t.nodo_sorgente.potato == False and t.nodo_destinazione.potato == False:
            nome = "<" + t.nome + " [" + '<FONT COLOR="green">' + t.osservazione + '</FONT>' + ", " + '<FONT COLOR="red">' + t.rilevanza + '</FONT>' + "]>"
            gra.edge(t.nodo_sorgente.id, t.nodo_destinazione.id, label=nome)
            #print("La stampo")


    gra.edge("start", spazio.nodi_iniziali[0].id, label="")

    #print(gra.source)

    gra.render(directory="Output/"+cartella)

    riassunto = open("Output/"+cartella+"/"+spazio.nome+"_potatura_riassunto"+aggiunta+".txt", "w")
    riassunto.write(spazio.riassunto_potatura())
    riassunto.close()


def stampa_rete_su_file(rete, cartella):
    '''Stampa la rete su un file PNG
        Input: rete, nome cartella di output
        Output: viene generato un file nome_rete.png nella cartella selezionata
        viene anche creato un file nome rete_riassunto.txt contenente le informazioni sull'automa in questione'''
    gra = Digraph("rete", filename=rete.nome+"_grafico", format='png')

    for automa in rete.automi:
        gra.node(automa.nome, shape='box')

    for link in rete.links:
        gra.edge(link.automa_sorgente.nome, link.automa_destinazione.nome, link.nome)

    #print(gra.source)

    gra.render(directory="Output/" + cartella)

    riassunto = open("Output/" + cartella+"/"+rete.nome+"_riassunto.txt", "w")
    riassunto.write("Numero di automi:" + str(len(rete.automi)) + "\n")
    riassunto.write("Numero di link:" + str(len(rete.links)) + "\n")
    riassunto.write(rete.to_string())
    riassunto.close()
