from Classi.Automa.automa import *
from Classi.Automa.rete import *
from Classi.Spazio.spazio_comportamentale import *
from copy import deepcopy

def crea_spazio_comportamentale_manuale(rete, *args):

    print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE MANUALMENTE")
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
        print("Creo nodo iniziale:")
        print("\t"+nodo_attuale.to_string()+"\n")

        #Inserisco il nodo iniziale nell'array
        nodi.append(nodo_attuale)
        #nodi_da_scorrete.append(nodo_attuale)

        transizioni=[]
    else:
        print("RIPRENDO DA SITUAZIONE PRECEDENTE")

        nodi = args[0]
        nodo_attuale = args[1]
        transizioni = args[2]
        print("numero nodi: " + str(len(nodi)))
        print("Nodo Attuale: " + nodo_attuale.to_string())
        fine = False
        if nodo_attuale.check==True:
            fine = True
            for n in nodi:
                if n.check == False:
                    nodo_attuale=n
                    fine = False

        if fine:
            print("FINE, non ci sono altri nodi da controllare FINE")
            return nodi, nodo_attuale, transizioni, True, "Non ci sono altri nodi da analizzare"



    out= controllo_transizioni_manualmente(nodi, nodo_attuale, transizioni)

    # nodi_finali=[]
    # nodi_iniziali=[]
    # for n in nodi:
    #     if n.finale:
    #         nodi_finali.append(n)
    #     if n.iniziale:
    #         nodi_iniziali.append(n)
    # spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    # sistema_transizioni(spazio)
    nodi = out[0]
    nodo_attuale = out[1]
    transizioni = out[2]
    commento = out[3]

    return nodi, nodo_attuale, transizioni, False, commento

def controllo_transizioni_manualmente(nodi, nodo_attuale, transizioni_spazio):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    print("\t"+nodo_attuale.to_string()+"\n")

    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    #scorro gli stati
    for s in stati_correnti:
        print("Scorro stati, in nodo numero: "+str(nodi.index(nodo_attuale)))
        print("il nodo ha transizioni: "+str(len(nodo_attuale.transizioni)))
        print("stato: "+s.nome+"\n")

        #scorro transizioni dello stato
        for t in s.transizioni:
            print("Scorro transizioni, in nodo numero: " +str(nodi.index(nodo_attuale)))
            print("stato: " + t.nome+"\n")

            salto = False
            for t_spazio in transizioni_spazio:
                if t.nome == t_spazio.nome and t_spazio.nodo_sorgente==nodo_attuale:
                    salto = True
                    print("Transizione già inserita la salto")

            if salto:
                print("la salto")
            else:
                # controllo se la transizione può scattare
                scatta = scatto_transizione(t, nodo_attuale)

                if (scatta):
                    # creo il nuovo nodo generato dallo scatto della transizione
                    print("inizio a creare il nuovo nodo")
                    nuovo_nodo = deepcopy(nodo_attuale)
                    nuovo_nodo.iniziale = False
                    nuovo_nodo = aggiorna_nodo(nuovo_nodo, t)
                    nuovo_nodo.finale = nuovo_nodo.is_finale()
                    nuovo_nodo.output = nuovo_nodo.get_output()

                    print("Nuovo nodo creato")
                    print("\t" + nuovo_nodo.to_string() + "\n")
                    # controllo che il nodo sia nuovo
                    contiene = contiene_nodo(nuovo_nodo, nodi)
                    if (isinstance(contiene, Nodo)):
                        print("Il nuovo nodo è già presente nella lista")
                        if contiene.iniziale:
                            contiene.finale = True
                        tra = crea_nuova_transizione(nodo_attuale, contiene, t)
                        transizioni_spazio.append(tra)
                        # nodo_attuale.transizioni.append(tra)
                        print("Creata la nuova transizione: ")
                        print("\t" + tra.to_string())
                        print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                    else:
                        print("Inserisco il nuovo nodo")
                        nodi.append(nuovo_nodo)
                        print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                        tra = crea_nuova_transizione(nodo_attuale, nuovo_nodo, t)
                        transizioni_spazio.append(tra)
                        # nodo_attuale.transizioni.append(tra)
                        print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                        print("Creata la nuova transizione: ")
                        print("\t" + tra.to_string())
                        print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                        commento="creo transizione: "+tra.nome+", che si collega al nuovo nodo: "+nuovo_nodo.to_string()
                        return [nodi, nuovo_nodo, transizioni_spazio, commento]

                else:
                    print("La transizione non scatta, esco dal ciclo")


    print("CHECKED ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True
    commento="analizzate tutte le possibili transizioni del nodo: "+nodo_attuale.to_string()+"\n necessario passare al prossimo nodo"
    return [nodi, nodo_attuale, transizioni_spazio, commento]




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
    transizioni=[]

    controllo_transizioni(nodi, nodo_attuale, transizioni)

    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)
    spazio = Spazio_comportamentale("spazio1", nodi_finali, nodi_iniziali, nodi, transizioni)
    sistema_transizioni(spazio)

    return spazio


