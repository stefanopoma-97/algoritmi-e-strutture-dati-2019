'''Modulo per gestire le operazioni di scrittura su file e di importazione'''
import pickle
from Classi.Automa.automa import *
from Classi.Automa.rete import *
import re
from tkinter import filedialog
from Classi.Spazio.spazio_comportamentale import *
import os

#Espressioni regolari per verificare la correttezza dei file txt di input per automi, link e transizioni
#REGEX_AUTOMA="^[a-zA-Z0-9]+\\n[0-9]+(\,[0-9]+)*\\n([0-9]+(\,[0-9]+)*)?\\n[0-9]+\>[a-zA-Z0-9]+\>[0-9]+(\,[0-9]+\>[a-zA-Z0-9]+\>[0-9]+)*\\n"
REGEX_AUTOMA="^[A-Za-z0-9_.]+\\n[A-Za-z0-9_.]+(\,[A-Za-z0-9_.]+)*\\n([A-Za-z0-9_.]+(\,[A-Za-z0-9_.]+)*)?\\n[A-Za-z0-9_.]+\>[A-Za-z0-9_.]+\>[A-Za-z0-9_.]+(\,[A-Za-z0-9_.]+\>[A-Za-z0-9_.]+\>[A-Za-z0-9_.]+)*\\n"
REGEX_LINK="^[a-zA-Z0-9]+\>[a-zA-Z0-9]+\>[a-zA-Z0-9]+\\n([a-zA-Z0-9]+\>[a-zA-Z0-9]+\>[a-zA-Z0-9]+\\n)*"
#REGEX_RETE="^[a-zA-Z0-9 ]+\\n([a-zA-Z0-9]+\,[a-zA-Z0-9]+\,(([a-zA-Z0-9]+\([a-zA-Z0-9]+\))| )\/\{((([a-zA-Z0-9]+\([a-zA-Z0-9]+\))(\;[a-zA-Z0-9]+\([a-zA-Z0-9]+\))*)| )\}\,([a-zA-Z0-9]+| )\,([a-zA-Z0-9]+| )\\n)*"
REGEX_RETE="^[a-zA-Z0-9 ]+\\n([a-zA-Z0-9]+\,[a-zA-Z0-9]+\,(([a-zA-Z0-9]+\([a-zA-Z0-9]+\))| )\/\{((([a-zA-Z0-9]+\([a-zA-Z0-9]+\))(\;[a-zA-Z0-9]+\([a-zA-Z0-9]+\))*)| )\}\,([a-zA-Z0-9 ]+| )\,([a-zA-Z0-9 ]+| )\\n)*"



#Importa componenti da file

def carica_spazio_da_file(*args):
    '''Carica un automa da un file generato in precedenza

    il file non deve avere estensione e deve contenere una classe di tipo Automa'''

    if len(args)==1:
        with open(args[0], 'rb') as config_dictionary_file:
            spazio_load = pickle.load(config_dictionary_file)
            return spazio_load
    else:
        file = filedialog.askopenfilename()
        estensione = file.split(".")
        if len(estensione) != 1:
            return "Estensione del file errata. Seleziona il file corretto"
        with open(file, 'rb') as config_dictionary_file:
            try:
                spazio_load = pickle.load(config_dictionary_file)
                if (isinstance(spazio_load, Spazio_comportamentale)):
                    check_a_false(spazio_load)
                    return spazio_load
                else:
                    return "Il file selezionato non contine una rete"

            except pickle.UnpicklingError as e:
                return "Il file selezionato non contine una rete"

def carica_automa_da_file(cartella, filename):
    '''Carica un automa da un file generato in precedenza'''
    with open('Output/'+cartella+'/'+filename, 'rb') as config_dictionary_file:
        automa_load = pickle.load(config_dictionary_file)
        return automa_load

