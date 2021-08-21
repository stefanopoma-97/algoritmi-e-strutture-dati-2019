'''Modulo contenente i 3 algoritmo e le loro varianti'''

from Classi.Automa.automa import *
from Classi.Automa.rete import *
from Classi.GestioneFile.grafici import stampa_spazio_ridenominato_su_file
from Classi.Spazio.spazio_comportamentale import *
from copy import deepcopy

#ALGORITMO 1, manuale
def crea_spazio_comportamentale_manuale(rete, *args):
    '''Versione manuale dell'algoritmo per la creazione dello spazio comportamentale data una rete
    Input:
        *args: serve a passare informazioni dell'esecuzione precedente per poterla riprendere
            nodi = args[0]
            nodo_attuale = args[1]
            transizioni = args[2]
        '''

    #print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE MANUALMENTE")
    rete = rete

    if len(args)==0:
        #Salvo l'array degli automi presenti nella rete #rete.automi
        #Salvo l'array dei links presenti nella rete #rete.links
        #Salvo l'array delle transizioni presenti nella rete #rete.transizioni
        automi = rete.automi
        links = rete.links
        transizioni = rete.get_transizioni()

        #creo un array vuoto di nodi dello spazio comportamentale
        nodi = []
        nodi_da_scorrete = []

        #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
        nodo_attuale = istanzio_nodo_iniziale(rete)
        # print("Creo nodo iniziale:")
        # print("\t"+nodo_attuale.to_string()+"\n")

        #Inserisco il nodo iniziale nell'array
        nodi.append(nodo_attuale)
        #nodi_da_scorrete.append(nodo_attuale)

        transizioni=[]
    else:
        #print("RIPRENDO DA SITUAZIONE PRECEDENTE")

        nodi = args[0]
        nodo_attuale = args[1]
        transizioni = args[2]
        # print("numero nodi: " + str(len(nodi)))
        # print("Nodo Attuale: " + nodo_attuale.to_string())
        fine = False
        if nodo_attuale.check==True:
            fine = True
            for n in nodi:
                if n.check == False:
                    nodo_attuale=n
                    fine = False

        if fine:
            #print("FINE, non ci sono altri nodi da controllare FINE")
            return nodi, nodo_attuale, transizioni, True, "Non ci sono altri nodi da analizzare"



    out= controllo_transizioni_manualmente(nodi, nodo_attuale, transizioni)

    # sistema_transizioni(spazio)
    nodi = out[0]
    nodo_attuale = out[1]
    transizioni = out[2]
    commento = out[3]

    return nodi, nodo_attuale, transizioni, False, commento

def controllo_transizioni_manualmente(nodi, nodo_attuale, transizioni_spazio):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    # print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    # print("\t"+nodo_attuale.to_string()+"\n")

    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    #scorro gli stati
    for s in stati_correnti:
        # print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
        # print("il nodo ha transizioni: "+str(len(nodo_attuale.transizioni)))
        # print("stato: "+s.nome+"\n")

        #scorro transizioni dello stato
        for t in s.transizioni:
            # print("Scorro transizioni, in nodo numero: " +str(nodi.index(nodo_attuale)))
            # print("stato: " + t.nome+"\n")

            salto = False
            for t_spazio in transizioni_spazio:
                if t.nome == t_spazio.nome and t_spazio.nodo_sorgente==nodo_attuale:
                    salto = True
                    #print("Transizione già inserita la salto")

            if salto:
                print("la salto")
            else:
                # controllo se la transizione può scattare
                scatta = scatto_transizione(t, nodo_attuale)

                if (scatta):
                    # creo il nuovo nodo generato dallo scatto della transizione
                    #print("inizio a creare il nuovo nodo")
                    nuovo_nodo = deepcopy(nodo_attuale)
                    nuovo_nodo.iniziale = False
                    nuovo_nodo = aggiorna_nodo(nuovo_nodo, t)
                    nuovo_nodo.finale = nuovo_nodo.is_finale()
                    nuovo_nodo.output = nuovo_nodo.get_output()

                    # print("Nuovo nodo creato")
                    # print("\t" + nuovo_nodo.to_string() + "\n")
                    # controllo che il nodo sia nuovo
                    contiene = contiene_nodo(nuovo_nodo, nodi)
                    if (isinstance(contiene, Nodo)):
                        #print("Il nuovo nodo è già presente nella lista")
                        if contiene.iniziale:
                            contiene.finale = True
                        tra = crea_nuova_transizione(nodo_attuale, contiene, t)
                        transizioni_spazio.append(tra)
                        # nodo_attuale.transizioni.append(tra)
                        # print("Creata la nuova transizione: ")
                        # print("\t" + tra.to_string())
                        # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    else:
                        #print("Inserisco il nuovo nodo")
                        nodi.append(nuovo_nodo)
                        #print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                        tra = crea_nuova_transizione(nodo_attuale, nuovo_nodo, t)
                        transizioni_spazio.append(tra)
                        # nodo_attuale.transizioni.append(tra)
                        # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                        # print("Creata la nuova transizione: ")
                        # print("\t" + tra.to_string())
                        # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                        commento="creo transizione: "+tra.nome+", che si collega al nuovo nodo: ["+nuovo_nodo.output+"]"
                        return [nodi, nuovo_nodo, transizioni_spazio, commento]

                else:
                    print("La transizione non scatta, esco dal ciclo")


    #print("CHECKED ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True
    commento="analizzate tutte le possibili transizioni del nodo: ["+nodo_attuale.output+"]\n necessario passare al prossimo nodo"
    return [nodi, nodo_attuale, transizioni_spazio, commento]

#ALGORITMO 1
def crea_spazio_comportamentale(rete):
    '''Algorimto 1: data una rete genera lo spazio comportamentale'''

    print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE")
    print("RETE")
    print(rete.to_string())


    #creo un array vuoto di nodi dello spazio comportamentale
    nodi = []

    #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
    nodo_attuale = istanzio_nodo_iniziale(rete)

    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)

    transizioni=[]

    controllo_transizioni(nodi, nodo_attuale, transizioni)

    print("FINITO CONTROLLO")

    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)
    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)
    ridenominazione_spazio_appena_creato(spazio)

    del nodi
    del nodo_attuale
    del nodi_finali
    del nodi_iniziali

    return spazio

def ridenominazione_spazio_appena_creato(spazio):
    '''Procedura di ridenominazione dello spazio'''
    for i in range(len(spazio.nodi)):
        spazio.nodi[i].id = str(i)

def sistema_transizioni(spazio):
    '''Dato uno spazio va ad aggiungere le corrette transizioni nelle liste
    transizioni e transizioni_sorgente di ogni nodo'''
    #print("SISTEMA TRANSIZIONI SPAZIO")
    for n in spazio.nodi:
        n.transizioni = []
        n.transizioni_sorgente = []

    for t in spazio.transizioni:
        t.nodo_sorgente.transizioni.append(t)
        t.nodo_destinazione.transizioni_sorgente.append(t)

def controllo_transizioni(nodi, nodo_attuale, transizioni_spazio):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    # print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    # print("\t"+nodo_attuale.to_string()+"\n")

    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    #scorro gli stati
    for s in stati_correnti:
        # print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
        # print("il nodo ha transizioni (nodo attuale.transizioni): "+str(len(nodo_attuale.transizioni)))
        # print("FOR LOOP. stato: "+s.nome+"\n")

        #scorro transizioni dello stato
        for t in s.transizioni:
            # print("Scorro transizioni, in nodo numero (id): " +str(nodi.index(nodo_attuale)))
            # print("transizione: "+t.nome+"\n")

            #controllo se la transizione può scattare
            scatta = scatto_transizione(t, nodo_attuale)

            if(scatta):
                #creo il nuovo nodo generato dallo scatto della transizione
                #print("inizio a creare il nuovo nodo")
                nuovo_nodo = deepcopy(nodo_attuale)
                nuovo_nodo.iniziale = False
                nuovo_nodo = aggiorna_nodo(nuovo_nodo, t)
                nuovo_nodo.finale = nuovo_nodo.is_finale()
                nuovo_nodo.output = nuovo_nodo.get_output()

                #print("Nuovo nodo creato")
                #print("\t" + nuovo_nodo.to_string() + "\n")
                #controllo che il nodo sia nuovo
                contiene = contiene_nodo(nuovo_nodo, nodi)
                if (isinstance(contiene, Nodo)):
                    #print("Il nuovo nodo è già presente nella lista")
                    if contiene.iniziale:
                        contiene.finale = True
                    tra = crea_nuova_transizione(nodo_attuale, contiene, t)
                    transizioni_spazio.append(tra)
                    #nodo_attuale.transizioni.append(tra)
                    # print("Creata la nuova transizione: ")
                    # print("\t"+tra.to_string())
                    # print("numero totale di transizioni: "+str(len(transizioni_spazio)))
                else:
                    #print("Inserisco il nuovo nodo")
                    nodi.append(nuovo_nodo)
                    #print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                    tra = crea_nuova_transizione(nodo_attuale, nuovo_nodo, t)
                    transizioni_spazio.append(tra)
                    #nodo_attuale.transizioni.append(tra)
                    # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    # print("Creata la nuova transizione: ")
                    # print("\t" + tra.to_string())
                    # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    controllo_transizioni(nodi, nuovo_nodo, transizioni_spazio)

            else:
                print("La transizione non scatta, esco dal ciclo")

    #print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True

def crea_nuova_transizione(sorgente, destinazione, transizione):
    nuova_transizione = Transizione_spazio(transizione.nome, sorgente, destinazione, transizione.osservazione, transizione.rilevanza)
    return nuova_transizione

def aggiorna_nodo(nodo, transizione):
    '''dato un nodo e una transizione, la transizione viene fatta scattare la transizione aggiornando il nodo stesso
    gli eventi in transizione.input vanno a togliere l'evento nel dizionario del nodo
    es.
        evento="e1" su Link1
        links: [Link1,"e1"] -> links: [Link1, ""]

    Gli eventi in transizione.output invece vanno ad inserire il nome dell'evento nella relativa stringa del dizionario links
    es.
        evento="e2" su Link2
        links: [Link2, ""] -> links: [Link2, "e2"]

    Allo stesso tempo lo stato sorgente del nodo viene aggiornato con lo stato destinazione presente nella transizione'''


    #print("aggiorno i valori del nuovo nodo")
    #scorro eventi di input
    for evento in transizione.input:
        #print("input")
        if (evento.nome != "" and evento.link != None):
            #tolgo i valori dai link di input
            nodo.links[evento.link.nome][1]=""
            #print("ho aggiornato "+evento.link.nome+" mettendolo a "+ nodo.links[evento.link.nome][1])
    for evento in transizione.output:
        #print("output")
        if (evento.nome != "" and evento.link != None):
            #inserisco l'evento nel link di output
            nodo.links[evento.link.nome][1]=evento.nome
            #print("ho aggiornato "+evento.link.nome+" mettendolo a "+ nodo.links[evento.link.nome][1])


    #ricavo la posizione dello stato sorgente
    for index, s in enumerate(nodo.stati):
        #print("Scorro stato: "+s.to_string()+" = "+str(s))
        #print("devo confrontarlo con: "+transizione.stato_sorgente.to_string()+" = "+str(transizione.stato_sorgente))
        if s.id == transizione.stato_sorgente.id:
            #print("ho aggiornato lo stato "+nodo.stati[index].nome)
            nodo.stati[index] = transizione.stato_destinazione
            #print(" mettendolo a " +nodo.stati[index].nome)

    return nodo

def scatto_transizione(tranizione, nodo):
    '''data una transizione e il nodo attuale viene stabilito se la transizione può scattare
    vengono fatte analisi solo sugli eventi presenti nei link
    non sullo stato di partenza della transizione'''
    scatta=True
    #print("Controllo transizione: "+tranizione.nome)

    #scorro eventi in input della transizione
    for evento in tranizione.input:
        #print("controllo INPUT")
        #verifico che non sia un evento vuoto
        if(evento.nome != "" and evento.link != None):
            #ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            #print("Evento: "+evento.nome+" ("+evento.link.nome+") -> valore nel nodo: "+valore_nel_link)

            if (evento.nome != valore_nel_link):
                #print("Non c'è l'input corretto, la transizione non può scattare\n")
                return False

    # scorro eventi in output della transizione
    for evento in tranizione.output:
        #print("controllo Output")
        # verifico che non sia un evento vuoto
        if (evento.nome != "" and evento.link != None):
            # ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            #print("Evento: " + evento.nome + " (" + evento.link.nome + ") -> valore nel nodo: " + valore_nel_link)

            if (valore_nel_link != ""):
                #print("Il link di output non è vuoto, impossibile scattare\n")
                return False
    #print("La transizione può scattare\n")
    return scatta

def istanzio_nodo_iniziale(rete):
    '''Partendo dalla rete creo l'istanza del nodo iniziale dello spazio comportamentale'''
    stati_correnti = rete.get_stati_correnti() #ricavo gli stati correnti da tutta la rete
    links = dict()
    for l in rete.links:
        links[l.nome] = [l, l.evento.nome]

    nodo_iniziale = Nodo(stati=stati_correnti, check=False, links=links, iniziale=True)
    return nodo_iniziale


