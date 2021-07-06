from Classi.Automa.automa import *
from Classi.Automa.rete import *
from Classi.Spazio.spazio_comportamentale import *
from copy import deepcopy




def crea_spazio_comportamentale(rete):

    print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE")
    rete = rete

    #Salvo l'array degli automi presenti nella rete #rete.automi
    #Salvo l'array dei links presenti nella rete #rete.links
    #Salvo l'array delle transizioni presenti nella rete #rete.transizioni
    automi = rete.automi
    links = rete.links
    transizioni = rete.get_transizioni()

    #creo un array vuoto di nodi dello spazio comportamentale
    nodi = []

    #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
    nodo_attuale = istanzio_nodo_iniziale(rete)
    print("Creo nodo iniziale:")
    print("\t"+nodo_attuale.to_string()+"\n")

    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)
    print("Creata lista di nodi\n")

    controllo_transizioni(nodi, nodo_attuale)





def controllo_transizioni(nodi, nodo_attuale):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    print("\t"+nodo_attuale.to_string()+"\n")

    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    #scorro gli stati
    for s in stati_correnti:
        print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
        print("stato: "+s.nome+"\n")

        #scorro transizioni dello stato
        for t in s.transizioni:
            print("Scorro transizioni, in nodo numero: " +str(nodi.index(nodo_attuale)))
            print("stato: " + t.nome+"\n")

            #controllo se la transizione può scattare
            scatta = scatto_transizione(t, nodo_attuale)

            if(scatta):
                #creo il nuovo nodo generato dallo scatto della transizione
                print("inizio a creare il nuovo nodo")
                nuovo_nodo = deepcopy(nodo_attuale)
                aggiorna_nodo(nuovo_nodo, t)
                print("Nuovo nodo creato con valore " + str(nodi.index(nuovo_nodo)))
                print("\t" + nuovo_nodo.to_string() + "\n")

            else:
                print("La transizione non scatta, esco dal ciclo")






def aggiorna_nodo(nodo, transizione):
    '''dato un nodo e una transizione viene fatta scattare la transizione aggiornando il nodo stesso'''

    #scorro eventi di input
    for evento in transizione.input:
        if (evento.nome != "" and evento.link != None):
            #tolgo i valori dai link di input
            nodo.links[evento.link.nome][1]=""
    for evento in transizione.output:
        if (evento.nome != "" and evento.link != None):
            #inserisco l'evento nel link di output
            nodo.links[evento.link.nome]=evento.nome

    #ricavo la posizione dello stato sorgente
    indice = nodo.stati.index(transizione.stato_sorgente)

    #lo sostituisco con lo stato destinazione
    nodo.stati[indice] = transizione.stato_destinazione



def scatto_transizione(tranizione, nodo):
    '''data una transizione e il nodo attuale viene stabilito se la transizione può scattare
    vengono fatte analisi solo sugli eventi presenti nei link
    non sullo stato di partenza della transizione'''
    scatta=True
    print("Controllo transizione: "+tranizione.nome)

    #scorro eventi in input della transizione
    for evento in tranizione.input:
        print("controllo INPUT")
        #verifico che non sia un evento vuoto
        if(evento.nome != "" and evento.link != None):
            #ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            print("Evento: "+evento.nome+" ("+evento.link.nome+") -> valore nel nodo: "+valore_nel_link)

            if (evento.nome != valore_nel_link):
                print("Non c'è l'input corretto, la transizione non può scattare\n")
                return False

    # scorro eventi in output della transizione
    for evento in tranizione.output:
        print("controllo Output")
        # verifico che non sia un evento vuoto
        if (evento.nome != "" and evento.link != None):
            # ricavo il valore del link nel nodo
            valore_nel_link = nodo.links[evento.link.nome][1]
            print("Evento: " + evento.nome + " (" + evento.link.nome + ") -> valore nel nodo: " + valore_nel_link)

            if (valore_nel_link != ""):
                print("Il link di output non è vuoto, impossibile scattare\n")
                return False
    print("La transizione può scattare\n")
    return scatta



def istanzio_nodo_iniziale(rete):
    '''Partendo dalla rete creo l'istanza del nodo iniziale dello spazio comportamentale'''
    stati_correnti = rete.get_stati_correnti()
    links = dict()
    for l in rete.links:
        links[l.nome] = [l, l.evento.nome]
    nodo_iniziale = Nodo(stati=stati_correnti, check=False, links=links, iniziale=True)
    return nodo_iniziale