def carica_rete_da_file(*args):
    '''Carica la rete da un file generato in precedenza'''

    if len(args)==1:
        with open(args[0], 'rb') as config_dictionary_file:
            rete_load = pickle.load(config_dictionary_file)
            return rete_load
    else:
        file = filedialog.askopenfilename()
        estensione = file.split(".")
        if len(estensione) != 1:
            return "Estensione del file errata. Seleziona il file corretto"
        with open(file, 'rb') as config_dictionary_file:
            try:
                rete_load = pickle.load(config_dictionary_file)
                if (isinstance(rete_load, Rete)):
                    return rete_load
                else:
                    return "Il file selezionato non contine una rete"

            except pickle.UnpicklingError as e:
                return "Il file selezionato non contine una rete"


#Salva componenti in un file

def salva_rete_su_file(rete, cartella, filename):
    '''Salva la rete su un file. Utilizzabile poi per importare nel programma la rete stessa'''
    with open('Output/'+cartella+'/'+filename, 'wb') as config_dictionary_file:
        pickle.dump(rete, config_dictionary_file)

def salva_spazio_su_file(spazio, cartella, *args):
    '''Salva lo spazio comportamentale su file
    Input:
        spazio
        cartella di salvataggio
        *args: stringa aggiuntiva messa in coda al nome del file

    output:
        file png in Output/cartalla/nome_spazio_salvataggio aggiunta.png'''
    if len(args)==1:
        aggiunta=args[0]
    else:
        aggiunta=""

    filePath = 'Output/'+cartella+'/'+spazio.nome+"_salvataggio"+aggiunta
    if os.path.exists(filePath):
        os.remove(filePath)

    with open('Output/'+cartella+'/'+spazio.nome+"_salvataggio"+aggiunta, 'wb') as config_dictionary_file:
        # Step 3
        pickle.dump(spazio, config_dictionary_file)

def salva_spazio_potato_su_file(spazio, cartella, *args):
    '''Salva lo spazio comportamentale potato su file
        Input:
            spazio
            cartella di salvataggio
            *args: stringa aggiuntiva messa in coda al nome del file

        output:
            file png in Output/cartalla/nome_spazio_potato_salvataggio aggiunta.png'''
    if len(args)==1:
        aggiunta=args[0]
    else:
        aggiunta=""
    filePath = 'Output/'+cartella+'/'+spazio.nome+"_potato_salvataggio"+aggiunta
    if os.path.exists(filePath):
        os.remove(filePath)

    with open('Output/'+cartella+'/'+spazio.nome+"_potato_salvataggio"+aggiunta, 'wb') as config_dictionary_file:
        # Step 3
        pickle.dump(spazio, config_dictionary_file)

def salva_automa_su_file(automa, cartella, filename):
    '''Salva l'automa su un file. Utilizzabile poi per importare nel programma l'automa stesso'''
    with open('Output/'+cartella+'/'+filename, 'wb') as config_dictionary_file:
        # Step 3
        pickle.dump(automa, config_dictionary_file)


#Salva componenti in un file txt (nel formato corretto per futura importazione)
def salva_rete_su_file_txt(rete, cartella, filename):
    '''Salva la rete in un file txt, rispettando il formato corretto
    è quindi possibile utilizzare il file generato per importare la rete durante una nuova esecuzione del programma'''
    file_txt = open('Output/'+cartella+'/'+filename+".txt", "w")
    file_txt.write(rete.to_string_txt())
    file_txt.close()

def salva_links_su_file_txt(rete, cartella, filename):
    '''Salva i links in un file txt, rispettando il formato corretto
    è quindi possibile utilizzare il file generato per importare i link durante una nuova esecuzione del programma'''
    file_txt = open('Output/'+cartella+'/'+filename+".txt", "w")
    file_txt.write(rete.to_string_link_txt())
    file_txt.close()

def salva_automa_su_file_txt(automa, cartella, filename):
    '''Salva l'automa in un file txt, rispettando il formato corretto
    è quindi possibile utilizzare il file generato per importare l'automa durante una nuova esecuzione del programma'''
    file_txt = open('Output/'+cartella+'/'+filename+".txt", "w")
    file_txt.write(automa.to_string_txt())
    file_txt.close()