#ALGORITMO1 MIGLIORATO
def crea_spazio_comportamentale_migliorato(rete):
    '''Algorimto 1: data una rete genera lo spazio comportamentale'''

    # print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE")
    # print("RETE")
    # print(rete.to_string())


    #creo un array vuoto di nodi dello spazio comportamentale
    nodi = []

    #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
    nodo_attuale = istanzio_nodo_iniziale(rete)

    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)

    transizioni=[]

    controllo_transizioni_migliorato(nodi, nodo_attuale, transizioni)

    #print("FINITO CONTROLLO")

    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)
    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)
    ridenominazione_spazio_appena_creato(spazio)

    del nodi
    del transizioni
    del nodo_attuale
    del nodi_finali
    del nodi_iniziali

    return spazio

def controllo_transizioni_migliorato(nodi, nodo_attuale, transizioni_spazio):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    # print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    # print("\t"+nodo_attuale.to_string()+"\n")

    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    #scorro gli stati
    for s in stati_correnti:
        # print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
        # print("il nodo ha transizioni (nodo attuale.transizioni): "+str(len(nodo_attuale.transizioni)))
        # print("FOR LOOP. stato: "+s.nome+"\n")

        #scorro transizioni dello stato
        for t in s.transizioni:
            # print("Scorro transizioni, in nodo numero (id): " +str(nodi.index(nodo_attuale)))
            # print("transizione: "+t.nome+"\n")

            #controllo se la transizione può scattare
            scatta = scatto_transizione_migliorato(t, nodo_attuale)

            if(isinstance(scatta, Nodo)):
                #creo il nuovo nodo generato dallo scatto della transizione
                nuovo_nodo = scatta

                # print("Nuovo nodo creato")
                # print("\t" + nuovo_nodo.to_string() + "\n")
                #controllo che il nodo sia nuovo
                contiene = contiene_nodo(nuovo_nodo, nodi)
                if (isinstance(contiene, Nodo)):
                    #print("Il nuovo nodo è già presente nella lista")
                    if contiene.iniziale:
                        contiene.finale = True
                    tra = crea_nuova_transizione(nodo_attuale, contiene, t)
                    transizioni_spazio.append(tra)
                    #nodo_attuale.transizioni.append(tra)
                    # print("Creata la nuova transizione: ")
                    # print("\t"+tra.to_string())
                    # print("numero totale di transizioni: "+str(len(transizioni_spazio)))
                else:
                    #print("Inserisco il nuovo nodo")
                    nodi.append(nuovo_nodo)
                    #print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                    tra = crea_nuova_transizione(nodo_attuale, nuovo_nodo, t)
                    transizioni_spazio.append(tra)
                    #nodo_attuale.transizioni.append(tra)
                    # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    # print("Creata la nuova transizione: ")
                    # print("\t" + tra.to_string())
                    # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    controllo_transizioni(nodi, nuovo_nodo, transizioni_spazio)

            else:
                print("La transizione non scatta, esco dal ciclo")

    #print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True


def scatto_transizione_migliorato(transizione, nodo):
    '''data una transizione e il nodo attuale viene stabilito se la transizione può scattare
    vengono fatte analisi solo sugli eventi presenti nei link
    non sullo stato di partenza della transizione'''
    scatta=True
    print("Controllo transizione: "+transizione.nome)
    nuovo_nodo = deepcopy(nodo)
    nuovo_nodo.iniziale = False

    #scorro eventi in input della transizione
    for evento in transizione.input:
        print("controllo INPUT")
        #verifico che non sia un evento vuoto
        if(evento.nome != "" and evento.link != None):
            #ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            #print("Evento: "+evento.nome+" ("+evento.link.nome+") -> valore nel nodo: "+valore_nel_link)

            if (evento.nome != valore_nel_link):
                #print("Non c'è l'input corretto, la transizione non può scattare\n")
                return False
            else:
                nuovo_nodo.links[evento.link.nome][1] = ""


    # scorro eventi in output della transizione
    for evento in transizione.output:
        #print("controllo Output")
        # verifico che non sia un evento vuoto
        if (evento.nome != "" and evento.link != None):
            # ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            #print("Evento: " + evento.nome + " (" + evento.link.nome + ") -> valore nel nodo: " + valore_nel_link)

            if (valore_nel_link != ""):
                #print("Il link di output non è vuoto, impossibile scattare\n")
                return False
            else:
                nuovo_nodo.links[evento.link.nome][1] = evento.nome

    # ricavo la posizione dello stato sorgente
    for index, s in enumerate(nuovo_nodo.stati):
        #print("Scorro stato: "+s.to_string()+" = "+str(s))
        #print("devo confrontarlo con: "+transizione.stato_sorgente.to_string()+" = "+str(transizione.stato_sorgente))
        if s.id == transizione.stato_sorgente.id:
            #print("ho aggiornato lo stato "+nuovo_nodo.stati[index].nome)
            nuovo_nodo.stati[index] = transizione.stato_destinazione
            #print(" mettendolo a " +nuovo_nodo.stati[index].nome)

    nuovo_nodo.finale = nuovo_nodo.is_finale()
    nuovo_nodo.output = nuovo_nodo.get_output()
    return nuovo_nodo


#ALGORITMO 1 NON RICORSIVO
def crea_spazio_comportamentale_non_ricorsivo(rete):
    '''Algorimto 1: data una rete genera lo spazio comportamentale'''

    print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE")
    print("RETE")


    #creo un array vuoto di nodi dello spazio comportamentale
    nodi = []

    #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
    nodo_attuale = istanzio_nodo_iniziale(rete)

    nodo_attuale.check = False

    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)

    transizioni=[]

    controllo_transizioni_non_ricorsivo(nodi, transizioni)

    print("FINITO CONTROLLO")

    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)
    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)
    ridenominazione_spazio_appena_creato(spazio)

    del nodi
    del nodo_attuale
    del nodi_finali
    del nodi_iniziali

    return spazio

def controllo_transizioni_non_ricorsivo(nodi, transizioni_spazio):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''

    lista_nodi= [nodi[0]]
    #i=0
    while(len(lista_nodi)>=1):
        #print("CI sono nodi NON controllati")
        nodo_attuale=lista_nodi[0]
        #print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
        #print("\t"+nodo_attuale.to_string()+"\n")

        #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
        stati_correnti = nodo_attuale.stati

        #scorro gli stati
        for s in stati_correnti:
            # print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
            # print("il nodo ha transizioni (nodo attuale.transizioni): "+str(len(nodo_attuale.transizioni)))
            # print("FOR LOOP. stato: "+s.nome+"\n")

            # scorro transizioni dello stato
            for t in s.transizioni:
                # print("Scorro transizioni, in nodo numero (id): " +str(nodi.index(nodo_attuale)))
                # print("transizione: "+t.nome+"\n")

                # controllo se la transizione può scattare
                scatta = scatto_transizione(t, nodo_attuale)

                if (scatta):
                    # creo il nuovo nodo generato dallo scatto della transizione
                    # print("inizio a creare il nuovo nodo")
                    nuovo_nodo = deepcopy(nodo_attuale)
                    nuovo_nodo.iniziale = False
                    nuovo_nodo = aggiorna_nodo(nuovo_nodo, t)
                    nuovo_nodo.finale = nuovo_nodo.is_finale()
                    nuovo_nodo.output = nuovo_nodo.get_output()

                    # print("Nuovo nodo creato")
                    # print("\t" + nuovo_nodo.to_string() + "\n")
                    # controllo che il nodo sia nuovo
                    contiene = contiene_nodo(nuovo_nodo, nodi)
                    if (isinstance(contiene, Nodo)):
                        # print("Il nuovo nodo è già presente nella lista")
                        if contiene.iniziale:
                            contiene.finale = True
                        tra = crea_nuova_transizione(nodo_attuale, contiene, t)
                        transizioni_spazio.append(tra)
                        # nodo_attuale.transizioni.append(tra)
                        # print("Creata la nuova transizione: ")
                        # print("\t"+tra.to_string())
                        # print("numero totale di transizioni: "+str(len(transizioni_spazio)))
                    else:
                        # print("Inserisco il nuovo nodo")
                        nuovo_nodo.check=False
                        nodi.append(nuovo_nodo)
                        #lista_nodi.append(nuovo_nodo)
                        # print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                        tra = crea_nuova_transizione(nodo_attuale, nuovo_nodo, t)
                        transizioni_spazio.append(tra)
                        # nodo_attuale.transizioni.append(tra)
                        # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                        # print("Creata la nuova transizione: ")
                        # print("\t" + tra.to_string())
                        # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                        controllo_transizioni(nodi, nuovo_nodo, transizioni_spazio)

                else:
                    print("La transizione non scatta, esco dal ciclo")

        #print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))


        nodo_attuale.check = True
        lista_nodi = [x for x in nodi if x.check == False]


        #print("\n\n\n\n\n-------------------------- iterazioni: " + str(i))
        #i=i+1


def crea_spazio_comportamentale_non_ricorsivo2(nodo):
    '''Algorimto 1: data una rete genera lo spazio comportamentale'''

    print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE")
    print("RETE")


    #creo un array vuoto di nodi dello spazio comportamentale
    nodi = []

    #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
    nodo_attuale = nodo
    nodo_attuale.check=False

    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)

    transizioni=[]

    controllo_transizioni_non_ricorsivo2(nodi, transizioni)

    print("FINITO CONTROLLO")

    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)
    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)
    ridenominazione_spazio_appena_creato(spazio)
    #
    del nodi
    del transizioni
    # del nodo_attuale
    # del nodi_finali
    # del nodi_iniziali
    #
    return spazio

def controllo_transizioni_non_ricorsivo2(nodi, transizioni_spazio):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''

    lista_nodi=[x for x in nodi if x.check==False]
    i=0
    while(len(lista_nodi)>=1):
    #while (i<=14):
        print("CI sono nodi NON controllati")
        nodo_attuale=lista_nodi[0]
        print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
        print("\t"+nodo_attuale.to_string()+"\n")

        #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
        stati_correnti = nodo_attuale.stati

        #scorro gli stati
        for s in stati_correnti:
            print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
            print("il nodo ha transizioni (nodo attuale.transizioni): "+str(len(nodo_attuale.transizioni)))
            print("FOR LOOP. stato: "+s.nome+"\n")

            #scorro transizioni dello stato
            for t in s.transizioni:
                print("Scorro transizioni, in nodo numero (id): " +str(nodi.index(nodo_attuale)))
                print("transizione: "+t.nome+"\n")

                #controllo se la transizione può scattare
                scatta = scatto_transizione_migliorato(t, nodo_attuale)

                #scatta = deepcopy(nodo_attuale)

                if(isinstance(scatta, Nodo)):
                    #creo il nuovo nodo generato dallo scatto della transizione
                    nuovo_nodo = scatta

                    print("Nuovo nodo creato")
                    print("\t" + nuovo_nodo.to_string() + "\n")
                    #controllo che il nodo sia nuovo
                    contiene = contiene_nodo(nuovo_nodo, nodi)
                    if (isinstance(contiene, Nodo)):
                        print("Il nuovo nodo è già presente nella lista")
                        if contiene.iniziale:
                            contiene.finale = True
                        tra = crea_nuova_transizione(nodo_attuale, contiene, t)
                        transizioni_spazio.append(tra)

                        print("Creata la nuova transizione: ")
                        print("\t"+tra.to_string())
                        print("numero totale di transizioni: "+str(len(transizioni_spazio)))
                    else:
                        print("Inserisco il nuovo nodo")
                        nuovo_nodo.check=False
                        nodi.append(nuovo_nodo)
                        print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                        tra = crea_nuova_transizione(nodo_attuale, nuovo_nodo, t)
                        transizioni_spazio.append(tra)
                        #nodo_attuale.transizioni.append(tra)
                        print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                        print("Creata la nuova transizione: ")
                        print("\t" + tra.to_string())
                        print("numero totale di transizioni: " + str(len(transizioni_spazio)))

                else:
                    print("La transizione non scatta, esco dal ciclo")

        print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
        nodo_attuale.check = True
        lista_nodi = [x for x in nodi if x.check == False]
        # if i<8:
        #     lista_nodi = [x for x in nodi if x.check == False]
        # else:
        #     lista_nodi = [x for x in nodi]
        print("\n\n\n\n\n-------------------------- iterazioni: " + str(i))
        i=i+1






#--------------------------------------------------------
#ALGORITMO 2 - da spazio, Manuale
def sistema_transizioni2(spazio):
    #print("SISTEMA TRANSIZIONI SPAZIO")

    # prima svuoto transizioni dai nodi però
    for n in spazio.nodi:
        n.transizioni = []
        n.transizioni_sorgente = []

    for t in spazio.transizioni:
        t.nodo_sorgente.transizioni.append(t)
        t.nodo_destinazione.transizioni_sorgente.append(t)

