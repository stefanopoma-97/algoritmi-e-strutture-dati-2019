from Classi.Automa.automa import *
from Classi.Automa.rete import *
from Classi.Spazio.spazio_comportamentale import *
from copy import deepcopy

#ALGORITMO 1, manuale
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
                        commento="creo transizione: "+tra.nome+", che si collega al nuovo nodo: ["+nuovo_nodo.output+"]"
                        return [nodi, nuovo_nodo, transizioni_spazio, commento]

                else:
                    print("La transizione non scatta, esco dal ciclo")


    print("CHECKED ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True
    commento="analizzate tutte le possibili transizioni del nodo: ["+nodo_attuale.output+"]\n necessario passare al prossimo nodo"
    return [nodi, nodo_attuale, transizioni_spazio, commento]

#ALGORITMO 1
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
    ridenominazione_spazio_appena_creato(spazio)
    return spazio

def ridenominazione_spazio_appena_creato(spazio):
    for i in range(len(spazio.nodi)):
        spazio.nodi[i].id = str(i)

def sistema_transizioni(spazio):
    print("SISTEMA TRANSIZIONI SPAZIO")
    for t in spazio.transizioni:
        t.nodo_sorgente.transizioni.append(t)
        t.nodo_destinazione.transizioni_sorgente.append(t)
        if (t.nome == "t1c"):
            print("TRANSIZIONE T1C")
            print("Sorgente: "+t.nodo_sorgente.output)
            print("destinazione: " + t.nodo_destinazione.output)

            print("DA DESTINAZIONE scorro transizioni")
            for u in t.nodo_destinazione.transizioni_sorgente:
                print("\t"+u.nome)
        else:
            print("NON TROVATA T1C")




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


#ALGORITMO 2 - MANUALE
def crea_spazio_comportamentale_manuale2(rete, osservazione, *args):

    print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE DA OSSERVAZIONE MANUALMENTE")
    rete = rete

    if len(args)==0:
        #Salvo l'array degli automi presenti nella rete #rete.automi
        #Salvo l'array dei links presenti nella rete #rete.links
        #Salvo l'array delle transizioni presenti nella rete #rete.transizioni
        automi = rete.automi
        links = rete.links
        transizioni = rete.get_transizioni()
        # creo un array vuoto di nodi dello spazio comportamentale
        nodi = []

        nodo_attuale = istanzio_nodo_iniziale2(rete)
        print("Creo nodo iniziale:")
        print("\t" + nodo_attuale.to_string() + "\n")

        # Inserisco il nodo iniziale nell'array
        nodi.append(nodo_attuale)
        print("Creata lista di nodi\n")
        transizioni = []
        global indice
        indice = 0


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



    out= controllo_transizioni_manualmente2(nodi, nodo_attuale, transizioni, osservazione)

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

def controllo_transizioni_manualmente2(nodi, nodo_attuale, transizioni_spazio, osservazione):
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

            salto=False
            for t_spazio in transizioni_spazio:
                if t.nome == t_spazio.nome and t_spazio.nodo_sorgente==nodo_attuale:
                    salto = True
                    print("Transizione già inserita la salto")

            if salto:
                print("la salto")
            else:
                # controllo se la transizione può scattare
                scatta = scatto_transizione2(t, nodo_attuale, osservazione)

                if (scatta):

                    print("inizio a creare il nuovo nodo")
                    nuovo_nodo = deepcopy(nodo_attuale)
                    nuovo_nodo.iniziale = False
                    nuovo_nodo = aggiorna_nodo2(nuovo_nodo, t, nodo_attuale.lunghezza_osservazione)
                    nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                    nuovo_nodo.output = nuovo_nodo.get_output()

                    print("Nuovo nodo creato")
                    print("\t" + nuovo_nodo.to_string() + "\n")
                    # controllo che il nodo sia nuovo
                    contiene = contiene_nodo_con_osservazione(nuovo_nodo, nodi)

                    if (isinstance(contiene, Nodo)):
                        if contiene.iniziale:
                            contiene.finale = True
                        print("aggionro l_osservazione del vecchio nodo")
                        contiene.lunghezza_osservazione = nuovo_nodo.lunghezza_osservazione
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
                        commento = "creo transizione: " + tra.nome + ", che si collega al nuovo nodo: [" + nuovo_nodo.output + "]"
                        return [nodi, nuovo_nodo, transizioni_spazio, commento]
                else:
                    print("La transizione non scatta, esco dal ciclo")


    print("CHECKED ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True
    commento="analizzate tutte le possibili transizioni del nodo: ["+nodo_attuale.output+"]\n necessario passare al prossimo nodo"
    return [nodi, nodo_attuale, transizioni_spazio, commento]

def controllo_transizioni_manualmente2_modificato(nodi, nodo_attuale, transizioni_spazio, osservazione):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    print("\t"+nodo_attuale.to_string()+"\n")

    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    tra = []
    for s in stati_correnti:
        tra += s.transizioni

    transizioni = []
    for t in tra:
        if t.osservazione != " ":
            transizioni.insert(0, t)
        else:
            transizioni.insert(len(transizioni), t)

    print("NODO: "+nodo_attuale.to_string())
    print("TRANSIZIONI: "+str(transizioni))

    for t in transizioni:
        print("FOR")
        print("transizione: " + t.nome+"\n")

        salto=False
        for t_spazio in transizioni_spazio:
            if t.nome == t_spazio.nome and t_spazio.nodo_sorgente==nodo_attuale:
                salto = True
                print("Transizione già inserita la salto")

        if salto:
            print("la salto")
        else:
            # controllo se la transizione può scattare
            scatta = scatto_transizione2_modificato(t, nodo_attuale, osservazione)

            if (scatta):
                if t.osservazione != " ":
                    #nodo_attuale.passata_osservazione = True
                    listOfGlobals = globals()
                    listOfGlobals['indice'] = listOfGlobals['indice'] + 1
                print("inizio a creare il nuovo nodo")
                nuovo_nodo = deepcopy(nodo_attuale)
                nuovo_nodo.iniziale = False
                nuovo_nodo = aggiorna_nodo2(nuovo_nodo, t, nodo_attuale.lunghezza_osservazione)
                nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                nuovo_nodo.output = nuovo_nodo.get_output()

                print("Nuovo nodo creato")
                print("\t" + nuovo_nodo.to_string() + "\n")
                # controllo che il nodo sia nuovo
                contiene = contiene_nodo_con_osservazione(nuovo_nodo, nodi)

                if (isinstance(contiene, Nodo)):
                    if contiene.iniziale:
                        contiene.finale = True
                    print("aggionro l_osservazione del vecchio nodo")
                    contiene.lunghezza_osservazione = nuovo_nodo.lunghezza_osservazione
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
                    commento = "creo transizione: " + tra.nome + ", che si collega al nuovo nodo: [" + nuovo_nodo.output + "]"
                    return [nodi, nuovo_nodo, transizioni_spazio, commento]
            else:
                print("La transizione non scatta, esco dal ciclo")


    print("CHECKED ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True
    commento="analizzate tutte le possibili transizioni del nodo: ["+nodo_attuale.output+"]\n necessario passare al prossimo nodo"
    return [nodi, nodo_attuale, transizioni_spazio, commento]

#ALGORITMO 2
def sistema_transizioni2(spazio):
    print("SISTEMA TRANSIZIONI SPAZIO")

    # prima svuoto transizioni dai nodi però
    for n in spazio.nodi:
        n.transizioni = []
        n.transizioni_sorgente = []

    for t in spazio.transizioni:
        t.nodo_sorgente.transizioni.append(t)
        t.nodo_destinazione.transizioni_sorgente.append(t)
        if (t.nome == "t1c"):
            print("TRANSIZIONE T1C")
            print("Sorgente: " + t.nodo_sorgente.output)
            print("destinazione: " + t.nodo_destinazione.output)

            print("DA DESTINAZIONE scorro transizioni")
            for u in t.nodo_destinazione.transizioni_sorgente:
                print("\t" + u.nome)
        else:
            print("NON TROVATA T1C")

def crea_spazio_comportamentale2_da_spazio(spazio, osservazione):

    print("\n\n\n---------------------------------\nCREO SPAZIO COMPORTAMENTALE CON OSSERVAZIONE DA SPAZIO")
    spazio = spazio
    osservazione=osservazione

    #creo un array vuoto di nodi dello spazio comportamentale
    nodi = []

    #Istanzio il nodo iniziale partendo dagli stati iniziali dei vari automi e dal contenuto dei link
    nodo_attuale = spazio.nodi[0]
    for n in spazio.nodi:
        n.lunghezza_osservazione=0
    nodo_attuale.lunghezza_osservazione=0

    nodo_attuale.finale=False
    print("Creo nodo iniziale:")
    print("\t"+nodo_attuale.to_string()+"\n")


    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)
    print("Creata lista di nodi\n")
    transizioni=[]


    controllo_transizioni2_da_spazio(nodi, transizioni, osservazione, spazio, nodo_attuale)

    nodi_finali=[]
    nodi_iniziali=[]
    for n in nodi:
        if n.finale:
            nodi_finali.append(n)
        if n.iniziale:
            nodi_iniziali.append(n)
    spazio_out = Spazio_comportamentale(spazio.nome, nodi_finali, nodi_iniziali, nodi, transizioni)
    print("Sistema transizioni")
    sistema_transizioni2(spazio_out)
    print("ridenominazione")
    ridenominazione_spazio_appena_creato(spazio_out)
    print("FINE CREAZIONE SPAZIO COMPORTAMENTALE")
    return spazio_out

def controllo_transizioni2_da_spazio(nodi, transizioni_spazio, osservazione, spazio, nodo_attuale):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    nodo=nodo_attuale
    #scorro nodi
    print("ANALIZZO NODO")
    print("NODO: "+nodo.to_string())


    #scorro transizioni dello stato
    for t in nodo.transizioni:
        print("FOR transizioni")
        print("nodo: "+nodo.to_string())
        print("transizione: "+t.nome)

        #controllo se la transizione può scattare
        scatta = scatto_transizione2_da_spazio(t, nodo, osservazione)

        if(scatta):
            #creo il nuovo nodo generato dallo scatto della transizione
            print("inizio a creare il nuovo nodo")
            if t.osservazione!=" ":
                nodo.passata_osservazione=True

            #calcolo indice nuovo nodo
            if t.osservazione != " ":
                print("La transizione ha un valore di osservazione: " + t.osservazione)
                indice=nodo.lunghezza_osservazione + 1
                print("Aggiornato il valore del nuovo nodo di l_osservazione")
            else:
                indice = nodo.lunghezza_osservazione

            nuovo_nodo = t.nodo_destinazione
            contiene = contiene_nodo(nuovo_nodo, nodi)
            if (isinstance(contiene, Nodo)):
                print("il nodo destinazione esiste già")
                if contiene.lunghezza_osservazione==indice:
                    print("effettivamente è lo stesso nodo")
                    if contiene.iniziale and contiene.lunghezza_osservazione == len(osservazione):
                        contiene.finale = True
                    tra = Transizione_spazio(t.nome, nodo, contiene, t.osservazione, t.rilevanza)
                    transizioni_spazio.append(tra)
                    # nodo_attuale.transizioni.append(tra)
                    print("Inserita la nuova transizione: ")
                    print("\t" + t.to_string())
                    print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                else:
                    print("l'indice è diverso, verrà creato un nodo separato")
                    nuovo_nodo = deepcopy(t.nodo_destinazione)
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

                    print("Nuovo nodo (aggiornato) creato ")
                    print("\t" + nuovo_nodo.to_string() + "\n")
                    controllo_transizioni2_da_spazio(nodi, transizioni_spazio, osservazione, spazio, nuovo_nodo)


            else:
                print("Inserisco il nuovo nodo")

                nuovo_nodo.iniziale = False
                nuovo_nodo.check = False
                nuovo_nodo.finale = False
                nuovo_nodo.lunghezza_osservazione = indice
                nuovo_nodo.passata_osservazione = False
                nuovo_nodo.finale = nuovo_nodo.is_finale_oss(len(osservazione))
                nuovo_nodo.output = nuovo_nodo.get_output()

                nodi.append(nuovo_nodo)
                print("Il suo indice è " + str(nodi.index(nuovo_nodo)))
                tra = Transizione_spazio(t.nome, nodo, nuovo_nodo, t.osservazione, t.rilevanza)
                transizioni_spazio.append(tra)
                #nodo_attuale.transizioni.append(tra)
                print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                print("Creata la nuova transizione: ")
                print("\t" + t.to_string())
                print("numero totale di transizioni: " + str(len(transizioni_spazio)))
                controllo_transizioni2_da_spazio(nodi, transizioni_spazio, osservazione, spazio, nuovo_nodo)

        else:
            print("La transizione non scatta, esco dal ciclo")
    print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo)))
    nodo.check = True