#Importa componenti da file .txt
def carica_automa_da_file_txt(*args):
    '''Carica un automa da un file .txt
    il file deve rispettare l'espressione regolare REGEX_AUTOMA'''

    if len(args)==1:
        f = open(args[0], "r")
    else:
        file = filedialog.askopenfilename()
        estensione = file.split(".")
        if len(estensione) != 2 or estensione[1] != "txt":
            return "Estensione del file errata. Seleziona un file .txt"
        f = open(file, "r")

    stringa_regex = f.read()
    x = re.fullmatch(REGEX_AUTOMA, stringa_regex)
    if x:
        print("Formato del file corretto")
    else:
        print("Problema nella lettura")
        return "Il formato del file non è corretto. Impossibile importarlo"

    f.close()

    if len(args)==1:
        f = open(args[0], "r")
    else:
        f = open(file, "r")

    automa = Automa("nome")


    # Riga 1: "nome"\n
    riga = f.readline()
    automa.nome = riga[:-1]

    # Riga 2: "stato1","stato2"\n
    riga = f.readline()
    riga = riga[:-1] #tolgo \n
    nomi_stato = riga.split(",")

    stati=[]
    for s in nomi_stato:
        stati.append(Stato(s))

    automa.stati=stati
    automa.stato_corrente = [automa.stati[0]]
    automa.stati_iniziali = [automa.stati[0]]


    # Riga 3: "stato1","stato2"\n
    riga = f.readline()
    if riga != "":
        riga = riga[:-1] #tolgo \n
        nomi_stato = riga.split(",")
        stati = []
        for s in nomi_stato:
            stati.append(Stato(s))
        automa.stati_finali=stati
    else:
        automa.stati_finali=[]

    # Riga 4: "stato1">"etichetta">"stato2","stato1">"stato2">"etichetta"\n

    riga = f.readline()
    riga = riga[:-1]  # tolgo \n
    nomi_transizioni = riga.split(",")

    transizioni = []
    for t in nomi_transizioni: #scorro le transizioni
        #print("scorro transizioni: "+t)
        componenti = t.split(">")
        lista_componenti = []
        for c in componenti: #scorro i componenti di una transizione
            lista_componenti.append(c)
            #print("componente: "+c)
        tra = Transizione(lista_componenti[1])

        #verifico che lo stato della transizione esista
        stato_presente=[x for x in automa.stati if x.nome == lista_componenti[0]]
        if (len(stato_presente)==1):
            #print("stato interessato a modifica: "+stato_presente[0].nome)
            tra.stato_sorgente=stato_presente[0]
            stato_presente[0].add_transizione(tra)
        else:
            return "Uno stato inserito nelle transizioni non è stato dichiarato precedentemente"

        stato_presente = [x for x in automa.stati if x.nome == lista_componenti[2]]
        if (len(stato_presente) == 1):
            tra.stato_destinazione = stato_presente[0]
        else:
            return "Uno stato inserito nelle transizioni non è stato dichiarato precedentemente"

        #print("transizione aggiunta")
        #print("stato1")
        #print(transizioni_to_string(automa.stati[0].transizioni))
        #print("stato2")
        #print(transizioni_to_string(automa.stati[1].transizioni))
        automa.transizioni = get_transizioni(automa)
        f.close()

    return automa

def carica_links_da_file_txt(automi, *args):
    '''Carica dei links da un file txt
    Devono essere forniti gli automi esistenti'''

    if len(args)==1:
        f = open(args[0], "r")
    else:
        file = filedialog.askopenfilename()
        estensione = file.split(".")
        if len(estensione) != 2 or estensione[1] != "txt":
            return "Estensione del file errata. Seleziona un file .txt"
        f = open(file, "r")

    stringa_regex = f.read()
    x = re.fullmatch(REGEX_LINK, stringa_regex)
    if x:
        print("Inizio a leggere il file")
    else:
        print("problema nella lettura")
        return "Il formato del file non è corretto. Impossibile importarlo"
    f.close()

    if len(args)==1:
        f = open(args[0], "r")
    else:
        f = open(file, "r")

    links=[]

    while (True):
        riga = f.readline()
        if not riga or riga == "\n":
            break
        riga = riga[:-1] #tolgo\n
        componenti = riga.split(">")
        lista_componenti = []
        for c in componenti:
            lista_componenti.append(c)

        # verifico che l'automa sorgente esista
        automa_presente = [x for x in automi if x.nome == lista_componenti[0]]
        if (len(automa_presente) == 1):
            sorgente = automa_presente[0]
        else:
            return "Questo automa sorgente non è mai stato dichiarato precedentemente: "+lista_componenti[0]

        # verifico che l'automa destinazione esista
        automa_presente = [x for x in automi if x.nome == lista_componenti[2]]
        if (len(automa_presente) == 1):
            destinazione = automa_presente[0]
        else:
            return "Questo automa destinazione non è mai stato dichiarato precedentemente: "+lista_componenti[2]

        links.append(Link(lista_componenti[1], sorgente, destinazione))

    f.close()
    return links