def crea_spazio_comportamentale_manuale2_da_spazio(spazio, osservazione, *args):
    '''Algoritmo 2, svolto partendo da uno spazio importato'''

    #print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE DA OSSERVAZIONE MANUALMENTE")
    spazio = spazio

    if len(args)==0:

        # creo un array vuoto di nodi dello spazio comportamentale
        nodi = []

        nodo_attuale = spazio.nodi[0]
        for n in spazio.nodi:
            n.lunghezza_osservazione = 0
        nodo_attuale.lunghezza_osservazione = 0

        nodo_attuale.finale = False

        # print("Nodo Attuale: " + nodo_attuale.to_string())
        # print("SUE TRANSIZIONI: ")
        # for t in nodo_attuale.transizioni:
        #     print(t.nome)
        # Inserisco il nodo iniziale nell'array
        nodi.append(nodo_attuale)
        #print("Creata lista di nodi\n")
        transizioni = []
        global indice
        indice = 0


    else:
        #print("RIPRENDO DA SITUAZIONE PRECEDENTE")

        nodi = args[0]
        nodo_attuale = args[1]
        transizioni = args[2]
        # print("numero nodi: " + str(len(nodi)))
        # print("Nodo Attuale: " + nodo_attuale.to_string())
        # print("SUE TRANSIZIONI: ")
        # for t in nodo_attuale.transizioni:
        #     print(t.nome)
        fine = False
        if nodo_attuale.check==True:
            fine = True
            for n in nodi:
                if n.check == False:
                    nodo_attuale=n
                    fine = False

        if fine:
            #print("FINE, non ci sono altri nodi da controllare FINE")
            return nodi, nodo_attuale, transizioni, True, "Non ci sono altri nodi da analizzare"



    out= controllo_transizioni_manualmente2_da_spazio(nodi, nodo_attuale, transizioni, osservazione, spazio)

    nodi = out[0]
    nodo_attuale = out[1]
    transizioni = out[2]
    commento = out[3]

    return nodi, nodo_attuale, transizioni, False, commento

def controllo_transizioni_manualmente2_da_spazio(nodi, nodo_attuale, transizioni_spazio, osservazione, spazio):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''


    nodo=nodo_attuale
    # print("ANALIZZO NODO")
    # print("NODO: " + nodo.to_string())

    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    for t in nodo.transizioni:
        # print("FOR transizioni")
        # print("nodo: " + nodo.to_string())
        # print("transizione: " + t.nome)


        #serve a non ripetere stessa transizione
        salto=False
        for t_spazio in transizioni_spazio:
            if t.nome == t_spazio.nome and t_spazio.nodo_sorgente==nodo_attuale:
                salto = True
                #print("Transizione già inserita la salto")

        if salto:
            print("la salto")
        else:
            # controllo se la transizione può scattare
            scatta = scatto_transizione2_da_spazio(t, nodo, osservazione)

            if (scatta):

                #print("inizio a creare il nuovo nodo")
                if t.osservazione != " ":
                    nodo.passata_osservazione = True

                # calcolo indice nuovo nodo
                if t.osservazione != " ":
                    #print("La transizione ha un valore di osservazione: " + t.osservazione)
                    indice = nodo.lunghezza_osservazione + 1
                    #print("Aggiornato il valore del nuovo nodo di l_osservazione")
                else:
                    indice = nodo.lunghezza_osservazione

                nuovo_nodo = deepcopy(t.nodo_destinazione)
                nuovo_nodo.lunghezza_osservazione = indice
                contiene = contiene_nodo(nuovo_nodo, nodi)

                if (isinstance(contiene, Nodo)):
                    # print("Voglio creare nuovo nodo: " + nuovo_nodo.to_string())
                    # print("il nodo destinazione esiste già")
                    # print("Eccolo: " + contiene.to_string())
                    if contiene.lunghezza_osservazione == indice:
                        #print("effettivamente è lo stesso nodo")
                        if contiene.iniziale and contiene.lunghezza_osservazione == len(osservazione):
                            contiene.finale = True
                        # print("CREO TRANSIZIONE:")
                        # print(t.nome + " ,da: " + nodo.output + " a:" + nuovo_nodo.output)
                        tra = Transizione_spazio(t.nome, nodo, contiene, t.osservazione, t.rilevanza)
                        transizioni_spazio.append(tra)

                        # print("Inserita la nuova transizione: ")
                        # print("\t" + t.to_string())
                        # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    else:
                        #print("l'indice è diverso, verrà creato un nodo separato")
                        # nuovo_nodo = deepcopy(t.nodo_destinazione)
                        nuovo_nodo = Nodo(t.nodo_destinazione.stati, False, t.nodo_destinazione.links, False, [])
                        nuovo_nodo.iniziale = False
                        nuovo_nodo.check = False
                        nuovo_nodo.finale = False
                        nuovo_nodo.lunghezza_osservazione = indice
                        nuovo_nodo.passata_osservazione = False

                        # nuovo
                        nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                        nuovo_nodo.output = nuovo_nodo.get_output()
                        nodi.append(nuovo_nodo)
                        # print("CREO TRANSIZIONE:")
                        # print(t.nome+" ,da: "+nodo.output+" a:"+nuovo_nodo.output)
                        tra = Transizione_spazio(t.nome, nodo, nuovo_nodo, t.osservazione, t.rilevanza)
                        transizioni_spazio.append(tra)

                        # print("Nuovo nodo (aggiornato) creato ")
                        # print("\t" + nuovo_nodo.to_string() + "\n")
                        commento = "creo transizione: " + tra.nome + ", che si collega al nuovo nodo: [" + nuovo_nodo.output + "]"
                        return [nodi, nuovo_nodo, transizioni_spazio, commento]
                else:
                    #print("Inserisco il nuovo nodo")

                    nuovo_nodo.iniziale = False
                    nuovo_nodo.check = False
                    nuovo_nodo.finale = False
                    nuovo_nodo.lunghezza_osservazione = indice
                    nuovo_nodo.passata_osservazione = False
                    nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                    nuovo_nodo.output = nuovo_nodo.get_output()

                    nodi.append(nuovo_nodo)
                    # print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                    # print("NUOVO NODO")
                    # print(nuovo_nodo.to_string())
                    # print("SUE TRANSIZIONI")
                    # for tn in nuovo_nodo.transizioni:
                    #     print(tn.nome)
                    #print("CREO TRANSIZIONE:")
                    #print(t.nome + " ,da: " + nodo.output + " a:" + nuovo_nodo.output)
                    tra = Transizione_spazio(t.nome, nodo, nuovo_nodo, t.osservazione, t.rilevanza)
                    transizioni_spazio.append(tra)
                    # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    # print("Creata la nuova transizione: ")
                    # print("\t" + t.to_string())
                    commento = "creo transizione: " + tra.nome + ", che si collega al nuovo nodo: [" + nuovo_nodo.output + "]"
                    return [nodi, nuovo_nodo, transizioni_spazio, commento]
            else:
                print("La transizione non scatta, esco dal ciclo")


    #print("CHECKED ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo.check = True
    commento="analizzate tutte le possibili transizioni del nodo: ["+nodo.output+"]\n necessario passare al prossimo nodo"
    return [nodi, nodo, transizioni_spazio, commento]

#ALGORITMO 2 - da spazio
def crea_spazio_comportamentale2_da_spazio(spazio, osservazione):

    #print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE CON OSSERVAZIONE DA SPAZIO")
    #spazio = spazio
    #osservazione=osservazione

    #creo un array vuoto di nodi dello spazio comportamentale
    nodi = []

    #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
    nodo_attuale = spazio.nodi[0]
    for n in spazio.nodi:
        n.lunghezza_osservazione=0
    nodo_attuale.lunghezza_osservazione=0

    nodo_attuale.finale=False
    # print("Creo nodo iniziale:")
    # print("\t"+nodo_attuale.to_string()+"\n")


    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)
    #print("Creata lista di nodi\n")
    transizioni=[]


    controllo_transizioni2_da_spazio(nodi, transizioni, osservazione, nodo_attuale)

    # print("VEDO TRANSIZIONI CREATE")
    # for t in transizioni:
    #     print(t.to_string())

    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)
    spazio_out = Spazio_comportamentale(spazio.nome, nodi_finali, nodi_iniziali, nodi, transizioni)
    #print("Sistema transizioni")
    sistema_transizioni2(spazio_out)
    #print("ridenominazione")
    ridenominazione_spazio_appena_creato(spazio_out)
    #print("FINE CREAZIONE SPAZIO COMPORTAMENTALE")
    return spazio_out

def controllo_transizioni2_da_spazio(nodi, transizioni_spazio, osservazione, nodo_attuale):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    nodo=nodo_attuale
    #scorro nodi
    # print("ANALIZZO NODO")
    # print("NODO: "+nodo.to_string())


    #scorro transizioni dello stato
    for t in nodo.transizioni:
        # print("FOR transizioni")
        # print("nodo: "+nodo.to_string())
        # print("transizione: "+t.nome)

        #controllo se la transizione può scattare
        scatta = scatto_transizione2_da_spazio(t, nodo, osservazione)

        if(scatta):
            #creo il nuovo nodo generato dallo scatto della transizione
            #print("inizio a creare il nuovo nodo")
            if t.osservazione!=" ":
                nodo.passata_osservazione=True

            #calcolo indice nuovo nodo
            if t.osservazione != " ":
                #print("La transizione ha un valore di osservazione: " + t.osservazione)
                indice=nodo.lunghezza_osservazione + 1
                #print("Aggiornato il valore del nuovo nodo di l_osservazione")
            else:
                indice = nodo.lunghezza_osservazione

            nuovo_nodo = deepcopy(t.nodo_destinazione)
            nuovo_nodo.lunghezza_osservazione=indice
            contiene = contiene_nodo(nuovo_nodo, nodi)
            if (isinstance(contiene, Nodo)):

                #IL nodo è presente e ha anche lo stesso valore di l_osservazione
                if contiene.lunghezza_osservazione==indice:
                    if contiene.iniziale and contiene.lunghezza_osservazione == len(osservazione):
                        contiene.finale = True
                    tra = Transizione_spazio(t.nome, nodo, contiene, t.osservazione, t.rilevanza)
                    transizioni_spazio.append(tra)

                    # print("Inserita la nuova transizione: ")
                    # print("\t" + t.to_string())
                    # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                else:
                    #l_osservazione è diverso. Creo nodo sepratato
                    nuovo_nodo = Nodo(t.nodo_destinazione.stati, False, t.nodo_destinazione.links, False, []) #stati, check, links, iniziale, transizioni=[], *args):

                    nuovo_nodo.iniziale=False
                    nuovo_nodo.check = False
                    nuovo_nodo.finale=False
                    nuovo_nodo.lunghezza_osservazione=indice
                    nuovo_nodo.passata_osservazione=False

                    #nuovo
                    nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                    nuovo_nodo.output = nuovo_nodo.get_output()
                    nodi.append(nuovo_nodo)
                    tra = Transizione_spazio(t.nome, nodo, nuovo_nodo, t.osservazione, t.rilevanza)
                    transizioni_spazio.append(tra)


                    #controllo_transizioni2_da_spazio(nodi, transizioni_spazio, osservazione, spazio, nuovo_nodo)


            else:
                #print("Inserisco il nuovo nodo")

                nuovo_nodo.iniziale = False
                nuovo_nodo.check = False
                nuovo_nodo.finale = False
                nuovo_nodo.lunghezza_osservazione = indice
                nuovo_nodo.passata_osservazione = False
                nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                nuovo_nodo.output = nuovo_nodo.get_output()

                nodi.append(nuovo_nodo)
                #print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                tra = Transizione_spazio(t.nome, nodo, nuovo_nodo, t.osservazione, t.rilevanza)
                transizioni_spazio.append(tra)
                #nodo_attuale.transizioni.append(tra)
                # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                # print("Creata la nuova transizione: ")
                # print("\t" + t.to_string())
                # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                controllo_transizioni2_da_spazio(nodi, transizioni_spazio, osservazione, nuovo_nodo)

        else:
            print("La transizione non scatta, esco dal ciclo")
    #print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo)))
    nodo.check = True

def scatto_transizione2_da_spazio(transizione, nodo, osservazioni):
    '''data una transizione e il nodo attuale viene stabilito se la transizione può scattare
    vengono fatte analisi solo sugli eventi presenti nei link
    non sullo stato di partenza della transizione'''
    scatta=True
    #print("Controllo transizione: "+transizione.nome)


    if transizione.osservazione != " ":
        # print("La transizione contiene un valore di osservazione: "+transizione.osservazione)
        # print("Osservazioni con lunghezza: "+str(len(osservazioni)))
        # print("Valore di l_osservazione nel nodo: " + str(nodo.lunghezza_osservazione))


        if nodo.lunghezza_osservazione == len(osservazioni):
            #print("len osservazione è già uguale a: " + str(nodo.lunghezza_osservazione) + ", non posso aggiungerne altre")
            return False
        else:
            if(osservazioni[nodo.lunghezza_osservazione]!=transizione.osservazione):
                # print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
                # print("La transizione ha il seguente valore: "+transizione.osservazione)
                # print("NON coincidono")
                return False
            #else:
                # print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
                # print("La transizione ha il seguente valore: " + transizione.osservazione)
                #print("Coincidono")

        if nodo.passata_osservazione:
            # print("IL nodo ha già una transizione uscente con l'etichetta di osservazione cercata")
            # print("NON SCATTA")
            return False


    return scatta