def scatto_transizione2_da_spazio(transizione, nodo, osservazioni):
    '''data una transizione e il nodo attuale viene stabilito se la transizione può scattare
    vengono fatte analisi solo sugli eventi presenti nei link
    non sullo stato di partenza della transizione'''
    scatta=True
    print("Controllo transizione: "+transizione.nome)


    if transizione.osservazione != " ":
        print("La transizione contiene un valore di osservazione: "+transizione.osservazione)
        print("Osservazioni con lunghezza: "+str(len(osservazioni)))
        print("Valore di l_osservazione nel nodo: " + str(nodo.lunghezza_osservazione))


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


    return scatta

def crea_spazio_comportamentale2(rete, osservazione):

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
    print("Creo nodo iniziale:")
    print("\t"+nodo_attuale.to_string()+"\n")

    #Inserisco il nodo iniziale nell'array
    nodi.append(nodo_attuale)
    print("Creata lista di nodi\n")
    transizioni=[]
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
    ridenominazione_spazio_appena_creato(spazio)
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
            scatta = scatto_transizione2(t, nodo_attuale, osservazione)

            if(scatta):
                #creo il nuovo nodo generato dallo scatto della transizione
                print("inizio a creare il nuovo nodo")
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

def controllo_transizioni2_modificato(nodi, nodo_attuale, transizioni_spazio, osservazione):
    '''Partendo dal nodo attuale controllo tutte le transizioni che possono scattare e le faccio scattare'''
    print("Controllo transizioni in nodo numero: "+str(nodi.index(nodo_attuale)))
    print("\t"+nodo_attuale.to_string()+"\n")


    #ricavo gli stati correnti del nodo analizzato, una transizione scatta solo se parte da uno di questi stati
    stati_correnti = nodo_attuale.stati

    tra=[]
    for s in stati_correnti:
        tra+=s.transizioni

    transizioni=[]
    for t in tra:
        if t.osservazione!=" ":
            transizioni.insert(0, t)
        else:
            transizioni.insert(len(transizioni), t)


    for t in transizioni:
        print("Scorro stati, in nodo numero: " + str(nodi.index(nodo_attuale)))
        print("il nodo ha transizioni (nodo attuale.transizioni): " + str(len(nodo_attuale.transizioni)))
        print("FOR LOOP. stato: " + s.nome + "\n")
        print("Scorro transizioni, in nodo numero (id): " +str(nodi.index(nodo_attuale)))
        print("nodo: "+nodo_attuale.to_string())
        print("transizione: "+t.nome+"\n")

        #controllo se la transizione può scattare
        scatta = scatto_transizione2_modificato(t, nodo_attuale, osservazione)

        if(scatta):
            #creo il nuovo nodo generato dallo scatto della transizione
            print("inizio a creare il nuovo nodo")
            if t.osservazione!=" ":
                #nodo_attuale.passata_osservazione=True
                listOfGlobals = globals()
                listOfGlobals['indice'] = listOfGlobals['indice']+1
            nuovo_nodo = deepcopy(nodo_attuale)
            nuovo_nodo.iniziale = False
            #nuovo_nodo.passata_osservazione=False
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
                controllo_transizioni2_modificato(nodi, nuovo_nodo, transizioni_spazio, osservazione)

        else:
            print("La transizione non scatta, esco dal ciclo")

    print("ho concluso tutte gli stati di nodo: " + str(nodi.index(nodo_attuale)))
    nodo_attuale.check = True