def carica_rete_da_file_txt(automi, links, *args):
    '''Carica una rete da un file .txt
    devono essere forniti automi e links esistenti'''
    if len(args) == 1:
        f = open(args[0], "r")
    else:
        file = filedialog.askopenfilename()
        estensione = file.split(".")
        if len(estensione) != 2 or estensione[1] != "txt":
            return "Estensione del file errata. Seleziona un file .txt"
        f = open(file, "r")

    stringa_regex = f.read()
    x = re.fullmatch(REGEX_RETE, stringa_regex)
    if x:
        print("Inizio a leggere il file")
    else:
        print("problema nella lettura")
        return "Il formato del file non è corretto. Impossibile importarlo"
    f.close()

    if len(args)==1:
        f = open(args[0], "r")
    else:
        f = open(file, "r")    # Riga 1: "nome"\n
    riga = f.readline()
    rete = Rete(riga[:-1], automi, links)

    #Riga 2
    while (True):
        riga = f.readline()
        if not riga or riga == "\n":
            break
        riga = riga[:-1]  # tolgo\n
        componenti = riga.split(",")
        #automa1,t1,e1(L1)/{e1(L1);e2(L2)},o1,r1
        lista_componenti = []
        for c in componenti:
            lista_componenti.append(c)

        transizioni=[]
        for a in automi:
            transizioni+=get_transizioni(a)
        #componente 2: nome transizione
        transizione_presente = [x for x in transizioni if x.nome == lista_componenti[1]]
        if (len(transizione_presente) == 1):
            t = transizione_presente[0]
            t.osservazione = lista_componenti[3]
            t.rilevanza = lista_componenti[4]
        else:
            return "La seguente transizione non esiste: "+lista_componenti[1]

        #componente 1: nome automa

        #componente 3 eventi e link di ingresso e uscita
        eventi = lista_componenti[2].split("/")
        lista_eventi = []
        for e in eventi:
            lista_eventi.append(e)

        #Input
        if lista_eventi[0]!=" ":
            stringa = lista_eventi[0].split("(")
            nome_evento = stringa[0]
            nome_link = stringa[1][:-1]

            link_presente = [x for x in links if x.nome == nome_link]
            if (len(link_presente) == 1):
                link = link_presente[0]
                evento = Evento(nome_evento, link)
                t.add_input(evento)
                #t.osservazione = lista_componenti[3]
                #t.rilevanza = lista_componenti[4]
            else:
                return "Il seguente link non esiste: "+nome_link
        else:
            evento = Evento("")
            t.add_input(evento)

        # Output
        elenco_eventi = lista_eventi[1][1:-1] # tolgo le {
        if elenco_eventi != " ": # non vuoto
            eventi = elenco_eventi.split(";")

            for e in eventi:
                stringa = e.split("(")
                nome_evento = stringa[0]
                nome_link = stringa[1][:-1]

                link_presente = [x for x in links if x.nome == nome_link]
                if (len(link_presente) == 1):
                    link = link_presente[0]
                    evento = Evento(nome_evento, link)
                    t.add_output(evento)
                    #t.osservazione = lista_componenti[3]
                    #t.rilevanza = lista_componenti[4]
                else:
                    return "Il seguente link non esiste: "+nome_link
        else:
            evento = Evento("")
            t.add_output(evento)

    f.close()
    return rete