#ALGORITMO 2 - da rete, Manuale
def crea_spazio_comportamentale_manuale2(rete, osservazione, *args):

    #print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE DA OSSERVAZIONE MANUALMENTE")
    rete = rete

    if len(args)==0:

        # creo un array vuoto di nodi dello spazio comportamentale
        nodi = []

        nodo_attuale = istanzio_nodo_iniziale2(rete)
        #print("Creo nodo iniziale:")
        #print("\t" + nodo_attuale.to_string() + "\n")

        # Inserisco il nodo iniziale nell'array
        nodi.append(nodo_attuale)
        #print("Creata lista di nodi\n")
        transizioni = []
        global indice
        indice = 0


    else:
        #print("RIPRENDO DA SITUAZIONE PRECEDENTE")

        nodi = args[0]
        nodo_attuale = args[1]
        transizioni = args[2]
        # print("numero nodi: " + str(len(nodi)))
        # print("Nodo Attuale: " + nodo_attuale.to_string())
        fine = False
        if nodo_attuale.check==True:
            fine = True
            for n in nodi:
                if n.check == False:
                    nodo_attuale=n
                    fine = False

        if fine:
            #print("FINE, non ci sono altri nodi da controllare FINE")
            return nodi, nodo_attuale, transizioni, True, "Non ci sono altri nodi da analizzare"



    out= controllo_transizioni_manualmente2(nodi, nodo_attuale, transizioni, osservazione)

    nodi = out[0]
    nodo_attuale = out[1]
    transizioni = out[2]
    commento = out[3]

    return nodi, nodo_attuale, transizioni, False, commento

def controllo_transizioni_manualmente2(nodi, nodo_attuale, transizioni_spazio, osservazione):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    # print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    # print("\t"+nodo_attuale.to_string()+"\n")

    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    #scorro gli stati
    for s in stati_correnti:
        # print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
        # print("il nodo ha transizioni: "+str(len(nodo_attuale.transizioni)))
        # print("stato: "+s.nome+"\n")

        #scorro transizioni dello stato
        for t in s.transizioni:
            # print("Scorro transizioni, in nodo numero: " +str(nodi.index(nodo_attuale)))
            # print("stato: " + t.nome+"\n")

            #serve a non ripetere stessa transizione
            salto=False
            for t_spazio in transizioni_spazio:
                if t.nome == t_spazio.nome and t_spazio.nodo_sorgente==nodo_attuale:
                    salto = True
                    #print("Transizione già inserita la salto")

            if salto:
                print("la salto")
            else:
                # controllo se la transizione può scattare
                scatta = scatto_transizione2(t, nodo_attuale, osservazione)

                if (scatta):

                    # creo il nuovo nodo generato dallo scatto della transizione
                    #print("inizio a creare il nuovo nodo")
                    if t.osservazione != " ":
                        nodo_attuale.passata_osservazione = True
                        listOfGlobals = globals()
                        listOfGlobals['indice'] = listOfGlobals['indice'] + 1
                    nuovo_nodo = deepcopy(nodo_attuale)
                    nuovo_nodo.iniziale = False
                    nuovo_nodo.passata_osservazione = False
                    nuovo_nodo = aggiorna_nodo2(nuovo_nodo, t, nodo_attuale.lunghezza_osservazione)
                    # nuovo
                    nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                    nuovo_nodo.output = nuovo_nodo.get_output()

                    #print("Nuovo nodo creato")


                    #print("\t" + nuovo_nodo.to_string() + "\n")
                    # controllo che il nodo sia nuovo
                    contiene = contiene_nodo_con_osservazione(nuovo_nodo, nodi)

                    if (isinstance(contiene, Nodo)):
                        #print("Il nuovo nodo è già presente nella lista")
                        if contiene.iniziale and contiene.lunghezza_osservazione == len(osservazione):
                            contiene.finale = True
                        #print("aggionro l_osservazione del vecchio nodo")
                        contiene.lunghezza_osservazione = nuovo_nodo.lunghezza_osservazione
                        tra = crea_nuova_transizione(nodo_attuale, contiene, t)
                        transizioni_spazio.append(tra)
                        # nodo_attuale.transizioni.append(tra)
                    #     print("Creata la nuova transizione: ")
                    #     print("\t" + tra.to_string())
                    #     print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    else:
                        #print("Inserisco il nuovo nodo")
                        nodi.append(nuovo_nodo)
                        #print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                        tra = crea_nuova_transizione(nodo_attuale, nuovo_nodo, t)
                        transizioni_spazio.append(tra)
                        # nodo_attuale.transizioni.append(tra)
                        # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                        # print("Creata la nuova transizione: ")
                        # print("\t" + tra.to_string())
                        # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                        commento = "creo transizione: " + tra.nome + ", che si collega al nuovo nodo: [" + nuovo_nodo.output + "]"
                        return [nodi, nuovo_nodo, transizioni_spazio, commento]
                else:
                    print("La transizione non scatta, esco dal ciclo")


    #print("CHECKED ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True
    commento="analizzate tutte le possibili transizioni del nodo: ["+nodo_attuale.output+"]\n necessario passare al prossimo nodo"
    return [nodi, nodo_attuale, transizioni_spazio, commento]



#ALGORITMO 2 - da rete
def crea_spazio_comportamentale2(rete, osservazione):

    #print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE CON OSSERVAZIONE")
    rete = rete
    osservazione=osservazione

    #Salvo l'array degli automi presenti nella rete #rete.automi
    #Salvo l'array dei links presenti nella rete #rete.links
    #Salvo l'array delle transizioni presenti nella rete #rete.transizioni
    automi = rete.automi
    links = rete.links
    transizioni = rete.get_transizioni()

    #creo un array vuoto di nodi dello spazio comportamentale
    nodi = []

    #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
    nodo_attuale = istanzio_nodo_iniziale2(rete)


    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)

    transizioni=[]

    #variabile globale
    global indice
    indice=0

    controllo_transizioni2(nodi, nodo_attuale, transizioni, osservazione)

    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)
    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)
    #ridenominazione_spazio_appena_creato(spazio)
    return spazio

def istanzio_nodo_iniziale2(rete):
    '''Partendo dalla rete creo l'istanza del nodo iniziale dello spazio comportamentale'''
    stati_correnti = rete.get_stati_correnti()
    links = dict()
    for l in rete.links:
        links[l.nome] = [l, l.evento.nome]
    nodo_iniziale = Nodo(stati_correnti, False, links, True, [], 0)
    return nodo_iniziale

def controllo_transizioni2(nodi, nodo_attuale, transizioni_spazio, osservazione):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    # print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    # print("\t"+nodo_attuale.to_string()+"\n")


    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    #scorro gli stati
    for s in stati_correnti:
        # print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
        # print("il nodo ha transizioni (nodo attuale.transizioni): "+str(len(nodo_attuale.transizioni)))
        # print("FOR LOOP. stato: "+s.nome+"\n")


        #scorro transizioni dello stato
        for t in s.transizioni:
            # print("Scorro transizioni, in nodo numero (id): " +str(nodi.index(nodo_attuale)))
            # print("nodo: "+nodo_attuale.to_string())
            # print("transizione: "+t.nome+"\n")

            #controllo se la transizione può scattare
            scatta = scatto_transizione2(t, nodo_attuale, osservazione)

            if(scatta):
                #creo il nuovo nodo generato dallo scatto della transizione
               # print("inizio a creare il nuovo nodo")
                if t.osservazione!=" ":
                    nodo_attuale.passata_osservazione=True
                    listOfGlobals = globals()
                    listOfGlobals['indice'] = listOfGlobals['indice']+1
                nuovo_nodo = deepcopy(nodo_attuale)
                nuovo_nodo.iniziale = False
                nuovo_nodo.passata_osservazione=False
                nuovo_nodo = aggiorna_nodo2(nuovo_nodo, t, nodo_attuale.lunghezza_osservazione)
                #nuovo
                nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                nuovo_nodo.output = nuovo_nodo.get_output()

                # print("Nuovo nodo creato")
                # print("\t" + nuovo_nodo.to_string() + "\n")
                #controllo che il nodo sia nuovo
                contiene = contiene_nodo_con_osservazione(nuovo_nodo, nodi)
                if (isinstance(contiene, Nodo)):
                    #print("Il nuovo nodo è già presente nella lista")
                    if contiene.iniziale and contiene.lunghezza_osservazione==len(osservazione):
                        contiene.finale = True
                    #print("aggionro l_osservazione del vecchio nodo")
                    contiene.lunghezza_osservazione=nuovo_nodo.lunghezza_osservazione
                    tra = crea_nuova_transizione(nodo_attuale, contiene, t)
                    transizioni_spazio.append(tra)
                    #nodo_attuale.transizioni.append(tra)
                    # print("Creata la nuova transizione: ")
                    # print("\t"+tra.to_string())
                    # print("numero totale di transizioni: "+str(len(transizioni_spazio)))
                else:
                   # print("Inserisco il nuovo nodo")
                    nodi.append(nuovo_nodo)
                    #print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                    tra = crea_nuova_transizione(nodo_attuale, nuovo_nodo, t)
                    transizioni_spazio.append(tra)
                    #nodo_attuale.transizioni.append(tra)
                    # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    # print("Creata la nuova transizione: ")
                    # print("\t" + tra.to_string())
                    # print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    controllo_transizioni2(nodi, nuovo_nodo, transizioni_spazio, osservazione)

            else:
                print("La transizione non scatta, esco dal ciclo")

    #print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True

def scatto_transizione2(tranizione, nodo, osservazioni):
    '''data una transizione e il nodo attuale viene stabilito se la transizione può scattare
    vengono fatte analisi solo sugli eventi presenti nei link
    non sullo stato di partenza della transizione'''
    scatta=True
    #print("Controllo transizione: "+tranizione.nome)


    if tranizione.osservazione != " ":


        if nodo.lunghezza_osservazione == len(osservazioni):
            #print("len osservazione è già uguale a: " + str(nodo.lunghezza_osservazione) + ", non posso aggiungerne altre")
            return False
        else:
            if(osservazioni[nodo.lunghezza_osservazione]!=tranizione.osservazione):
                # print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
                # print("La transizione ha il seguente valore: "+tranizione.osservazione)
                # print("NON coincidono")
                return False
            # else:
            #     print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
            #     print("La transizione ha il seguente valore: " + tranizione.osservazione)
            #     print("Coincidono")

        if nodo.passata_osservazione:
            # print("IL nodo ha già una transizione uscente con l'etichetta di osservazione cercata")
            # print("NON SCATTA")
            return False

    #scorro eventi in input della transizione
    for evento in tranizione.input:
        #print("controllo INPUT")
        #verifico che non sia un evento vuoto
        if(evento.nome != "" and evento.link != None):
            #ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            #print("Evento: "+evento.nome+" ("+evento.link.nome+") -> valore nel nodo: "+valore_nel_link)

            if (evento.nome != valore_nel_link):
                #print("Non c'è l'input corretto, la transizione non può scattare\n")
                return False

    # scorro eventi in output della transizione
    for evento in tranizione.output:
        #print("controllo Output")
        # verifico che non sia un evento vuoto
        if (evento.nome != "" and evento.link != None):
            # ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            #print("Evento: " + evento.nome + " (" + evento.link.nome + ") -> valore nel nodo: " + valore_nel_link)

            if (valore_nel_link != ""):
                #print("Il link di output non è vuoto, impossibile scattare\n")
                return False
    #print("La transizione può scattare\n")
    return scatta

def aggiorna_nodo2(nodo, transizione, l_osservazione):
    '''dato un nodo e una transizione viene fatta scattare la transizione aggiornando il nodo stesso'''
    #print("aggiorno i valori del nuovo nodo")
    #scorro eventi di input
    for evento in transizione.input:
        #print("input")
        if (evento.nome != "" and evento.link != None):
            #tolgo i valori dai link di input
            nodo.links[evento.link.nome][1]=""
            #print("ho aggiornato "+evento.link.nome+" mettendolo a "+ nodo.links[evento.link.nome][1])
    for evento in transizione.output:
        #print("output")
        if (evento.nome != "" and evento.link != None):
            #inserisco l'evento nel link di output
            nodo.links[evento.link.nome][1]=evento.nome
            #print("ho aggiornato "+evento.link.nome+" mettendolo a "+ nodo.links[evento.link.nome][1])


    #ricavo la posizione dello stato sorgente
    for index, s in enumerate(nodo.stati):
        # print("Scorro stato: "+s.to_string()+" = "+str(s))
        # print("devo confrontarlo con: "+transizione.stato_sorgente.to_string()+" = "+str(transizione.stato_sorgente))
        if s.id == transizione.stato_sorgente.id:
            #print("ho aggiornato lo stato "+nodo.stati[index].nome)
            nodo.stati[index] = transizione.stato_destinazione
            #print(" mettendolo a " +nodo.stati[index].nome)

    if transizione.osservazione!=" ":
        #print("La transizione ha un valore di osservazione: "+transizione.osservazione)
        nodo.lunghezza_osservazione= l_osservazione + 1
        #print("Aggiornato il valore del nuovo nodo di l_osservazione")

    return nodo


def ridenominazione_spazio_appena_creato(spazio):
    for i in range(len(spazio.nodi)):
        spazio.nodi[i].id = str(i)