def scatto_transizione2(tranizione, nodo, osservazioni):
    '''data una transizione e il nodo attuale viene stabilito se la transizione può scattare
    vengono fatte analisi solo sugli eventi presenti nei link
    non sullo stato di partenza della transizione'''
    scatta=True
    print("Controllo transizione: "+tranizione.nome)


    if tranizione.osservazione != " ":
        print("La transizione contiene un valore di osservazione: "+tranizione.osservazione)

        print("Osservazioni con lunghezza: "+str(len(osservazioni)))
        print("Valore di l_osservazione nel nodo: " + str(nodo.lunghezza_osservazione))
        #print("Valore dell'indice complessivo: "+str(indice))

        # if indice == len(osservazioni):
        #     print("Indice vale: "+str(indice))
        #     print("La lunghezza delle osservazioni è: "+str(len(osservazioni)))
        #     print("SALTO")
        #     return False
        #
        # if (osservazioni[indice]!=tranizione.osservazione):
        #     print("rispetto all'indice mi serve il valore: "+osservazioni[indice])
        #     print("il nodo contiene: "+tranizione.osservazione)
        #     print("NON COINCIDONO, salto")
        #     return False

        if nodo.lunghezza_osservazione == len(osservazioni):
            print("len osservazione è già uguale a: " + str(nodo.lunghezza_osservazione) + ", non posso aggiungerne altre")
            return False
        else:
            if(osservazioni[nodo.lunghezza_osservazione]!=tranizione.osservazione):
                print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
                print("La transizione ha il seguente valore: "+tranizione.osservazione)
                print("NON coincidono")
                return False
            else:
                print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
                print("La transizione ha il seguente valore: " + tranizione.osservazione)
                print("Coincidono")

        if nodo.passata_osservazione:
            print("IL nodo ha già una transizione uscente con l'etichetta di osservazione cercata")
            print("NON SCATTA")
            return False

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