def sistema_transizioni(spazio):
    for t in spazio.transizioni:
        t.nodo_sorgente.transizioni.append(t)
        t.nodo_destinazione.transizioni_sorgente.append(t)



def controllo_transizioni(nodi, nodo_attuale, transizioni_spazio):
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
            print("transizione: "+t.nome+"\n")

            #controllo se la transizione può scattare
            scatta = scatto_transizione(t, nodo_attuale)

            if(scatta):
                #creo il nuovo nodo generato dallo scatto della transizione
                print("inizio a creare il nuovo nodo")
                nuovo_nodo = deepcopy(nodo_attuale)
                nuovo_nodo.iniziale = False
                nuovo_nodo = aggiorna_nodo(nuovo_nodo, t)
                nuovo_nodo.finale = nuovo_nodo.is_finale()
                nuovo_nodo.output = nuovo_nodo.get_output()

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
                    controllo_transizioni(nodi, nuovo_nodo, transizioni_spazio)

            else:
                print("La transizione non scatta, esco dal ciclo")

    print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True



def crea_nuova_transizione(sorgente, destinazione, transizione):
    nuova_transizione = Transizione_spazio(transizione.nome, sorgente, destinazione, transizione.osservazione, transizione.rilevanza)
    return nuova_transizione




def aggiorna_nodo(nodo, transizione):
    '''dato un nodo e una transizione viene fatta scattare la transizione aggiornando il nodo stesso'''
    print("aggiorno i valori del nuovo nodo")
    #scorro eventi di input
    for evento in transizione.input:
        print("input")
        if (evento.nome != "" and evento.link != None):
            #tolgo i valori dai link di input
            nodo.links[evento.link.nome][1]=""
            print("ho aggiornato "+evento.link.nome+" mettendolo a "+ nodo.links[evento.link.nome][1])
    for evento in transizione.output:
        print("output")
        if (evento.nome != "" and evento.link != None):
            #inserisco l'evento nel link di output
            nodo.links[evento.link.nome][1]=evento.nome
            print("ho aggiornato "+evento.link.nome+" mettendolo a "+ nodo.links[evento.link.nome][1])


    #ricavo la posizione dello stato sorgente
    for index, s in enumerate(nodo.stati):
        print("Scorro stato: "+s.to_string()+" = "+str(s))
        print("devo confrontarlo con: "+transizione.stato_sorgente.to_string()+" = "+str(transizione.stato_sorgente))
        if s.id == transizione.stato_sorgente.id:
            print("ho aggiornato lo stato "+nodo.stati[index].nome)
            nodo.stati[index] = transizione.stato_destinazione
            print(" mettendolo a " +nodo.stati[index].nome)

    return nodo




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



def potatura_e_ridenominazione(spazio):
    for i in range(len(spazio.nodi)):
        spazio.nodi[i].id = str(i)


    nodi_finali = spazio.nodi_finali
    potatura(nodi_finali)
    return spazio

def potatura(nodi):
    for n in nodi:
        salva_nodo_da_potatura(n)
        for t in n.transizioni_sorgente:
            if t.nodo_sorgente.potato == True:
                potatura([t.nodo_sorgente])

def salva_nodo_da_potatura(nodo):
    nodo.potato=False
    for t in nodo.transizioni_sorgente:
        t.potato=False