def crea_nuova_transizione(sorgente, destinazione, transizione):
    nuova_transizione = Transizione_spazio(transizione.nome, sorgente, destinazione, transizione.osservazione, transizione.rilevanza)
    return nuova_transizione

#ALGORITMO 2 Da rete - Migliorato
def crea_spazio_comportamentale2_migliorato(rete, osservazione):

    print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE CON OSSERVAZIONE")
    rete = rete
    osservazione=osservazione

    #Salvo l'array degli automi presenti nella rete #rete.automi
    #Salvo l'array dei links presenti nella rete #rete.links
    #Salvo l'array delle transizioni presenti nella rete #rete.transizioni
    automi = rete.automi
    links = rete.links
    transizioni = rete.get_transizioni()

    #creo un array vuoto di nodi dello spazio comportamentale
    nodi = []

    #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
    nodo_attuale = istanzio_nodo_iniziale2(rete)


    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)

    transizioni=[]

    #variabile globale
    global indice
    indice=0

    controllo_transizioni2_migliorato(nodi, nodo_attuale, transizioni, osservazione)

    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)
    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)
    ridenominazione_spazio_appena_creato(spazio)
    return spazio

def controllo_transizioni2_migliorato(nodi, nodo_attuale, transizioni_spazio, osservazione):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    print("\t"+nodo_attuale.to_string()+"\n")


    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    #scorro gli stati
    for s in stati_correnti:
        print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
        print("il nodo ha transizioni (nodo attuale.transizioni): "+str(len(nodo_attuale.transizioni)))
        print("FOR LOOP. stato: "+s.nome+"\n")


        #scorro transizioni dello stato
        for t in s.transizioni:
            print("Scorro transizioni, in nodo numero (id): " +str(nodi.index(nodo_attuale)))
            print("nodo: "+nodo_attuale.to_string())
            print("transizione: "+t.nome+"\n")

            #controllo se la transizione può scattare
            scatta = scatto_transizione2_migliorato(t, nodo_attuale, osservazione, nodo_attuale.lunghezza_osservazione)

            if(isinstance(scatta, Nodo)):
                #creo il nuovo nodo generato dallo scatto della transizione
                print("inizio a creare il nuovo nodo")
                if t.osservazione!=" ":
                    nodo_attuale.passata_osservazione=True
                    listOfGlobals = globals()
                    listOfGlobals['indice'] = listOfGlobals['indice']+1
                nuovo_nodo = scatta
                nuovo_nodo.iniziale = False
                nuovo_nodo.passata_osservazione=False
                nuovo_nodo = aggiorna_nodo2(nuovo_nodo, t, nodo_attuale.lunghezza_osservazione)
                #nuovo
                nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                nuovo_nodo.output = nuovo_nodo.get_output()

                print("Nuovo nodo creato")
                print("\t" + nuovo_nodo.to_string() + "\n")
                #controllo che il nodo sia nuovo
                contiene = contiene_nodo_con_osservazione(nuovo_nodo, nodi)
                if (isinstance(contiene, Nodo)):
                    print("Il nuovo nodo è già presente nella lista")
                    if contiene.iniziale and contiene.lunghezza_osservazione==len(osservazione):
                        contiene.finale = True
                    print("aggionro l_osservazione del vecchio nodo")
                    contiene.lunghezza_osservazione=nuovo_nodo.lunghezza_osservazione
                    tra = crea_nuova_transizione(nodo_attuale, contiene, t)
                    transizioni_spazio.append(tra)
                    #nodo_attuale.transizioni.append(tra)
                    print("Creata la nuova transizione: ")
                    print("\t"+tra.to_string())
                    print("numero totale di transizioni: "+str(len(transizioni_spazio)))
                else:
                    print("Inserisco il nuovo nodo")
                    nodi.append(nuovo_nodo)
                    print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                    tra = crea_nuova_transizione(nodo_attuale, nuovo_nodo, t)
                    transizioni_spazio.append(tra)
                    #nodo_attuale.transizioni.append(tra)
                    print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    print("Creata la nuova transizione: ")
                    print("\t" + tra.to_string())
                    print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    controllo_transizioni2(nodi, nuovo_nodo, transizioni_spazio, osservazione)

            else:
                print("La transizione non scatta, esco dal ciclo")

    print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True

def scatto_transizione2_migliorato(transizione, nodo, osservazioni, l_osservazione):
    '''data una transizione e il nodo attuale viene stabilito se la transizione può scattare
    vengono fatte analisi solo sugli eventi presenti nei link
    non sullo stato di partenza della transizione'''
    scatta=True
    print("Controllo transizione: "+transizione.nome)

    nuovo_nodo = deepcopy(nodo)


    if transizione.osservazione != " ":


        if nodo.lunghezza_osservazione == len(osservazioni):
            print("len osservazione è già uguale a: " + str(nodo.lunghezza_osservazione) + ", non posso aggiungerne altre")
            return False
        else:
            if(osservazioni[nodo.lunghezza_osservazione]!=transizione.osservazione):
                print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
                print("La transizione ha il seguente valore: "+transizione.osservazione)
                print("NON coincidono")
                return False
            else:
                print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
                print("La transizione ha il seguente valore: " + transizione.osservazione)
                print("Coincidono")

        if nodo.passata_osservazione:
            print("IL nodo ha già una transizione uscente con l'etichetta di osservazione cercata")
            print("NON SCATTA")
            return False

    #scorro eventi in input della transizione
    for evento in transizione.input:
        print("controllo INPUT")
        #verifico che non sia un evento vuoto
        if(evento.nome != "" and evento.link != None):
            #ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            print("Evento: "+evento.nome+" ("+evento.link.nome+") -> valore nel nodo: "+valore_nel_link)

            if (evento.nome != valore_nel_link):
                print("Non c'è l'input corretto, la transizione non può scattare\n")
                return False
            else:
                nuovo_nodo.links[evento.link.nome][1] = ""
                print("ho aggiornato " + evento.link.nome + " mettendolo a " + nodo.links[evento.link.nome][1])


    # scorro eventi in output della transizione
    for evento in transizione.output:
        print("controllo Output")
        # verifico che non sia un evento vuoto
        if (evento.nome != "" and evento.link != None):
            # ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            print("Evento: " + evento.nome + " (" + evento.link.nome + ") -> valore nel nodo: " + valore_nel_link)

            if (valore_nel_link != ""):
                print("Il link di output non è vuoto, impossibile scattare\n")
                return False
            else:
                nuovo_nodo.links[evento.link.nome][1] = evento.nome
                print("ho aggiornato " + evento.link.nome + " mettendolo a " + nodo.links[evento.link.nome][1])

    for index, s in enumerate(nuovo_nodo.stati):
        print("Scorro stato: "+s.to_string()+" = "+str(s))
        print("devo confrontarlo con: "+transizione.stato_sorgente.to_string()+" = "+str(transizione.stato_sorgente))
        if s.id == transizione.stato_sorgente.id:
            print("ho aggiornato lo stato "+nuovo_nodo.stati[index].nome)
            nuovo_nodo.stati[index] = transizione.stato_destinazione
            print(" mettendolo a " +nuovo_nodo.stati[index].nome)

    if transizione.osservazione!=" ":
        print("La transizione ha un valore di osservazione: "+transizione.osservazione)
        nuovo_nodo.lunghezza_osservazione= l_osservazione + 1
        print("Aggiornato il valore del nuovo nodo di l_osservazione")

    return nuovo_nodo

#ALGORITMO 2 Da rete - Migliorato (nuova ridenominazione)
def crea_spazio_comportamentale2_migliorato_nuova_ridenominazione(rete, osservazione):

    print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE CON OSSERVAZIONE")
    rete = rete
    osservazione=osservazione

    #Salvo l'array degli automi presenti nella rete #rete.automi
    #Salvo l'array dei links presenti nella rete #rete.links
    #Salvo l'array delle transizioni presenti nella rete #rete.transizioni
    automi = rete.automi
    links = rete.links
    transizioni = rete.get_transizioni()

    #creo un array vuoto di nodi dello spazio comportamentale
    nodi = []

    #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
    nodo_attuale = istanzio_nodo_iniziale2(rete)


    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)

    transizioni=[]

    #variabile globale
    global indice
    global ridenominazione
    ridenominazione = 0
    indice=0

    controllo_transizioni2_migliorato_nuova_ridenominazione(nodi, nodo_attuale, transizioni, osservazione)

    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)
    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)
    #ridenominazione_spazio_appena_creato(spazio)
    return spazio

def controllo_transizioni2_migliorato_nuova_ridenominazione(nodi, nodo_attuale, transizioni_spazio, osservazione):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    print("\t"+nodo_attuale.to_string()+"\n")


    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    #scorro gli stati
    for s in stati_correnti:
        print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
        print("il nodo ha transizioni (nodo attuale.transizioni): "+str(len(nodo_attuale.transizioni)))
        print("FOR LOOP. stato: "+s.nome+"\n")


        #scorro transizioni dello stato
        for t in s.transizioni:
            print("Scorro transizioni, in nodo numero (id): " +str(nodi.index(nodo_attuale)))
            print("nodo: "+nodo_attuale.to_string())
            print("transizione: "+t.nome+"\n")

            #controllo se la transizione può scattare
            scatta = scatto_transizione2_migliorato(t, nodo_attuale, osservazione, nodo_attuale.lunghezza_osservazione)

            if(isinstance(scatta, Nodo)):
                #creo il nuovo nodo generato dallo scatto della transizione
                print("inizio a creare il nuovo nodo")
                if t.osservazione!=" ":
                    nodo_attuale.passata_osservazione=True
                    listOfGlobals = globals()
                    listOfGlobals['indice'] = listOfGlobals['indice']+1
                nuovo_nodo = scatta
                nuovo_nodo.iniziale = False
                nuovo_nodo.passata_osservazione=False
                nuovo_nodo = aggiorna_nodo2(nuovo_nodo, t, nodo_attuale.lunghezza_osservazione)
                #nuovo
                nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                nuovo_nodo.output = nuovo_nodo.get_output()

                print("Nuovo nodo creato")
                print("\t" + nuovo_nodo.to_string() + "\n")
                #controllo che il nodo sia nuovo
                contiene = contiene_nodo_con_osservazione(nuovo_nodo, nodi)
                if (isinstance(contiene, Nodo)):
                    print("Il nuovo nodo è già presente nella lista")
                    if contiene.iniziale and contiene.lunghezza_osservazione==len(osservazione):
                        contiene.finale = True
                    print("aggionro l_osservazione del vecchio nodo")
                    contiene.lunghezza_osservazione=nuovo_nodo.lunghezza_osservazione
                    tra = crea_nuova_transizione(nodo_attuale, contiene, t)
                    transizioni_spazio.append(tra)
                    #nodo_attuale.transizioni.append(tra)
                    print("Creata la nuova transizione: ")
                    print("\t"+tra.to_string())
                    print("numero totale di transizioni: "+str(len(transizioni_spazio)))
                else:
                    listOfGlobals = globals()
                    rid = listOfGlobals['ridenominazione']
                    print("Inserisco il nuovo nodo")
                    nuovo_nodo.id=str(rid)
                    listOfGlobals['ridenominazione'] = rid +1
                    nodi.append(nuovo_nodo)
                    print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                    tra = crea_nuova_transizione(nodo_attuale, nuovo_nodo, t)
                    transizioni_spazio.append(tra)
                    #nodo_attuale.transizioni.append(tra)
                    print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    print("Creata la nuova transizione: ")
                    print("\t" + tra.to_string())
                    print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    controllo_transizioni2(nodi, nuovo_nodo, transizioni_spazio, osservazione)

            else:
                print("La transizione non scatta, esco dal ciclo")

    print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True