def scatto_transizione2_modificato(tranizione, nodo, osservazioni):
    '''data una transizione e il nodo attuale viene stabilito se la transizione può scattare
    vengono fatte analisi solo sugli eventi presenti nei link
    non sullo stato di partenza della transizione'''
    scatta=True
    print("Controllo transizione: "+tranizione.nome)
    listOfGlobals = globals()
    indice = listOfGlobals['indice']

    if tranizione.osservazione != " ":
        print("La transizione contiene un valore di osservazione: "+tranizione.osservazione)

        print("Osservazioni con lunghezza: "+str(len(osservazioni)))
        print("Valore di l_osservazione nel nodo: " + str(nodo.lunghezza_osservazione))
        print("Valore dell'indice complessivo: "+str(indice))

        if indice == len(osservazioni):
            print("Indice vale: "+str(indice))
            print("La lunghezza delle osservazioni è: "+str(len(osservazioni)))
            print("SALTO")
            return False

        if (osservazioni[indice]!=tranizione.osservazione):
            print("rispetto all'indice mi serve il valore: "+osservazioni[indice])
            print("il nodo contiene: "+tranizione.osservazione)
            print("NON COINCIDONO, salto")
            return False

        # if nodo.lunghezza_osservazione == len(osservazioni):
        #     print("len osservazione è già uguale a: " + str(nodo.lunghezza_osservazione) + ", non posso aggiungerne altre")
        #     return False
        # else:
        #     if(osservazioni[nodo.lunghezza_osservazione]!=tranizione.osservazione):
        #         print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
        #         print("La transizione ha il seguente valore: "+tranizione.osservazione)
        #         print("NON coincidono")
        #         return False
        #     else:
        #         print("il valore che mi serve nelle osservazioni è: " + osservazioni[nodo.lunghezza_osservazione])
        #         print("La transizione ha il seguente valore: " + tranizione.osservazione)
        #         print("Coincidono")

        # if nodo.passata_osservazione:
        #     print("IL nodo ha già una transizione uscente con l'etichetta di osservazione cercata")
        #     print("NON SCATTA")
        #     return False

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