def scatto_transizione2_migliorato(transizione, nodo, osservazioni, l_osservazione):
    '''data una transizione e il nodo attuale viene stabilito se la transizione può scattare
    vengono fatte analisi solo sugli eventi presenti nei link
    non sullo stato di partenza della transizione'''
    scatta=True
    print("Controllo transizione: "+transizione.nome)

    nuovo_nodo = deepcopy(nodo)


    if transizione.osservazione != " ":


        if nodo.lunghezza_osservazione == len(osservazioni):
            print("len osservazione è già uguale a: " + str(nodo.lunghezza_osservazione) + ", non posso aggiungerne altre")
            return False
        else:
            if(osservazioni[nodo.lunghezza_osservazione]!=transizione.osservazione):
                print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
                print("La transizione ha il seguente valore: "+transizione.osservazione)
                print("NON coincidono")
                return False
            else:
                print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
                print("La transizione ha il seguente valore: " + transizione.osservazione)
                print("Coincidono")

        if nodo.passata_osservazione:
            print("IL nodo ha già una transizione uscente con l'etichetta di osservazione cercata")
            print("NON SCATTA")
            return False

    #scorro eventi in input della transizione
    for evento in transizione.input:
        print("controllo INPUT")
        #verifico che non sia un evento vuoto
        if(evento.nome != "" and evento.link != None):
            #ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            print("Evento: "+evento.nome+" ("+evento.link.nome+") -> valore nel nodo: "+valore_nel_link)

            if (evento.nome != valore_nel_link):
                print("Non c'è l'input corretto, la transizione non può scattare\n")
                return False
            else:
                nuovo_nodo.links[evento.link.nome][1] = ""
                print("ho aggiornato " + evento.link.nome + " mettendolo a " + nodo.links[evento.link.nome][1])


    # scorro eventi in output della transizione
    for evento in transizione.output:
        print("controllo Output")
        # verifico che non sia un evento vuoto
        if (evento.nome != "" and evento.link != None):
            # ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            print("Evento: " + evento.nome + " (" + evento.link.nome + ") -> valore nel nodo: " + valore_nel_link)

            if (valore_nel_link != ""):
                print("Il link di output non è vuoto, impossibile scattare\n")
                return False
            else:
                nuovo_nodo.links[evento.link.nome][1] = evento.nome
                print("ho aggiornato " + evento.link.nome + " mettendolo a " + nodo.links[evento.link.nome][1])

    for index, s in enumerate(nuovo_nodo.stati):
        print("Scorro stato: "+s.to_string()+" = "+str(s))
        print("devo confrontarlo con: "+transizione.stato_sorgente.to_string()+" = "+str(transizione.stato_sorgente))
        if s.id == transizione.stato_sorgente.id:
            print("ho aggiornato lo stato "+nuovo_nodo.stati[index].nome)
            nuovo_nodo.stati[index] = transizione.stato_destinazione
            print(" mettendolo a " +nuovo_nodo.stati[index].nome)

    if transizione.osservazione!=" ":
        print("La transizione ha un valore di osservazione: "+transizione.osservazione)
        nuovo_nodo.lunghezza_osservazione= l_osservazione + 1
        print("Aggiornato il valore del nuovo nodo di l_osservazione")

    return nuovo_nodo




#--------------------------------------------------
#POTATURA
def potatura_e_ridenominazione(spazio):
    '''Algoritmo per potare uno spazio comportamentale e contemporaneamente ridenominarlo'''

    nodi_finali = spazio.nodi_finali
    potatura(nodi_finali)
    #print("SPAZIO DOPO POTATURA")


    ridenominazione_dopo_potatura(spazio)
    # for n in spazio.nodi:
    #     #print("NODO: "+str(n.id))
    #     # for t in n.transizioni_sorgente:
    #     #     print(str(i) + ") " + "ID: " + t.nodo_sorgente.id + "(" + str(
    #     #         t.nodo_sorgente.potato) + ") - " + t.nome + " potata: " + str(t.potato) + ", " + str(
    #     #         t.nodo_destinazione.id) + "(" + str(t.nodo_destinazione.potato) + ")")
    #     #     i = i + 1
    spazio.spazio_potato=True
    #print("Durante POTATURA")

    return spazio

def potatura(nodi):
    for n in nodi:
        salva_nodo_da_potatura(n)
        for t in n.transizioni_sorgente:
            t.potato=False
            if t.nodo_sorgente.potato == True:
                potatura([t.nodo_sorgente])
        #print("NODO ID: " + str(n.id) + "potato: " + str(n.potato))
    i = 0

def salva_nodo_da_potatura(nodo):
    nodo.potato=False
    for t in nodo.transizioni_sorgente:
        t.potato=False

def ridenominazione_dopo_potatura(spazio):
    for i in range(len([n for n in spazio.nodi if n.potato == False])):
        spazio.nodi[i].old_id = spazio.nodi[i].id
        spazio.nodi[i].id = str(i)

#POTATURA MIGLIORATO
def potatura_migliorato(nodi):
    for n in nodi:
        n.potato = False
        for t in n.transizioni_sorgente:
            t.potato = False
            if t.nodo_sorgente.potato == True:
                potatura([t.nodo_sorgente])




def crea_spazio_da_spazio_potato(spazio):
    '''Dato uno spazio potato ne crea un secondo contenente solamente i nodi non potati
    e aggiornando di conseguenza tutte le transizioni'''
    nuovo_spazio = deepcopy(spazio)

    nuovi_nodi = [n for n in nuovo_spazio.nodi if n.potato == False]
    nuovo_spazio.nodi=nuovi_nodi
    for n in nuovo_spazio.nodi:
        ripristina_nodo(n)

    nuove_transizioni = [t for t in nuovo_spazio.transizioni if t.potato == False]
    nuovo_spazio.transizioni=nuove_transizioni
    for t in nuovo_spazio.transizioni:
        ripristina_transizione(t)

    for t in nuovo_spazio.transizioni:
        t.nodo_sorgente.transizioni.append(t)
        t.nodo_destinazione.transizioni_sorgente.append(t)


    # #print("SALVATAGGIO")
    # for n in nuovo_spazio.nodi:
    #     #print("NODO: " + n.to_string())
    #     for t in n.transizioni:
    #         print("\t" + t.to_string() + "transizione potata= " + str(t.potato))

    return  nuovo_spazio

def crea_spazio_da_spazio(spazio):
    '''Dato uno spazio ne crea una copia, impostando però tutti i nodi ai valri originari'''
    nuovo_spazio = deepcopy(spazio)

    for n in nuovo_spazio.nodi:
        ripristina_nodo(n)

    for t in nuovo_spazio.transizioni:
        ripristina_transizione(t)

    for t in nuovo_spazio.transizioni:
        t.nodo_sorgente.transizioni.append(t)
        t.nodo_destinazione.transizioni_sorgente.append(t)

    return nuovo_spazio


#---------------------------------------------------------
#ALGORITMO 3

#procedure per sistemare nodi iniziali e finali
def diagnosi_sistemo_spazio(spazio):
    '''procedura per sistemare nodi iniziali e finali prima di eseguire la diagnosi'''
    nodi = spazio.nodi
    transizioni = spazio.transizioni

    nodo_iniziale = spazio.nodi_iniziali[0]  # prendo nodo iniziale
    nodi_finali = spazio.nodi_finali
    # print("TROVO NODO INIZIALE:")
    # print(nodo_iniziale.to_string())

    # se il nodo iniziale ha delle transizioni entranti va creato un nuovo nodo iniziale
    sistemo_nodo_iniziale(nodo_iniziale, nodi, transizioni)

    # se ci sono più nodi finiali ne va creato solo uno
    sistemo_nodi_finali(nodi_finali, nodi, transizioni)

def sistemo_nodo_iniziale(nodo_iniziale, nodi, transizioni):
    #print("\n\nSISTEMO NODO INIZIALE")
    #print("Lunghezza transizioni che entrano nel nodo iniziale: "+str(len(nodo_iniziale.transizioni_sorgente)))

    if len(nodo_iniziale.transizioni_sorgente) > 0:
        nuovo_nodo = Nodo(nodo_iniziale.stati, False, nodo_iniziale.links, True, [], 0)
        #print("Creo nuovo nodo: "+nuovo_nodo.to_string())
        nodo_iniziale.iniziale=False
        tra = Transizione_spazio("n0", nuovo_nodo, nodo_iniziale, " ", " ") #nome, nodo_sorgente=None, nodo_destinazione=None, osservazione=None, rilevanza=None
        #print("Creo nuova transizione: "+tra.to_string())

        transizioni.insert(0, tra)
        nodi.insert(0, nuovo_nodo)

def sistemo_nodi_finali(nodi_finali, nodi, transizioni):
    #print("\n\nSISTEMO NODI FINALI")
    numero_nodi_finali = len(nodi_finali)

    if (numero_nodi_finali > 1):
        #print("Il numero di nodi finali è > 1")
        nuovo_nodo = Nodo(nodi_finali[0].stati, False, nodi_finali[0].links, False, [], 0) #stati, check, links, iniziale, transizioni=[], *args):
        nuovo_nodo.finale=True
        nodi.append(nuovo_nodo)

        for idx, n in enumerate(nodi_finali):
            n.finale=False
            tra = Transizione_spazio("nq"+str(idx), n, nuovo_nodo, " ", " ")  # nome, nodo_sorgente=None, nodo_destinazione=None, osservazione=None, rilevanza=None
            transizioni.append(tra)
            #print("Creata nuova transizione: "+tra.to_string())

    if (numero_nodi_finali==1)and(len(nodi_finali[0].transizioni)>0):
        #print("Il numero di nodi finali è = 1")
        nuovo_nodo = Nodo(nodi_finali[0].stati, False, nodi_finali[0].links, False, [],
                          0)  # stati, check, links, iniziale, transizioni=[], *args):
        nuovo_nodo.finale = True
        nodi.append(nuovo_nodo)

        for idx, n in enumerate(nodi_finali):
            n.finale = False
            tra = Transizione_spazio("nq"+str(idx), n, nuovo_nodo, " ", " ")
            transizioni.append(tra)
            #print("Creata nuova transizione: " + tra.to_string())



#ALGORITMO 3, manuale
def diagnosi_algoritmo_su_spazio_manuale(spazio):
    '''Procedura per eseguire una diagnosi manualmente'''

    nodi = spazio.nodi
    transizioni=spazio.transizioni

    nodo_iniziale = spazio.nodi_iniziali[0] #prendo nodo iniziale
    nodi_finali = spazio.nodi_finali

    finito = semplifico_transizioni_diagnosi_manuale(nodi, transizioni)


    #fine output
    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)


    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)

    return spazio, finito

def semplifico_transizioni_diagnosi_manuale(nodi, transizioni):

    sistema_transizioni_da_nodi_e_transizioni(nodi, transizioni)
    if (len(transizioni)>1):
        sistema_transizioni_da_nodi_e_transizioni(nodi, transizioni)
        # print("---------------------iterazione: "+str(i))
        #
        # print("-----------CONTROLLO SEQUENZA")
        sequenza = controllo_sequenza(nodi, transizioni)
        if sequenza == False:
            #print("--------CONTROLLO TRATTI PARALLELI")
            tratti = controlla_tratti_paralleli(transizioni)
            if tratti==False:
                #print("------------CONTROLLO NODI")
                controlla_nodi(nodi, transizioni)
                sistema_transizioni_da_nodi_e_transizioni(nodi, transizioni)
        nodi_finali = []
        nodi_iniziali = []
        for n in nodi:
            if n.finale:
                nodi_finali.append(n)
            if n.iniziale:
                nodi_iniziali.append(n)
        return False
    else:
        return True


#ALGORITMO 3
def diagnosi_algoritmo_su_spazio(spazio):
    '''Metodo per eseguire una diagnosi sullo spazio dato in input'''

    #print("DENTRO LA DIAGNOSI")
    nodi = spazio.nodi
    transizioni=spazio.transizioni

    nodo_iniziale = spazio.nodi_iniziali[0] #prendo nodo iniziale
    nodi_finali = spazio.nodi_finali
    #print("TROVO NODO INIZIALE:")
    #print(nodo_iniziale.to_string())

    #se il nodo iniziale ha delle transizioni entranti va creato un nuovo nodo iniziale
    #sistemo_nodo_iniziale(nodo_iniziale, nodi, transizioni)

    #se ci sono più nodi finiali ne va creato solo uno
    #sistemo_nodi_finali(nodi_finali, nodi, transizioni)


    semplifico_transizioni_diagnosi(nodi, transizioni)


    #fine output
    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)


    # print("NODI TOTALI:")
    # i=0
    # for n in nodi:
    #     print(str(i)+") "+n.to_string())
    #     i=i+1
    #
    # print("TRANSIZIONI TOTALI:")
    # i=0
    # for t in transizioni:
    #     print(str(i)+") "+t.to_string())
    #     i=i+1
    #
    # print("NODI INZIALI:")
    # i = 0
    # for n in nodi_iniziali:
    #     print(str(i) + ") " + n.to_string())
    #     i = i + 1
    #
    # print("NODI FINALI:")
    # i = 0
    # for n in nodi_finali:
    #     print(str(i) + ") " + n.to_string())
    #     i = i + 1


    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)
    #ridenominazione_spazio_appena_creato(spazio)
    # print("SPAZIO: ")
    # print(spazio.to_string())
    return spazio

def diagnosi_algoritmo_su_spazio_unito(spazio):
    '''Metodo per eseguire una diagnosi sullo spazio dato in input'''

    diagnosi_sistemo_spazio(spazio)
    #print("DENTRO LA DIAGNOSI")
    nodi = spazio.nodi
    transizioni=spazio.transizioni

    nodo_iniziale = spazio.nodi_iniziali[0] #prendo nodo iniziale
    nodi_finali = spazio.nodi_finali
    #print("TROVO NODO INIZIALE:")
    #print(nodo_iniziale.to_string())

    #se il nodo iniziale ha delle transizioni entranti va creato un nuovo nodo iniziale
    #sistemo_nodo_iniziale(nodo_iniziale, nodi, transizioni)

    #se ci sono più nodi finiali ne va creato solo uno
    #sistemo_nodi_finali(nodi_finali, nodi, transizioni)


    semplifico_transizioni_diagnosi(nodi, transizioni)


    #fine output
    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)


    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)
    #ridenominazione_spazio_appena_creato(spazio)
    # print("SPAZIO: ")
    # print(spazio.to_string())
    return spazio


def semplifico_transizioni_diagnosi(nodi, transizioni):
    '''Metodo per svolgere i passaggi della diagnosi
        Semplificazione di una seguenza
        Semplificazione di transizioni parallele
        Terzo tipo di semplificazione (auto transizione)'''
    #print("\n\n\nSEMPLIFICO TRANSIZIONI")

    sistema_transizioni_da_nodi_e_transizioni(nodi, transizioni)
    #print("Ho corretto sorgente, dest e auto di tutti i nodi")
    i=1
    while (len(transizioni)>1):
        sistema_transizioni_da_nodi_e_transizioni(nodi, transizioni)
        # print("---------------------iterazione: "+str(i))
        #
        # print("-----------CONTROLLO SEQUENZA")
        sequenza = controllo_sequenza(nodi, transizioni)
        if sequenza == False:
            #print("--------CONTROLLO TRATTI PARALLELI")
            tratti = controlla_tratti_paralleli(transizioni)
            if tratti==False:
                #print("------------CONTROLLO NODI")
                controlla_nodi(nodi, transizioni)
                sistema_transizioni_da_nodi_e_transizioni(nodi, transizioni)
        nodi_finali = []
        nodi_iniziali = []
        for n in nodi:
            if n.finale:
                nodi_finali.append(n)
            if n.iniziale:
                nodi_iniziali.append(n)
        i = i + 1

def controlla_nodi(nodi, transizioni):
    '''Terzo tipo di semplificazione: auto transizioni'''
    for n in nodi:
        # print("FOR NODO: ")
        # print(n.to_string())
        trovato=False
        if n.finale==False and n.iniziale==False:
            #transizioni entranti (non auto transizioni)
            for i in [x for x in n.transizioni_sorgente if x.nodo_sorgente!=n]:
                for o in [y for y in n.transizioni if y.nodo_destinazione!=n]:
                    # print("INTERNO FOR, transizioni")
                    # print("Transizione entrante: "+i.to_string())
                    # print("Transizione uscente: " + o.to_string())

                    if len(n.transizioni_auto)==0: #non ci sono autotransizioni
                        trovato=True
                        lista_etichette=[]
                        lista_etichette.append(i.rilevanza)
                        lista_etichette.append(o.rilevanza)

                        #print("Creazione etichetta")
                        etichetta = ""
                        for e in lista_etichette:
                            etichetta = crea_etichetta_and(etichetta, e)
                        if etichetta == "":
                            etichetta = " "
                        #print("Ho creato etichetta nuova transizione: " + etichetta)

                        nodo_sorgente = i.nodo_sorgente
                        nodo_destinazione = o.nodo_destinazione
                        transizione = Transizione_spazio(nome="nome", nodo_sorgente=nodo_sorgente,
                                                         nodo_destinazione=nodo_destinazione, osservazione=" ",
                                                         rilevanza=etichetta)
                        transizioni.append(transizione)
                        # print("Creo nuova transizione: ")
                        # print(transizione.to_string())
                    else: #ci sono autotransizioni
                        trovato=True
                        for auto in n.transizioni_auto:
                            lista_etichette = []
                            lista_etichette.append(i.rilevanza)
                            lista_etichette.append("("+auto.rilevanza+")*")
                            lista_etichette.append(o.rilevanza)

                            #print("Creazione etichetta")
                            etichetta = ""
                            for e in lista_etichette:
                                etichetta = crea_etichetta_and(etichetta, e)
                            if etichetta == "":
                                etichetta = " "
                            #print("Ho creato etichetta nuova transizione: " + etichetta)

                            nodo_sorgente = i.nodo_sorgente
                            nodo_destinazione = o.nodo_destinazione
                            transizione = Transizione_spazio(nome="nome", nodo_sorgente=nodo_sorgente,
                                                             nodo_destinazione=nodo_destinazione, osservazione=" ",
                                                             rilevanza=etichetta)
                            transizioni.append(transizione)
                            # print("Creo nuova transizione: ")
                            # print(transizione.to_string())
        if trovato:
            #print("Finito FOR sul nodo con successo. Inizio a eliminare parti inutili")
            if n in nodi:
                nodi.remove(n)
                #print("rimuovo nodo: "+n.to_string())
            for t in n.transizioni:
                if t in transizioni:
                    transizioni.remove(t)
                    #print("rimuovo transizione: " + t.to_string())
            for t in n.transizioni_sorgente:
                if t in transizioni:
                    transizioni.remove(t)
                    #print("rimuovo transizione: " + t.to_string())
            break

def controlla_tratti_paralleli(transizioni):
    '''Terzo tipo di semplificazione: tratti paralleli'''
    #print("CONTROLLO TRATTI PARALLELI PER OR")

    for t in transizioni:
        paralleli = False
        lista_transizioni = []

        # print("FOR: Analizzo la transizione: ")
        # print(t.to_string())
        # print("\n")
        # print("INFO sulla transizione")
        # print("numero transizioni nodo sorgente: " + str(len(t.nodo_sorgente.transizioni)))
        # print("numero transizioni entranti nodo dest: " + str(len(t.nodo_destinazione.transizioni_sorgente)))

        if ((len(t.nodo_sorgente.transizioni)) > 1 ) and ((len(t.nodo_destinazione.transizioni_sorgente)) > 1 ):
            # print("Il nodo destinazione rispecchia i requisiti")
            # print("Nodo destinazione: " + t.nodo_destinazione.to_string())
            for tra in t.nodo_sorgente.transizioni:
                if t!=tra:
                    if t.nodo_destinazione==tra.nodo_destinazione:
                        # print("trovata transizione parallela:")
                        # print(tra.to_string())
                        lista_transizioni.append(t)
                        lista_transizioni.append(tra)
                        paralleli = True
                        break
        if paralleli:
            break


    if paralleli:
        #print("Creazione etichetta")
        etichetta = ""
        if lista_transizioni[0].rilevanza==" ":
            if lista_transizioni[1].rilevanza==" ":
                etichetta=" "
            else:
                etichetta=lista_transizioni[1].rilevanza+"|ε"
        else:
            if lista_transizioni[1].rilevanza==" ":
                etichetta=lista_transizioni[0].rilevanza+"|ε"
            else:
                etichetta=lista_transizioni[0].rilevanza+"|"+lista_transizioni[1].rilevanza

        #print("Ho creato etichetta nuova transizione: " + etichetta)

        # creo transizione
        nodo_sorgente = lista_transizioni[0].nodo_sorgente
        nodo_destinazione = lista_transizioni[0].nodo_destinazione
        transizione = Transizione_spazio(nome="nome", nodo_sorgente=nodo_sorgente, nodo_destinazione=nodo_destinazione,
                                         osservazione=" ", rilevanza=etichetta)
        transizioni.append(transizione)
        # print("Creo nuova transizione: ")
        # print(transizione.to_string())

        transizioni.remove(lista_transizioni[0])
        transizioni.remove(lista_transizioni[1])
        return True
    else:
        return False

def controllo_sequenza(nodi, transizioni):
    '''Terzo tipo di semplificazione: sequenza'''
    #print("CONTROLLO PER SEQUENZA AND")


    for t in transizioni:
        sequenza = False
        lista_sequenza = []

        # print("FOR: Analizzo la transizione: ")
        # print(t.to_string())
        # print("\n")
        # print("INFO sulla transizione")
        # print("lunghezza nodo dest transizioni entranti: "+str(len(t.nodo_destinazione.transizioni_sorgente)))
        # print("nodo dest auto transizioni: "+str(len(t.nodo_sorgente.transizioni_auto)))

        #il nodo destinazione ha 1 transizione uscente e una entrante
        if ((len(t.nodo_destinazione.transizioni) == 1) and (len(t.nodo_destinazione.transizioni_sorgente) == 1) and (len(t.nodo_destinazione.transizioni_auto)==0)):
            #print("Il nodo destinazione rispecchia i requisiti, 1 transizione entrante, 1 uscente, no auto transizioni")
            #print("Nodo destinazione: "+t.nodo_destinazione.to_string())
            lista_sequenza.append(t)
            lista_sequenza.append(t.nodo_destinazione.transizioni[0])
            sequenza=True
            esplora_sequenza(t.nodo_destinazione.transizioni[0], lista_sequenza)
            #print("ho finito di esplorare la seguenza, è lunga: "+str(len(lista_sequenza)))
            break

    if sequenza:
        #print("Creazione etichetta")
        etichetta=""
        for tra in lista_sequenza:
            etichetta = crea_etichetta_and(etichetta, tra.rilevanza)

        if etichetta=="":
            etichetta=" "


        #print("Ho creato etichetta nuova transizione: "+etichetta)

        #creo transizione
        nodo_sorgente=lista_sequenza[0].nodo_sorgente
        nodo_destinazione=lista_sequenza[len(lista_sequenza)-1].nodo_destinazione
        transizione = Transizione_spazio(nome="nome",nodo_sorgente=nodo_sorgente,nodo_destinazione=nodo_destinazione,osservazione=" ",rilevanza=etichetta)
        transizioni.append(transizione)
        #print("Creo nuova transizione: ")
        #print(transizione.to_string())

        #elimino nodi e transizioni saltate
        for index, tra in enumerate(lista_sequenza):
            if index==0:
                if tra.nodo_destinazione in nodi:
                    nodi.remove(tra.nodo_destinazione)
                transizioni.remove(tra)
            elif index==len(lista_sequenza)-1:
                if tra.nodo_sorgente in nodi:
                    nodi.remove(tra.nodo_sorgente)
                transizioni.remove(tra)
            else:
                if tra.nodo_sorgente in nodi:
                    nodi.remove(tra.nodo_sorgente)
                if tra.nodo_destinazione in nodi:
                    nodi.remove(tra.nodo_destinazione)
                if tra in transizioni:
                    transizioni.remove(tra)
        return True
    else:
        return False

def esplora_sequenza(transizione, lista_sequenza):
    '''funzione ricorsiva che parte da una transizione e cerca ulteriori transizioni che possano creare una sequenza di AND'''
    #prendo transizione uscente
    #print("Esploro la seguenza, sono nella transizione:")
    #print(transizione.to_string())
    if ((len(transizione.nodo_destinazione.transizioni )== 1) and (len(transizione.nodo_destinazione.transizioni_sorgente )== 1) and (len(
            transizione.nodo_destinazione.transizioni_auto)==0)):
        #print("Il nodo destinazione rispecchia i requisiti, 1 transizione entrante, 1 uscente, no auto transizioni")
        #print("Nodo: " + transizione.nodo_destinazione.to_string())
        lista_sequenza.append(transizione)
        esplora_sequenza(transizione.nodo_destinazione.transizioni[0], lista_sequenza)
    else:
        return

#Algoritmo 3 - Migliorato
def controllo_sequenza_migliorato(nodi, transizioni):
    '''Terzo tipo di semplificazione: sequenza'''
    #print("CONTROLLO PER SEQUENZA AND")


    for t in transizioni:
        sequenza = False
        lista_sequenza = []

        # print("FOR: Analizzo la transizione: ")
        # print(t.to_string())
        # print("\n")
        # print("INFO sulla transizione")
        # print("lunghezza nodo dest transizioni entranti: "+str(len(t.nodo_destinazione.transizioni_sorgente)))
        # print("nodo dest auto transizioni: "+str(len(t.nodo_destinazione.transizioni_auto)))
        # print("nodo dest transizioni: " + str(len(t.nodo_destinazione.transizioni)))

        #il nodo destinazione ha 1 transizione uscente e una entrante
        if ((len(t.nodo_destinazione.transizioni) == 1) and (len(t.nodo_destinazione.transizioni_sorgente) == 1) and (len(t.nodo_destinazione.transizioni_auto)==0)):
            # print("Il nodo destinazione rispecchia i requisiti, 1 transizione entrante, 1 uscente, no auto transizioni")
            # print("Nodo destinazione: "+t.nodo_destinazione.to_string())
            lista_sequenza.append(t)
            lista_sequenza.append(t.nodo_destinazione.transizioni[0])
            sequenza=True
            esplora_sequenza(t.nodo_destinazione.transizioni[0], lista_sequenza)
            #print("ho finito di esplorare la seguenza, è lunga: "+str(len(lista_sequenza)))
            break

    if sequenza:
        #print("Creazione etichetta")
        etichetta=""
        for tra in lista_sequenza:
            etichetta = crea_etichetta_and(etichetta, tra.rilevanza)

        if etichetta=="":
            etichetta=" "


        #print("Ho creato etichetta nuova transizione: "+etichetta)

        #creo transizione
        nodo_sorgente=lista_sequenza[0].nodo_sorgente
        nodo_destinazione=lista_sequenza[len(lista_sequenza)-1].nodo_destinazione
        transizione = Transizione_spazio(nome="nome",nodo_sorgente=nodo_sorgente,nodo_destinazione=nodo_destinazione,osservazione=" ",rilevanza=etichetta)
        transizioni.append(transizione)
        nodo_sorgente.transizioni.append(transizione)
        nodo_destinazione.transizioni_sorgente.append(transizione)


        for index, tra in enumerate(lista_sequenza):
            if index==0:
                if tra.nodo_destinazione in nodi:
                    nodi.remove(tra.nodo_destinazione)
                transizioni.remove(tra)
                #migliorato
                tra.nodo_sorgente.transizioni.remove(tra)
            elif index==len(lista_sequenza)-1:
                if tra.nodo_sorgente in nodi:
                    nodi.remove(tra.nodo_sorgente)
                transizioni.remove(tra)
                tra.nodo_destinazione.transizioni_sorgente.remove(tra)
            else:
                if tra.nodo_sorgente in nodi:
                    nodi.remove(tra.nodo_sorgente)
                if tra.nodo_destinazione in nodi:
                    nodi.remove(tra.nodo_destinazione)
                if tra in transizioni:
                    transizioni.remove(tra)
        #print("NUMERO DI NODI DOPO SEQUENZA: " + str(len(nodi)))
        # for nod in nodi:
        #     print("\t" + nod.to_string() + " numero transizioni: " + str(len(nod.transizioni)))
        return True
    else:
        return False