def aggiorna_nodo2(nodo, transizione, l_osservazione):
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

    if transizione.osservazione!=" ":
        print("La transizione ha un valore di osservazione: "+transizione.osservazione)
        nodo.lunghezza_osservazione= l_osservazione + 1
        print("Aggiornato il valore del nuovo nodo di l_osservazione")

    return nodo

def ridenominazione_spazio_appena_creato(spazio):
    for i in range(len(spazio.nodi)):
        spazio.nodi[i].id = str(i)


def crea_nuova_transizione(sorgente, destinazione, transizione):
    nuova_transizione = Transizione_spazio(transizione.nome, sorgente, destinazione, transizione.osservazione, transizione.rilevanza)
    return nuova_transizione









#POTATURA
def potatura_e_ridenominazione(spazio):

    nodi_finali = spazio.nodi_finali
    potatura(nodi_finali)
    print("SPAZIO DOPO POTATURA")
    i = 0
    # for t in spazio.transizioni:
    #     print(str(i) + ") " + "ID: " + t.nodo_sorgente.id + "(" + str(
    #         t.nodo_sorgente.potato) + ") - " + t.nome + " potata: " + str(t.potato) + ", " + str(
    #         t.nodo_destinazione.id) + "(" + str(t.nodo_destinazione.potato) + ")")
    #     i = i + 1
    ridenominazione_dopo_potatura(spazio)
    for n in spazio.nodi:
        print("NODO: "+str(n.id))
        for t in n.transizioni_sorgente:
            print(str(i) + ") " + "ID: " + t.nodo_sorgente.id + "(" + str(
                t.nodo_sorgente.potato) + ") - " + t.nome + " potata: " + str(t.potato) + ", " + str(
                t.nodo_destinazione.id) + "(" + str(t.nodo_destinazione.potato) + ")")
            i = i + 1
    spazio.spazio_potato=True
    print("Durante POTATURA")
    i = 0
    # print("SPAZIO DOPO POTATURA")
    # i = 0
    # for t in spazio.transizioni:
    #     print(str(i) + ") " + "ID: " + t.nodo_sorgente.id + "(" + str(
    #         t.nodo_sorgente.potato) + ") - " + t.nome + " potata: " + str(t.potato) + ", " + str(
    #         t.nodo_destinazione.id) + "(" + str(t.nodo_destinazione.potato) + ")")
    #     i = i + 1
    return spazio

def potatura(nodi):
    for n in nodi:
        salva_nodo_da_potatura(n)
        for t in n.transizioni_sorgente:
            t.potato=False
            # print("NODO ID: " + str(n.id)+ "potato: "+str(n.potato))
            # print("TRANSIZIONE: " + t.nome + ", potata: " + str(t.potato))
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

def crea_spazio_da_spazio_potato(spazio):
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


    print("SALVATAGGIO")
    for n in nuovo_spazio.nodi:
        print("NODO: " + n.to_string())
        for t in n.transizioni:
            print("\t" + t.to_string() + "transizione potata= " + str(t.potato))

    return  nuovo_spazio


def crea_spazio_da_spazio(spazio):
    nuovo_spazio = deepcopy(spazio)

    for n in nuovo_spazio.nodi:
        ripristina_nodo(n)

    for t in nuovo_spazio.transizioni:
        ripristina_transizione(t)

    for t in nuovo_spazio.transizioni:
        t.nodo_sorgente.transizioni.append(t)
        t.nodo_destinazione.transizioni_sorgente.append(t)

    return nuovo_spazio