def controlla_tratti_paralleli_migliorato(transizioni):
    '''Terzo tipo di semplificazione: tratti paralleli'''
    #print("CONTROLLO TRATTI PARALLELI PER OR")

    for t in transizioni:
        paralleli = False
        lista_transizioni = []

        # print("FOR: Analizzo la transizione: ")
        # print(t.to_string())
        # print("\n")
        # print("INFO sulla transizione")
        # print("numero transizioni nodo sorgente: " + str(len(t.nodo_sorgente.transizioni)))
        # print("numero transizioni entranti nodo dest: " + str(len(t.nodo_destinazione.transizioni_sorgente)))

        if ((len(t.nodo_sorgente.transizioni)) > 1 ) and ((len(t.nodo_destinazione.transizioni_sorgente)) > 1 ):
            #print("Il nodo destinazione rispecchia i requisiti")
            #print("Nodo destinazione: " + t.nodo_destinazione.to_string())
            for tra in t.nodo_sorgente.transizioni:
                if t!=tra:
                    if t.nodo_destinazione==tra.nodo_destinazione:
                        # print("trovata transizione parallela:")
                        # print(tra.to_string())
                        lista_transizioni.append(t)
                        lista_transizioni.append(tra)
                        paralleli = True
                        break
        if paralleli:
            break


    if paralleli:
        #print("Creazione etichetta")
        etichetta = ""
        if lista_transizioni[0].rilevanza==" ":
            if lista_transizioni[1].rilevanza==" ":
                etichetta=" "
            else:
                etichetta=lista_transizioni[1].rilevanza+"|ε"
        else:
            if lista_transizioni[1].rilevanza==" ":
                etichetta=lista_transizioni[0].rilevanza+"|ε"
            else:
                etichetta=lista_transizioni[0].rilevanza+"|"+lista_transizioni[1].rilevanza

        #print("Ho creato etichetta nuova transizione: " + etichetta)

        # creo transizione
        nodo_sorgente = lista_transizioni[0].nodo_sorgente
        nodo_destinazione = lista_transizioni[0].nodo_destinazione
        transizione = Transizione_spazio(nome="nome", nodo_sorgente=nodo_sorgente, nodo_destinazione=nodo_destinazione,
                                         osservazione=" ", rilevanza=etichetta)
        transizioni.append(transizione)
        #print("Creo nuova transizione: ")
        #print(transizione.to_string())

        nodo_sorgente.transizioni.append(transizione)
        nodo_destinazione.transizioni_sorgente.append(transizione)


        nodo_sorgente.transizioni.remove(lista_transizioni[0])
        nodo_sorgente.transizioni.remove(lista_transizioni[1])
        nodo_destinazione.transizioni_sorgente.remove(lista_transizioni[0])
        nodo_destinazione.transizioni_sorgente.remove(lista_transizioni[1])
        if lista_transizioni[0] in transizioni:
            transizioni.remove(lista_transizioni[0])
        if lista_transizioni[1] in transizioni:
            transizioni.remove(lista_transizioni[1])
        return True
    else:
        return False

def controlla_nodi_migliorato(nodi, transizioni):
    '''Terzo tipo di semplificazione: auto transizioni'''
    for n in nodi:
        #print("FOR NODO: ")
        #print(n.to_string())
        transizioni_inserite=[]
        trovato=False
        if n.finale==False and n.iniziale==False:
            #transizioni entranti (non auto transizioni)
            for i in [x for x in n.transizioni_sorgente if x.nodo_sorgente!=n]:
                for o in [y for y in n.transizioni if y.nodo_destinazione!=n]:
                    # print("INTERNO FOR, transizioni")
                    # print("Transizione entrante: "+i.to_string())
                    # print("Transizione uscente: " + o.to_string())

                    if len(n.transizioni_auto)==0: #non ci sono autotransizioni
                        #print("n non ha auto transizioni")
                        trovato=True
                        lista_etichette=[]
                        lista_etichette.append(i.rilevanza)
                        lista_etichette.append(o.rilevanza)

                        #print("Creazione etichetta")
                        etichetta = ""
                        for e in lista_etichette:
                            etichetta = crea_etichetta_and(etichetta, e)
                        if etichetta == "":
                            etichetta = " "
                        #print("Ho creato etichetta nuova transizione: " + etichetta)

                        nodo_sorgente = i.nodo_sorgente
                        nodo_destinazione = o.nodo_destinazione
                        transizione = Transizione_spazio(nome="nome", nodo_sorgente=nodo_sorgente,
                                                         nodo_destinazione=nodo_destinazione, osservazione=" ",
                                                         rilevanza=etichetta)
                        transizioni.append(transizione)

                        info=[]
                        info.append(nodo_sorgente)
                        info.append(nodo_destinazione)
                        info.append(transizione)
                        info.append(i)
                        info.append(o)
                        # nodo_sorgente.transizioni.append(transizione)
                        # nodo_destinazione.transizioni_sorgente.append(transizione)
                        # if i in nodo_sorgente.transizioni:
                        #     nodo_sorgente.transizioni.remove(i)
                        # if o in nodo_destinazione.transizioni_sorgente:
                        #     nodo_destinazione.transizioni_sorgente.remove(o)
                        transizioni_inserite.append(info)

                    else: #ci sono autotransizioni
                        #print("n ha auto transizioni")
                        trovato=True
                        for auto in n.transizioni_auto:
                            lista_etichette = []
                            lista_etichette.append(i.rilevanza)
                            lista_etichette.append("("+auto.rilevanza+")*")
                            lista_etichette.append(o.rilevanza)

                            #print("Creazione etichetta")
                            etichetta = ""
                            for e in lista_etichette:
                                etichetta = crea_etichetta_and(etichetta, e)
                            if etichetta == "":
                                etichetta = " "
                            #print("Ho creato etichetta nuova transizione: " + etichetta)

                            nodo_sorgente = i.nodo_sorgente
                            nodo_destinazione = o.nodo_destinazione
                            transizione = Transizione_spazio(nome="nome", nodo_sorgente=nodo_sorgente,
                                                             nodo_destinazione=nodo_destinazione, osservazione=" ",
                                                             rilevanza=etichetta)
                            transizioni.append(transizione)

                            info = []
                            info.append(nodo_sorgente)
                            info.append(nodo_destinazione)
                            info.append(transizione)
                            info.append(i)
                            info.append(o)
                            transizioni_inserite.append(info)
                            # nodo_sorgente.transizioni.append(transizione)
                            # nodo_destinazione.transizioni_sorgente.append(transizione)
                            #
                            # nodo_sorgente.transizioni.remove(i)
                            # nodo_destinazione.transizioni_sorgente.remove(o)

        if trovato:
            #print("Finito FOR sul nodo con successo. Inizio a eliminare parti inutili")
            #scorro lista
            for info in transizioni_inserite:
                nodo_sorgente=info[0]
                nodo_destinazione=info[1]
                transizione=info[2]
                i=info[3]
                o=info[4]
                if(transizione.nodo_sorgente==transizione.nodo_destinazione):
                    nodo_sorgente.transizioni_auto.append(transizione)
                if (transizione not in nodo_sorgente.transizioni):
                    nodo_sorgente.transizioni.append(transizione)
                if (transizione not in nodo_destinazione.transizioni_sorgente):
                    nodo_destinazione.transizioni_sorgente.append(transizione)
                if i in nodo_sorgente.transizioni:
                    nodo_sorgente.transizioni.remove(i)
                if o in nodo_destinazione.transizioni_sorgente:
                    nodo_destinazione.transizioni_sorgente.remove(o)


            if n in nodi:
                nodi.remove(n)
                #print("rimuovo nodo: "+n.to_string())
            for t in n.transizioni:
                if t in transizioni:
                    transizioni.remove(t)
                    #print("rimuovo transizione: " + t.to_string())
            for t in n.transizioni_sorgente:
                if t in transizioni:
                    transizioni.remove(t)
                    #print("rimuovo transizione: " + t.to_string())
            break

def semplifico_transizioni_diagnosi_migliorato(nodi, transizioni):
    '''Metodo per svolgere i passaggi della diagnosi
        Semplificazione di una seguenza
        Semplificazione di transizioni parallele
        Terzo tipo di semplificazione (auto transizione)'''
    #print("\n\n\nSEMPLIFICO TRANSIZIONI")

    sistema_transizioni_da_nodi_e_transizioni(nodi, transizioni)
    #print("Ho corretto sorgente, dest e auto di tutti i nodi")
    i=1
    while (len(transizioni)>1):
        #sistema_transizioni_da_nodi_e_transizioni(nodi, transizioni)
        #print("---------------------iterazione: "+str(i))
        #print("NUMERO DI TRANSIZIONI: "+str(len(transizioni)))
        # for trr in transizioni:
        #     print("\t"+trr.to_string()+"\n")
        #
        # print("NUMERO DI NODI: " + str(len(nodi)))
        # for nod in nodi:
        #     print("\t" + nod.to_string()+" numero transizioni: "+str(len(nod.transizioni)))
        #
        # print("-----------CONTROLLO SEQUENZA")
        sequenza = controllo_sequenza_migliorato(nodi, transizioni)
        if sequenza == False:
            #print("--------CONTROLLO TRATTI PARALLELI")
            tratti = controlla_tratti_paralleli_migliorato(transizioni)
            if tratti==False:
                #print("------------CONTROLLO NODI")
                controlla_nodi_migliorato(nodi, transizioni)
                #sistema_transizioni_da_nodi_e_transizioni(nodi, transizioni)
        nodi_finali = []
        nodi_iniziali = []
        for n in nodi:
            if n.finale:
                nodi_finali.append(n)
            if n.iniziale:
                nodi_iniziali.append(n)

        # spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
        # #sistema_transizioni(spazio)
        # stampa_spazio_ridenominato_su_file(spazio, "SPAZIO", "__"+str(i)+"__")
        # if (i==5):
        #     break
        i=i+1
    return i

def diagnosi_algoritmo_su_spazio_migliorato(spazio):
    '''Metodo per eseguire una diagnosi sullo spazio dato in input'''

    #print("DENTRO LA DIAGNOSI")
    nodi = spazio.nodi
    transizioni=spazio.transizioni



    i=semplifico_transizioni_diagnosi_migliorato(nodi, transizioni)


    #fine output
    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)


    del spazio
    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)
    #ridenominazione_spazio_appena_creato(spazio)
    #print("SPAZIO: ")
    #print(spazio.to_string())
    return spazio,i




def crea_etichetta_and(e1, e2):
    '''Date due etichette queste vengono unite con l'operazione di AND.
    parentesi, ripetizioni e termini ε vengono gestiti di conseguenza'''

    if e2 != " ":
        if e1 == "":
            e1 = e2
        else:
            if ("|" in e1) and ("|" in e2):
                divisione_etichetta = e1.split("|")
                divisione_tra = e2.split("|")
                out = ""
                for e in divisione_etichetta:
                    for t in divisione_tra:
                        # print("Analizzo: "+e+", "+t)
                        if e != "ε" and t != "ε":
                            out = out + e + t + "|"
                        elif e == "ε" and t != "ε":
                            out = out + t + "|"
                        elif e != "ε" and t == "ε":
                            out = out + e + "|"
                        else:
                            out = out + "ε|"
                        # print("out: "+out+"\n")
                e1 = out[:-1]
            elif "|" in e2:
                divisione = e2.split("|")
                out = ""
                for el in divisione:
                    if el != "ε":
                        el = e1 + el
                        out = out + el + "|"
                    else:
                        el = e1
                        out = out + el + "|"
                e1 = out[:-1]
            elif "|" in e1:
                divisione = e1.split("|")
                out = ""
                for el in divisione:
                    if el != "ε":
                        el = el + e2
                        out = out + el + "|"
                    else:
                        el = e2
                        out = out + el + "|"
                e1 = out[:-1]
            else:
                e1 = e1 + e2

    return e1

def sistema_transizioni_da_nodi_e_transizioni(nodi, transizioni):
    '''Dati nodi e transizioni va ad aggiornare transizioni e transizioni sorgenti
    dei vari nodi sulla base delle informazioni contenute nell'array di transizioni'''
    for n in nodi:
        n.transizioni=[]
        n.transizioni_sorgente=[]
        n.transizioni_auto=[]

    for t in transizioni:
        t.nodo_sorgente.transizioni.append(t)
        t.nodo_destinazione.transizioni_sorgente.append(t)

        if t.nodo_sorgente == t.nodo_destinazione:
            t.nodo_sorgente.transizioni_auto.append(t)


