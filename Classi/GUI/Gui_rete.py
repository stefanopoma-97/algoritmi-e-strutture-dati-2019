import copy

import PySimpleGUI as sg
from tkinter.filedialog import askopenfilename
from Classi.GestioneFile.input_output import *
from Classi.Automa.automa import *
from Classi.Automa.rete import *
from Classi.GestioneFile.grafici import *
from Classi.Automa.rete import *
from Classi.GestioneFile.input_output import *
import datetime
from Classi.Spazio.spazio_comportamentale import *
from Classi.Algoritmi.algoritmo_spazio_comportamentale import *
import os



def gui_crea_rete():
    '''Gui per gestire la creazione di una Rete'''
    # Variabili
    global stato, cartella, automi, links, rete, cartella_save, elenco_cartelle
    stato = "1"
    cartella = ""
    cartella_save = ""
    automi = []
    links = []
    elenco_cartelle = []
    rete = None

    def crea_layout_crea_rete():
        colonna1 = [
            [
                sg.Text("Seleziona cartella"),
                sg.Input(key='input_cartella', size=(20, 1)),
                sg.Button('Conferma', key='conferma_cartella')
            ],
            [
                sg.Button("Carica Automa", key="carica_automa", disabled=True),
                sg.Button("Carica Link", key="carica_link", disabled=True),
                sg.Button("Carica Transizioni", key="carica_transizioni", disabled=True)
            ],
            [
                sg.Button("Reset", key="reset", disabled=False),
                sg.Button("Salva su file", key="salva", disabled=True),
                sg.Button("Mostra grafici", key="stampa", disabled=True),
                sg.Button("Carica rete 1", key="rete1", disabled=False),
                sg.Button("Carica rete 2", key="rete2", disabled=False),
                sg.Button("Carica rete 3", key="rete3", disabled=False)
            ],
            [
                sg.Button("Spazio comportamentale", key="spazio_comportamentale", disabled=True),
            ],
            [
                sg.Text("Automi:"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 10), key="automi", autoscroll=True
                )
            ],
            [
                sg.Text("Link:"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 5), key="link", autoscroll=True
                )
            ],
            [
                sg.Text("Reti:"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 10), key="rete", autoscroll=True
                )
            ],
        ]

        colonna2 = [
            [
                sg.Text("Informazioni"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 20), key="informazioni", autoscroll=True
                )
            ],
        ]

        layout_crea_rete = [
            [
                sg.Column(colonna1),
                sg.VSeperator(),
                sg.Column(colonna2),
            ]
        ]

        return layout_crea_rete

    def aggiorna_elenco_automi():
        '''Aggiorna l'elenco degli automi inseriti'''
        listOfGlobals = globals()
        automi = listOfGlobals['automi']

        window_crea_rete['automi'].update("")
        if len(automi)!=0:
            for a in automi:
                window_crea_rete['automi'].update(
                    window_crea_rete['automi'].get() + "\n"+a.to_string())


    def aggiorna_elenco_links():
        '''Aggiorna l'elenco dei link inseriti'''
        listOfGlobals = globals()
        links = listOfGlobals['links']

        window_crea_rete['link'].update("")
        if len(links)!=0:
            for l in links:
                window_crea_rete['link'].update(
                    window_crea_rete['link'].get() + "\n"+l.to_string())

    def aggiorna_rete():
        '''Aggiorna l'elenco delle transizioni inserite'''
        listOfGlobals = globals()
        rete = listOfGlobals['rete']

        window_crea_rete['rete'].update("")
        if rete is not None:
            window_crea_rete['rete'].update(
                window_crea_rete['rete'].get() + "\n"+rete.to_string())

    def conferma_cartella():
        '''Metodo per selezionare la cartella di salvataggio
        non si possono inserire due nomi identici
        il nome della cartella verrà preceduto dalla data attuale: %Y_%m_%d_%H_%M'''
        listOfGlobals = globals()
        cartella = listOfGlobals['cartella']
        stato = listOfGlobals['stato']
        cartella_save = listOfGlobals['cartella_save']
        elenco_cartelle = listOfGlobals['elenco_cartelle']

        stato="conferma cartella"

        if values['input_cartella'] != "":
            if len(elenco_cartelle)!=0 and values['input_cartella'] in elenco_cartelle:
                sg.Popup('Attenzione!',
                         'Cartella già usata')
            else:
                cartella = values['input_cartella']
                elenco_cartelle.append(values['input_cartella'])
                x = datetime.datetime.now()
                data_attuale = str(x.strftime("%Y_%m_%d_%H_%M"))
                cartella_save = data_attuale + "_" + cartella
                window_crea_rete['conferma_cartella'].update(disabled=True)
                window_crea_rete['input_cartella'].update(disabled=True)
                window_crea_rete['carica_automa'].update(disabled=False)
                window_crea_rete['informazioni'].update(window_crea_rete['informazioni'].get()+"\nCartella selezionata: "+cartella)
                listOfGlobals['cartella']=cartella
                listOfGlobals['stato']=stato
                listOfGlobals['cartella_save'] = cartella_save
                listOfGlobals['elenco_cartelle'] = elenco_cartelle
        else:
            sg.Popup('Attenzione!',
                     'Inserire un nome non vuoto')

    def carica_automa():
        '''Metodo per permettere il caricamento di un automa'''
        listOfGlobals = globals()
        stato = listOfGlobals['stato']
        automi = listOfGlobals['automi']
        a = carica_automa_da_file_txt()
        if (isinstance(a, Automa)):
            window_crea_rete['informazioni'].update(
                window_crea_rete['informazioni'].get() + "\n" + "Automa letto correttamente:")
            window_crea_rete['informazioni'].update(
                window_crea_rete['informazioni'].get() + "\n" + a.to_string_txt())
            if (controlla_inserimento_automa(automi, a)):
                automi.append(a)
                window_crea_rete['carica_link'].update(disabled=False)
            else:
                window_crea_rete['informazioni'].update(
                    window_crea_rete['informazioni'].get() + "\n" + "Il seguente automa è già stato inserito")

        else:
            window_crea_rete['informazioni'].update(
                window_crea_rete['informazioni'].get() + "\n" + "PROBLEMA LETTURA AUTOMA\n" + a)

        listOfGlobals["automi"]=automi
        aggiorna_elenco_automi()

    def carica_rete():
        '''Metodo per permettere il caricamento delle transizioni'''
        listOfGlobals = globals()
        stato = listOfGlobals['stato']
        automi = listOfGlobals['automi']
        links = listOfGlobals['links']

        a = carica_rete_da_file_txt(automi, links)
        if (isinstance(a, Rete)):
            window_crea_rete['informazioni'].update(
                window_crea_rete['informazioni'].get() + "\n" + "Transizioni lette correttamente:")
            window_crea_rete['informazioni'].update(
                window_crea_rete['informazioni'].get() + "\n" + a.to_string_txt())
            rete = a
            window_crea_rete['salva'].update(disabled=False)
            window_crea_rete['carica_automa'].update(disabled=True)
            window_crea_rete['carica_link'].update(disabled=True)
            window_crea_rete['carica_transizioni'].update(disabled=True)
            window_crea_rete['spazio_comportamentale'].update(disabled=False)

        else:
            window_crea_rete['informazioni'].update(
                window_crea_rete['informazioni'].get() + "\n" + "PROBLEMA LETTURA TRANSIZIONI\n" + a)
            rete = None

        listOfGlobals["automi"]=automi
        listOfGlobals["rete"] = rete
        aggiorna_elenco_automi()
        aggiorna_rete()

    def carica_link():
        '''Metodo per permettere il caricamento dei link'''
        listOfGlobals = globals()
        stato = listOfGlobals['stato']
        links = listOfGlobals['links']
        automi = listOfGlobals['automi']
        out = carica_links_da_file_txt(automi)
        if (isinstance(out, list)):
            window_crea_rete['informazioni'].update(
                window_crea_rete['informazioni'].get() + "\n" + "Link letti correttamente")
            links=out
            window_crea_rete['carica_automa'].update(disabled=True)
            window_crea_rete['carica_link'].update(disabled=True)
            window_crea_rete['carica_transizioni'].update(disabled=False)
        else:
            window_crea_rete['informazioni'].update(
                window_crea_rete['informazioni'].get() + "\n" + "PROBLEMA LETTURA LINKS\n" + out)

        listOfGlobals["automi"]=automi
        listOfGlobals["links"] = links
        aggiorna_elenco_links()
        aggiorna_elenco_automi()

    def salva_su_file():
        '''Salva la rete, gli automi e i links su file
        ogni componente verrà salvato nel seguente modo:
        nome componente (file per salvare la classe)
        nome componente.txt (file contenente il formato utilizzato per importare il componente)
        nome componente_grafico.png (file contenente il grafico del componente)
        nome componente_riassunto.txt (riassunto delle informazioni contenute nel componente)'''
        listOfGlobals = globals()
        cartella = listOfGlobals['cartella']
        cartella_save = listOfGlobals['cartella_save']
        automi = listOfGlobals['automi']
        links = listOfGlobals['links']
        rete = listOfGlobals['rete']

        window_crea_rete['informazioni'].update(
            window_crea_rete['informazioni'].get() + "\n" + "Salvo file nella cartella: "+cartella_save)

        for a in automi:
            stampa_automa_su_file(a, cartella=cartella_save)
        stampa_rete_su_file(rete, cartella=cartella_save)

        window_crea_rete['informazioni'].update(
            window_crea_rete['informazioni'].get() + "\n" + "Creati file PNG dei grafici")

        salva_rete_su_file_txt(rete, cartella_save, rete.nome)
        salva_rete_su_file(rete, cartella_save, rete.nome)
        salva_rete_su_file_txt(rete, cartella_save, rete.nome)
        salva_links_su_file_txt(rete, cartella_save, "links")

        for a in automi:
            salva_automa_su_file(a, cartella_save, a.nome)
            salva_automa_su_file_txt(a, cartella_save, a.nome)

        window_crea_rete['informazioni'].update(
            window_crea_rete['informazioni'].get() + "\n" + "Creati file per la rete, i links e gli automi")


        window_crea_rete['salva'].update(disabled=True)
        window_crea_rete['stampa'].update(disabled=False)
        listOfGlobals['cartella_save'] = cartella_save

    def stampa_grafici():
        '''Metodo per permettere di visualizzare i grafici degli automi, link e transizioni'''
        listOfGlobals = globals()
        automi = listOfGlobals['automi']
        links = listOfGlobals['links']
        rete = listOfGlobals['rete']
        cartella_save = listOfGlobals['cartella_save']

        immagini=[]
        titoli=[]

        for a in automi:
            immagini.append(sg.Image(filename='Output/' + cartella_save + '/' + a.nome + '_grafico.png'))
            titoli.append(sg.Text(a.nome))
        immagine_rete = sg.Image(filename='Output/' + cartella_save + '/' + rete.nome + '_grafico.png')



        grafici_automi = [
            titoli,
            immagini
        ]

        grafici_reti = [
            immagine_rete
        ]

        layout_grafici = [
            [
                sg.Column(grafici_automi)
            ],
            [
                immagine_rete
            ]
        ]

        window_mostra_grafici = sg.Window('Mostra grafici', layout_grafici)

        while True:
            event, values = window_mostra_grafici.read()
            if event == sg.WINDOW_CLOSED:
                break
        window_mostra_grafici.close()

    def carica_rete1():
        '''Metodo per caricare rapidamente la prima rete'''
        listOfGlobals = globals()

        a1 = carica_automa_da_file_txt("Input/RETE1/C2.txt")
        a2 = carica_automa_da_file_txt("Input/RETE1/C3.txt")
        automi = [a1, a2]

        links = carica_links_da_file_txt(automi, "Input/RETE1/links.txt")

        rete = carica_rete_da_file_txt(automi, links, "Input/RETE1/rete 1.txt")

        listOfGlobals['automi'] = automi
        listOfGlobals['links'] = links
        listOfGlobals['rete'] = rete

        aggiorna_elenco_automi()
        aggiorna_elenco_links()
        aggiorna_rete()

        window_crea_rete['conferma_cartella'].update(disabled=True)
        window_crea_rete['input_cartella'].update(disabled=True)
        window_crea_rete['carica_automa'].update(disabled=True)
        window_crea_rete['carica_link'].update(disabled=True)
        window_crea_rete['carica_transizioni'].update(disabled=True)
        window_crea_rete['salva'].update(disabled=False)
        window_crea_rete['stampa'].update(disabled=True)
        window_crea_rete['spazio_comportamentale'].update(disabled=False)

        window_crea_rete['informazioni'].update("Caricata rete 1")

    def carica_rete2():
        '''Metodo per caricare rapidamente la seconda rete'''

        listOfGlobals = globals()

        a1 = carica_automa_da_file_txt("Input/RETE2/B.txt")
        a2 = carica_automa_da_file_txt("Input/RETE2/S.txt")
        automi = [a1, a2]

        links = carica_links_da_file_txt(automi, "Input/RETE2/links.txt")

        rete = carica_rete_da_file_txt(automi, links, "Input/RETE2/rete 2.txt")

        listOfGlobals['automi'] = automi
        listOfGlobals['links'] = links
        listOfGlobals['rete'] = rete

        aggiorna_elenco_automi()
        aggiorna_elenco_links()
        aggiorna_rete()

        window_crea_rete['conferma_cartella'].update(disabled=True)
        window_crea_rete['input_cartella'].update(disabled=True)
        window_crea_rete['carica_automa'].update(disabled=True)
        window_crea_rete['carica_link'].update(disabled=True)
        window_crea_rete['carica_transizioni'].update(disabled=True)
        window_crea_rete['salva'].update(disabled=False)
        window_crea_rete['stampa'].update(disabled=True)
        window_crea_rete['spazio_comportamentale'].update(disabled=False)

        window_crea_rete['informazioni'].update("Caricata rete 2")

    def carica_rete3():
        '''Metodo per caricare rapidamente la terza rete'''

        listOfGlobals = globals()

        a1 = carica_automa_da_file_txt("Input/RETE3/C1.txt")
        a2 = carica_automa_da_file_txt("Input/RETE3/C2.txt")
        a3 = carica_automa_da_file_txt("Input/RETE3/C3.txt")
        automi = [a1, a2, a3]

        links = carica_links_da_file_txt(automi, "Input/RETE3/links.txt")

        rete3 = carica_rete_da_file_txt(automi, links, "Input/RETE3/rete 3.txt")

        listOfGlobals['automi'] = automi
        listOfGlobals['links'] = links
        listOfGlobals['rete'] = rete3

        aggiorna_elenco_automi()
        aggiorna_elenco_links()
        aggiorna_rete()

        window_crea_rete['conferma_cartella'].update(disabled=True)
        window_crea_rete['input_cartella'].update(disabled=True)
        window_crea_rete['carica_automa'].update(disabled=True)
        window_crea_rete['carica_link'].update(disabled=True)
        window_crea_rete['carica_transizioni'].update(disabled=True)
        window_crea_rete['salva'].update(disabled=False)
        window_crea_rete['stampa'].update(disabled=True)
        window_crea_rete['spazio_comportamentale'].update(disabled=False)

        window_crea_rete['informazioni'].update("Caricata rete 3")

    def spazio_comportamentale():
        '''Metodo per aprire la finestra che permetterà di eseguire i vari algoritmi'''

        listOfGlobals = globals()
        automi = listOfGlobals['automi']
        links = listOfGlobals['links']
        rete = listOfGlobals['rete']
        cartella_save = listOfGlobals['cartella_save']
        cartella = listOfGlobals['cartella']
        stato = listOfGlobals['stato']
        print("Tutto: "+cartella+"; "+cartella_save)
        gui_crea_spazio_comportamentale(automi, links, rete, cartella_save, cartella, stato, None, "")


    def reset():
        '''Cancella tutte le informazioni presenti nella finestra e la porta nella situazione iniziale'''

        listOfGlobals = globals()
        listOfGlobals['cartella'] = ""
        listOfGlobals['cartella_save'] = ""
        listOfGlobals['stato'] = "1"
        listOfGlobals['automi'] = []
        listOfGlobals['links'] = []
        listOfGlobals['rete'] = None
        aggiorna_elenco_automi()
        aggiorna_elenco_links()
        aggiorna_rete()
        window_crea_rete['conferma_cartella'].update(disabled=False)
        window_crea_rete['spazio_comportamentale'].update(disabled=True)
        window_crea_rete['input_cartella'].update("", disabled=False)
        window_crea_rete['carica_automa'].update(disabled=True)
        window_crea_rete['carica_link'].update(disabled=True)
        window_crea_rete['carica_transizioni'].update(disabled=True)
        window_crea_rete['salva'].update(disabled=True)
        window_crea_rete['stampa'].update(disabled=True)
        window_crea_rete['informazioni'].update("RESET")



    window_crea_rete = sg.Window('Crea rete', crea_layout_crea_rete())
    while True:
        event, values = window_crea_rete.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "conferma_cartella":
            conferma_cartella()
            print("stato: " + stato)
            print("cartella: "+cartella)
            print("len automi: "+str(len(automi)))
        elif event == "carica_automa":
            carica_automa()
            print("cartella: " + cartella)
            print("len automi: " +str(len(automi)))
        elif event == "carica_link":
            carica_link()
            print("cartella: " + cartella)
            print("len automi: " +str(len(automi)))
        elif event == "reset":
            reset()
            print("cartella: " + cartella)
            print("len automi: " +str(len(automi)))
        elif event == "carica_transizioni":
            carica_rete()
            print("cartella: " + cartella)
            print("len automi: " +str(len(automi)))
        elif event == "salva":
            salva_su_file()
            print("cartella salvataggio: "+cartella_save)
        elif event == "stampa":
            stampa_grafici()
        elif event == "rete1":
            carica_rete1()
        elif event == "rete2":
            carica_rete2()
        elif event == "rete3":
            carica_rete3()
        elif event == "spazio_comportamentale":
            out = spazio_comportamentale()


def gui_crea_spazio_comportamentale(a, l, r, c, c2, s, spazio, nome_S):
    '''Metodo per gestire la finestra che permette di eseguire i 3 algoritmi
    questo metodo viene richiamato in 2 modalità dal programma:
    1)passando tutte le variabile e lasciando a None le ultime 2. Il metodo viene invocato in questo modo quando si ha a disposizione una rete e si vuole generare lo spazio comportamentale da quest'ultima
    2)passando solo lo spaio e lasciando le altre variabili vuote. Il metodo viene invocato in questo modo se si ha importato uno spazio comportamentale e su quest'ultimo si vogliono eseguire gli algoritmi (senza passare prima dalla rete)

    il metodo in base alle variabili di input si comporta in modo diverso, permettendo alcune specifiche operazioni'''

    #variabili globali
    global stato, cartella, automi, links, rete, cartella_save, spazio_comportamentale, nome_spazio, \
        elenco_cartelle, spazio_importato, spazio_comportamentale_potato, \
        osservazione_lineare, spazio_comportamentale_oss, spazio_comportamentale_potato_oss

    stato = s #stato attuale
    cartella = c2 #cartella selezionata per il salvataggio
    cartella_save = c #cartella effettia dove vengono salvati i file (aggiunta di datetime)
    automi = a #automi
    links = l #links
    rete = r #rete
    elenco_cartelle = [] #elenco cartelle utilizzate
    spazio_comportamentale = spazio #spazio comportamentale sul quale si lavora (None)
    spazio_importato = copy.deepcopy(spazio) #spazio importato (inizialmente None)
    nome_spazio = nome_S #nome dello spazio
    spazio_comportamentale_potato = None #spazio comportamentale potato (creato dopo potatura)
    osservazione_lineare = None #osservazione lineare inserita manualmente
    spazio_comportamentale_oss = None #spazio comportamentale generato con algoritmo 2
    spazio_comportamentale_potato_oss = None  # spazio comportamentale potato generato con algoritmo 2


    def crea_layout_spazio_comportamentale():
        colonna1 = [
            [
                sg.Text("Dai un nome alla cartella dove salvare lo spazio comportamentale"),
                sg.Input(key='input_cartella', size=(20, 1)),
                sg.Button('Conferma', key='conferma_cartella')
            ],
            [
                sg.Text("Dai un nome allo spazio comportamentale"),
                sg.Input(key='input_nome_spazio', size=(20, 1), disabled=True),
                sg.Button('Conferma', key='conferma_nome_spazio', disabled=True)
            ],
            [
                sg.HSeparator(),
            ],
            [
                sg.Text("Algoritmo 1", key="algoritmo 1"),
            ],
            [

                sg.Button("Crea spazio comportamentale", key="avvio_algoritmo1", disabled=True),
                sg.Button("Crea spazio comportamentale (passaggi)", key="avvio_algoritmo1_manuale", disabled=True),
                sg.Button("avvio 3", key="avvio3", disabled=True)
            ],
            [
                sg.Button("Salva informazioni spazio su file", key="salva", disabled=True),
                sg.Button("Mostra grafico spazio compotamentale", key="stampa", disabled=True)
            ],
            [
                sg.Button("Potatura dello spazio comportamentale", key="potatura", disabled=True),
                sg.Button("Mostra grafico spazio potato", key="stampa_potatura", disabled=True)
            ],
            [
                sg.Button("Reset", key="reset", disabled=True),
            ],
            [
                sg.HSeparator(),
            ],
            [
                sg.Text("Algoritmo 2", key="algoritmo2"),
            ],
            [

                sg.Text("Inserisci un osservazione lineare"),
                sg.Input(key='input_osservazione_lineare', size=(20, 1), disabled=True),
                sg.Button('Conferma', key='conferma_osservazione_lineare', disabled=True)

            ],
            [
                sg.Text("Creazione di uno spazio comportamentale relativo ad un'osservazione lineare, partendo da una rete"),

            ],
            [
                sg.Button("Crea spazio comportamentale relativo all'osservazione", key="avvio_algoritmo2",
                          disabled=True),
                sg.Button("Crea spazio comportamentale relativo all'osservazione (passaggi)",
                          key="avvio_algoritmo2_manuale", disabled=True),
                sg.Button("avvio 3", key="avvio3", disabled=True)
            ],
            [
                sg.Button("Salva informazioni spazio su file", key="salva_spazio2", disabled=True),
                sg.Button("Mostra grafico spazio compotamentale", key="stampa_spazio2", disabled=True)
            ],
            [
                sg.Button("Potatura dello spazio comportamentale", key="potatura_spazio2", disabled=True),
                sg.Button("Mostra grafico spazio potato", key="stampa_potatura_spazio2", disabled=True)
            ],
            [
                sg.Button("Reset", key="reset_algoritmo2", disabled=True),
            ],
            [
                sg.HSeparator(),
            ],

        ]

        colonna2 = [
            [
                sg.Text("Informazioni"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 20), key="informazioni", autoscroll=True
                )
            ],
        ]

        layout_spazio_comportamentale = [
            [
                sg.Column(colonna1),
                sg.VSeperator(),
                sg.Column(colonna2),
            ]
        ]

        return layout_spazio_comportamentale

#Metodi per abilitare o disabilitare sezioni della GUI
    def abilita_algoritmo2(bool):
        '''abilita o disabilita tutta la sezione dell'algoritmo 2'''
        if bool==False:
            window_spazio_comportamentale['algoritmo2'].update('Algoritmo 2 - Abilitato')
            window_spazio_comportamentale['informazioni'].update(
                window_spazio_comportamentale[
                    'informazioni'].get() + "\nL'algoritmo 2 è disabilitato, inserire una rete o uno spazio comportamentale")
        else:
            listOfGlobals = globals()
            rete = listOfGlobals['rete']
            if rete==None:
                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale[
                        'informazioni'].get() + "\nL'algoritmo 2 è abilitato - Verra svolto sullo spazio importato")
            else:
                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale[
                        'informazioni'].get() + "\nL'algoritmo 2 è abilitato - Verra svolto sulla rete importata")
        bool = not bool
        window_spazio_comportamentale['input_osservazione_lineare'].update('', disabled=bool)
        window_spazio_comportamentale['conferma_osservazione_lineare'].update(disabled=bool)
        window_spazio_comportamentale['avvio_algoritmo2'].update(disabled=bool)
        window_spazio_comportamentale['avvio_algoritmo2_manuale'].update(disabled=bool)
        window_spazio_comportamentale['avvio3'].update(disabled=bool)
        window_spazio_comportamentale['reset_algoritmo2'].update(disabled=bool)
        window_spazio_comportamentale['salva_spazio2'].update(disabled=bool)
        window_spazio_comportamentale['stampa_spazio2'].update(disabled=bool)
        window_spazio_comportamentale['potatura_spazio2'].update(disabled=bool)
        window_spazio_comportamentale['stampa_potatura_spazio2'].update(disabled=bool)

    def abilita_algoritmo1(bool):
        '''abilita o disabilita tutta la sezione dell'algoritmo 2'''
        if bool == False:
            window_spazio_comportamentale['informazioni'].update(
                window_spazio_comportamentale[
                    'informazioni'].get() + "\nL'algoritmo 1 è disabilitato, inserire una rete o uno spazio comportamentale")
        else:
            listOfGlobals = globals()
            rete = listOfGlobals['rete']
            if rete == None:
                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale[
                        'informazioni'].get() + "\nL'algoritmo 1 è abilitato - Verra svolto sullo spazio importato")
            else:
                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale[
                        'informazioni'].get() + "\nL'algoritmo 1 è abilitato - Verra svolto sulla rete importata")
        bool = not bool
        window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=bool)
        window_spazio_comportamentale['avvio_algoritmo1_manuale'].update(disabled=bool)
        window_spazio_comportamentale['salva'].update(disabled=bool)
        window_spazio_comportamentale['stampa'].update(disabled=bool)
        window_spazio_comportamentale['stampa_potatura'].update(disabled=bool)
        window_spazio_comportamentale['potatura'].update(disabled=bool)

    def abilita_algoritmo1_spazio():
        window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=True)
        window_spazio_comportamentale['avvio_algoritmo1_manuale'].update(disabled=True)
        window_spazio_comportamentale['salva'].update(disabled=False)
        window_spazio_comportamentale['potatura'].update(disabled=False)
        window_spazio_comportamentale['reset'].update(disabled=False)
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\nL'algoritmo 1 è abilitato, verrà avviato sullo spazio comportamentale inserito")

    def abilita_algoritmo1_rete():
        window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=False)
        window_spazio_comportamentale['avvio_algoritmo1_manuale'].update(disabled=False)
        window_spazio_comportamentale['salva'].update(disabled=True)
        window_spazio_comportamentale['potatura'].update(disabled=True)
        window_spazio_comportamentale['reset'].update(disabled=False)
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\nL'algoritmo 1 è abilitato, verrà avviato sulla rete inserita")

    def abilita_algoritmo1_creato_spazio():
        window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=True)
        window_spazio_comportamentale['avvio_algoritmo1_manuale'].update(disabled=True)
        window_spazio_comportamentale['salva'].update(disabled=False)
        window_spazio_comportamentale['potatura'].update(disabled=False)
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\nL'algoritmo 1 è stato avviato, sono ora disponibili le funzioni di salvataggio e potatura")

    def abilita_algoritmo2_creato_spazio():
        window_spazio_comportamentale['input_osservazione_lineare'].update('', disabled=True)
        window_spazio_comportamentale['conferma_osservazione_lineare'].update(disabled=True)
        window_spazio_comportamentale['avvio_algoritmo2'].update(disabled=True)
        window_spazio_comportamentale['avvio_algoritmo2_manuale'].update(disabled=True)
        window_spazio_comportamentale['salva_spazio2'].update(disabled=False)
        window_spazio_comportamentale['stampa_spazio2'].update(disabled=True)
        window_spazio_comportamentale['potatura_spazio2'].update(disabled=False)
        window_spazio_comportamentale['stampa_potatura_spazio2'].update(disabled=True)
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\nL'algoritmo 1 è stato avviato, sono ora disponibili le funzioni di salvataggio e potatura")

    def abilita_algoritmo2_salva():
        window_spazio_comportamentale['salva_spazio2'].update(disabled=True)
        window_spazio_comportamentale['stampa_spazio2'].update(disabled=False)

    def abilita_algoritmo2_potatura():
        window_spazio_comportamentale['potatura_spazio2'].update(disabled=True)
        window_spazio_comportamentale['stampa_potatura_spazio2'].update(disabled=False)

    def abilita_algoritmo2_spazio():
        window_spazio_comportamentale['input_osservazione_lineare'].update(disabled=False)
        window_spazio_comportamentale['conferma_osservazione_lineare'].update(disabled=False)
        window_spazio_comportamentale['avvio_algoritmo2'].update(disabled=True)
        window_spazio_comportamentale['avvio_algoritmo2_manuale'].update(disabled=True)
        window_spazio_comportamentale['avvio3'].update(disabled=True)
        window_spazio_comportamentale['reset_algoritmo2'].update(disabled=False)
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\nL'algoritmo 2 è abilitato, verrà avviato sullo spazio comportamentale inserito")

    def abilita_algoritmo2_rete():
        window_spazio_comportamentale['input_osservazione_lineare'].update(disabled=False)
        window_spazio_comportamentale['conferma_osservazione_lineare'].update(disabled=False)
        window_spazio_comportamentale['avvio_algoritmo2'].update(disabled=True)
        window_spazio_comportamentale['avvio_algoritmo2_manuale'].update(disabled=True)
        window_spazio_comportamentale['avvio3'].update(disabled=True)
        window_spazio_comportamentale['reset_algoritmo2'].update(disabled=False)
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\nL'algoritmo 2 è abilitato, verrà avviato sulla rete inserita")

    def abilita_algoritmo2_inserita_osservazione():
        listOfGlobals = globals()
        rete = listOfGlobals["rete"]
        window_spazio_comportamentale['input_osservazione_lineare'].update(disabled=False)
        window_spazio_comportamentale['conferma_osservazione_lineare'].update(disabled=False)
        window_spazio_comportamentale['avvio_algoritmo2'].update(disabled=False)
        window_spazio_comportamentale['avvio_algoritmo2_manuale'].update(disabled=False)
        window_spazio_comportamentale['avvio3'].update(disabled=False)
        window_spazio_comportamentale['reset_algoritmo2'].update(disabled=False)
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\nL'algoritmo 2 è pronto per essere eseguito: osservazione lineare inserita correttamente")
        if rete == None:
            window_spazio_comportamentale['informazioni'].update(
                window_spazio_comportamentale[
                    'informazioni'].get() + "\nL'algoritmo 2 verrà eseguito sullo spazio comportamentale inserito")
        else:
            window_spazio_comportamentale['informazioni'].update(
                window_spazio_comportamentale[
                    'informazioni'].get() + "\nL'algoritmo 2 verrà eseguito sulla rete inserita")



#METODI

    def conferma_cartella():
        '''Permette di selezionare la cartella di salvataggio

        in caso questa sia già stata selezionata in precedenza si utilizzerà:
        cartella già selezionata/nome cartella specificato/algoritmo*/vari file

        Se invece non è stata selezinata in precedenza alcuna cartella (in caso in cui si giunga a questa finestra importando direttamente uno spazio comportamentale)
        i file verranno salvati nella seguente cartella:
        data attuale / nome cartella / algoritmo* / vari file

        il metodo gestisce anche la possibilità di compire molteplici operazioni sulla stessa rete/spazio
        in questo caso i file verranno salvati sfruttando variando il nome della cartalla
        cartella già selezionata / nome cartalla 1 / ecc
        cartella già selezionata / nome cartalla 2 / ecc
        '''
        listOfGlobals = globals()
        cartella_save = listOfGlobals['cartella_save']
        elenco_cartelle = listOfGlobals['elenco_cartelle']

        if values['input_cartella']!="":
            if len(elenco_cartelle)!=0 and values['input_cartella'] in elenco_cartelle:
                sg.Popup('Attenzione!',
                         'Cartella già usata')
            else:
                if cartella_save!="":
                    elenco = cartella_save.split("/")
                    print("Cartella save: "+cartella_save)
                    print("ultimo elemento: "+elenco[len(elenco)-1])
                    if elenco[len(elenco)-1] in elenco_cartelle:
                        nuova=""
                        for e in elenco[:-1]:
                            nuova += e
                        print("nuova: "+nuova)
                        cartella_save = nuova
                    cartella_save = cartella_save+"/"+values['input_cartella']
                    elenco_cartelle.append(values['input_cartella'])
                else:
                    x = datetime.datetime.now()
                    data_attuale = str(x.strftime("%Y_%m_%d_%H_%M_%S"))
                    cartella_save = data_attuale
                    elenco_cartelle.append(values['input_cartella'])
                    cartella_save = cartella_save + "/" + values['input_cartella']

                if listOfGlobals['spazio_importato']==None:
                    window_spazio_comportamentale['conferma_cartella'].update(disabled=True)
                    window_spazio_comportamentale['input_cartella'].update(disabled=True)
                    window_spazio_comportamentale['conferma_nome_spazio'].update(disabled=False)
                    window_spazio_comportamentale['input_nome_spazio'].update(disabled=False)
                    window_spazio_comportamentale['reset'].update(disabled=False)
                    window_spazio_comportamentale['informazioni'].update(
                        window_spazio_comportamentale['informazioni'].get() + "\nCartella selezionata: " + cartella_save)
                    listOfGlobals['cartella_save'] = cartella_save
                    listOfGlobals['elenco_cartelle'] = elenco_cartelle
                else:

                    window_spazio_comportamentale['conferma_cartella'].update(disabled=True)
                    window_spazio_comportamentale['input_cartella'].update(disabled=True)
                    window_spazio_comportamentale['conferma_nome_spazio'].update(disabled=True)
                    window_spazio_comportamentale['input_nome_spazio'].update(disabled=True)
                    window_spazio_comportamentale['informazioni'].update(
                        window_spazio_comportamentale[
                            'informazioni'].get() + "\nCartella selezionata: " + cartella_save)

                    abilita_algoritmo1_spazio()
                    abilita_algoritmo2_spazio()

                    listOfGlobals['cartella_save'] = cartella_save
                    listOfGlobals['elenco_cartelle'] = elenco_cartelle
                    importato = listOfGlobals['spazio_importato']
                    listOfGlobals['spazio_comportamentale'] = copy.deepcopy(importato)
                    window_spazio_comportamentale['informazioni'].update(
                        window_spazio_comportamentale[
                            'informazioni'].get() + "\nSpazio già presente, con nome: " + spazio.nome)

        else:
            sg.Popup('Attenzione!',
                     'Inserire un nome non vuoto')

    def conferma_nome_spazio():
        '''Permette di selezionare il nome da attribuire allo spazio comportamentale
        il metodo non potrà essere attivato nel caso si giunga a questa finestra importando uno spazio'''
        listOfGlobals = globals()
        nome_spazio = listOfGlobals['nome_spazio']

        if values['input_nome_spazio'] != "":
            if nome_spazio!="" and nome_spazio==values['input_nome_spazio']:
                sg.Popup('Attenzione!',
                         'Hai già usato questo nome')
            else:
                nome_spazio = values['input_nome_spazio']
                window_spazio_comportamentale['conferma_cartella'].update(disabled=True)
                window_spazio_comportamentale['input_cartella'].update(disabled=True)
                window_spazio_comportamentale['conferma_nome_spazio'].update(disabled=True)
                window_spazio_comportamentale['input_nome_spazio'].update(disabled=True)
                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale['informazioni'].get() + "\nNome spazio impostato: " + nome_spazio)

                abilita_algoritmo1_rete()
                abilita_algoritmo2_rete()
                listOfGlobals['nome_spazio'] = nome_spazio
        else:
            sg.Popup('Attenzione!',
                     'Inserire un nome non vuoto')

    def conferma_osservazione_lineare():
        '''Permette di impostare un'osservazione lineare. Sfruttando la seguente espressione regolare:
        ^[a-zA-Z0-9]+(,([a-zA-Z0-9]+,)*[a-zA-Z0-9]+)?

        l'osservazione lineare sarà quindi del tipo: o2,o3,o4'''
        REGEX_OSSERVAZIONE = "^[a-zA-Z0-9]+(,([a-zA-Z0-9]+,)*[a-zA-Z0-9]+)?"
        listOfGlobals = globals()
        osservazione_lineare = listOfGlobals['osservazione_lineare']

        if values['input_osservazione_lineare'] != "":

            stringa_regex = values['input_osservazione_lineare']
            x = re.fullmatch(REGEX_OSSERVAZIONE, stringa_regex)
            if x:
                osservazione_lineare = values['input_osservazione_lineare']
                osservazione_lineare = stringa_regex.split(",")
                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale[
                        'informazioni'].get() + "\nOsservazione lineare letta correttamente: "+str(osservazione_lineare))
                abilita_algoritmo2_inserita_osservazione()
                listOfGlobals['osservazione_lineare'] = osservazione_lineare
            else:
                sg.Popup('Attenzione!',
                         'formato della stringa sbagliato. Inserire un\'osservazione tipo \"o2,o3,o4\"')
        else:
            sg.Popup('Attenzione!',
                     'Inserire un nome non vuoto')

    def reset():
        '''Imposta la rete allo stato iniziale'''
        window_spazio_comportamentale['conferma_cartella'].update(disabled=False)
        window_spazio_comportamentale['input_cartella'].update("", disabled=False)
        window_spazio_comportamentale['conferma_nome_spazio'].update(disabled=True)
        window_spazio_comportamentale['input_nome_spazio'].update("", disabled=True)
        window_spazio_comportamentale['informazioni'].update("RESET")
        abilita_algoritmo1(False)
        abilita_algoritmo2(False)
        listOfGlobals = globals()
        listOfGlobals['spazio_comportamentale']=None

    def algoritmo_crea_spazio_comportamentale():
        '''Invoca lalgoritmo per creare lo spazio comportamentale data una rete
        lo spazio è automaticamente ridenominato sfruttando degli id univoci'''
        listOfGlobals = globals()
        rete = listOfGlobals['rete']
        spazio_comportamentale = listOfGlobals['spazio_comportamentale']
        nome_spazio = listOfGlobals['nome_spazio']

        spazio_comportamentale = crea_spazio_comportamentale(rete)
        spazio_comportamentale.nome=nome_spazio


        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale['informazioni'].get() + "\nCreato lo spazio comportamentale: \n" + spazio_comportamentale.riassunto())
        listOfGlobals['spazio_comportamentale'] = spazio_comportamentale

        abilita_algoritmo1_creato_spazio()

    def algoritmo_crea_spazio_comportamentale2():
        '''Invoca l'algoritmo per creare uno spazio comportamentale data un'osservazione lineare'''
        listOfGlobals = globals()
        if listOfGlobals['spazio_importato'] == None:
            print("LAVORO SU RETE")
            rete = listOfGlobals['rete']
            if rete != None:
                spazio_comportamentale_oss = listOfGlobals['spazio_comportamentale_oss']
                osservazione_lineare = listOfGlobals['osservazione_lineare']
                nome_spazio = listOfGlobals['nome_spazio']
                print("OSS: "+str(osservazione_lineare))

                if osservazione_lineare==None or (rete.controlla_osservazione(osservazione_lineare)):
                    spazio_comportamentale_oss = crea_spazio_comportamentale2(rete, osservazione_lineare)
                    spazio_comportamentale_oss.nome = nome_spazio

                    window_spazio_comportamentale['informazioni'].update(
                        window_spazio_comportamentale[
                            'informazioni'].get() + "\nCreato lo spazio comportamentale: \n" + spazio_comportamentale_oss.riassunto() + "\npartendo dall\'osservazione lineare: " + str(
                            osservazione_lineare))
                    listOfGlobals['spazio_comportamentale_oss'] = spazio_comportamentale_oss

                    abilita_algoritmo2_creato_spazio()
                else:
                    sg.Popup('Attenzione!',
                             'Le etichette dell\'osservazione lineare inserita non sono presenti nella rete. Cambiare l\'osservazione lineare per proseguire')
        else:
            print("LAVORO SU SPAZIO")
            spazio = listOfGlobals['spazio_importato']
            spazio_comportamentale_oss = listOfGlobals['spazio_comportamentale_oss']
            osservazione_lineare = listOfGlobals['osservazione_lineare']
            nome_spazio = listOfGlobals['nome_spazio']
            print("OSS: " + str(osservazione_lineare))

            if (osservazione_lineare != None):
                spazio_comportamentale_oss = crea_spazio_comportamentale2_da_spazio(spazio, osservazione_lineare)
                spazio_comportamentale_oss.nome = nome_spazio

                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale[
                        'informazioni'].get() + "\nCreato lo spazio comportamentale: \n" + spazio_comportamentale_oss.riassunto() + "\npartendo dall\'osservazione lineare: " + str(
                        osservazione_lineare))
                listOfGlobals['spazio_comportamentale_oss'] = spazio_comportamentale_oss

                abilita_algoritmo2_creato_spazio()
            else:
                sg.Popup('Attenzione!',
                         'Le etichette dell\'osservazione lineare inserita non sono presenti nella rete. Cambiare l\'osservazione lineare per proseguire')


    def algoritmo_crea_spazio_comportamentale_manuale(nome):
        '''Permette di creare uno spazio comportamentale data una rete svolgendo manualmente tutti i vari passaggi
        l'algoritmo non termina fino a che l'utente non chiude la nuova finestra'''
        listOfGlobals = globals()

        rete = listOfGlobals['rete']
        spazio_comportamentale = listOfGlobals['spazio_comportamentale']
        cartella_save = listOfGlobals['cartella_save']
        nome_spazio = listOfGlobals['nome_spazio']
        spazio_comportamentale = Spazio_comportamentale("")


        #prima iterazione creo spazio
        nodi_a, nodo_attuale_a, transizioni_a, fine_a, commento = crea_spazio_comportamentale_manuale(rete)
        print("Nodo attuale: "+nodo_attuale_a.to_string())
        nodi_finali_a = []
        nodi_iniziali_a = []
        for n in nodi_a:
            if n.finale:
                nodi_finali_a.append(n)
            if n.iniziale:
                nodi_iniziali_a.append(n)
        print("lunghezza nodi finali: "+str(len(nodi_finali_a)))
        print("lunghezza nodi iniziali: " + str(len(nodi_iniziali_a)))
        spazio = Spazio_comportamentale(nome_spazio, nodi_finali_a, nodi_iniziali_a, nodi_a, transizioni_a)
        sistema_transizioni(spazio)
        ridenominazione_spazio_appena_creato(spazio)
        listOfGlobals['spazio_comportamentale'] = spazio
        stampa_spazio_su_file(spazio, cartella_save + nome +"/iterazione1")
        i=2

        colonna1 = [
            [
                sg.Button('Passaggio successivo', key='passaggio_successivo', disabled=False),
                sg.Button('Concludi', key='concludi', disabled=False),
            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 20), key="informazioni_algoritmo", autoscroll=True
                )
            ],
        ]

        colonna2 = [
            [
                sg.Image('Output/' + cartella_save+ nome +'/iterazione1/' + spazio.nome + '_grafico.png', key="immagine", size=(1000, 2000))
            ]
        ]

        layout_grafici = [
            [
                sg.Column(colonna1),
                sg.VSeperator(),
                sg.Column(colonna2, scrollable=True),
            ]
        ]

        window_crea_spazio_comportamentale_manuale = sg.Window('Creazione manuale spazio comportamentale', layout_grafici, location=(0, 0),
                                          size=(800, 600), keep_on_top=True)

        #window_crea_spazio_comportamentale_manuale['informazioni_algoritmo'].update(window_crea_spazio_comportamentale_manuale['informazioni_algoritmo'].get()+"\niniziato analizzando stato inziiale\n"+commento)

        while True:
            event, values = window_crea_spazio_comportamentale_manuale.read()
            if event == sg.WINDOW_CLOSED or event == "concludi":
                abilita_algoritmo1_creato_spazio()
                if fine_a==False:
                    window_spazio_comportamentale['informazioni'].update(
                        window_spazio_comportamentale[
                            'informazioni'].get() + "\nConcludo l'esecuzione senza aver generato tutto lo spazio comportamentale \n")

                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale['informazioni'].get() + "\nCreato lo spazio comportamentale: \n" + spazio.riassunto())
                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale[
                        'informazioni'].get() + "\nLo spazio è stato ridenominato e salvato su file correttamente")
                break
            elif event == "passaggio_successivo":
                nodi_a, nodo_attuale_a, transizioni_a, fine_a, commento = crea_spazio_comportamentale_manuale(rete, nodi_a, nodo_attuale_a,
                                                                                            transizioni_a)
                window_crea_spazio_comportamentale_manuale['informazioni_algoritmo'].update(
                    window_crea_spazio_comportamentale_manuale[
                        'informazioni_algoritmo'].get() + "\n" + commento)

                nodi_finali_a = []
                nodi_iniziali_a = []
                for n in nodi_a:
                    if n.finale:
                        nodi_finali_a.append(n)
                    if n.iniziale:
                        nodi_iniziali_a.append(n)
                spazio = Spazio_comportamentale(nome_spazio, nodi_finali_a, nodi_iniziali_a, nodi_a, transizioni_a)
                #stampa_spazio_su_file(spazio, cartella_save + nome)
                sistema_transizioni(spazio)
                ridenominazione_spazio_appena_creato(spazio)
                listOfGlobals['spazio_comportamentale'] = spazio
                stampa_spazio_su_file(spazio, cartella_save +nome + "/iterazione"+str(i))
                window_crea_spazio_comportamentale_manuale["immagine"].update('Output/' + cartella_save +nome +'/iterazione'+str(i)+"/" + spazio.nome + '_grafico.png')
                i = i+1

        window_crea_spazio_comportamentale_manuale.close()



        # window_spazio_comportamentale['informazioni'].update(
        #     window_spazio_comportamentale['informazioni'].get() + "\nCreato lo spazio comportamentale: \n" + spazio_comportamentale.to_string())
        # listOfGlobals['spazio_comportamentale'] = spazio_comportamentale
        # window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=True)
        # window_spazio_comportamentale['salva'].update(disabled=False)
        # window_spazio_comportamentale['potatura'].update(disabled=False)

    def algoritmo_crea_spazio_comportamentale_manuale2(nome):
        '''Permette di creare uno spazio comportamentale data un'osservazione lineare svolgendo manualmente tutti i vari passaggi
                l'algoritmo non termina fino a che l'utente non chiude la nuova finestra'''
        listOfGlobals = globals()

        rete = listOfGlobals['rete']
        spazio_comportamentale_oss = listOfGlobals['spazio_comportamentale_oss']
        osservazione_lineare = listOfGlobals['osservazione_lineare']
        cartella_save = listOfGlobals['cartella_save']
        nome_spazio = listOfGlobals['nome_spazio']
        spazio_comportamentale_oss = Spazio_comportamentale("")


        #prima iterazione creo spazio
        nodi_a, nodo_attuale_a, transizioni_a, fine_a, commento = crea_spazio_comportamentale_manuale2(rete, osservazione_lineare)
        print("Nodo attuale: "+nodo_attuale_a.to_string())
        nodi_finali_a = []
        nodi_iniziali_a = []
        for n in nodi_a:
            if n.finale:
                nodi_finali_a.append(n)
            if n.iniziale:
                nodi_iniziali_a.append(n)
        print("lunghezza nodi finali: "+str(len(nodi_finali_a)))
        print("lunghezza nodi iniziali: " + str(len(nodi_iniziali_a)))
        spazio = Spazio_comportamentale(nome_spazio, nodi_finali_a, nodi_iniziali_a, nodi_a, transizioni_a)
        sistema_transizioni(spazio)
        ridenominazione_spazio_appena_creato(spazio)
        listOfGlobals['spazio_comportamentale'] = spazio
        stampa_spazio_su_file(spazio, cartella_save + nome +"/iterazione1")
        i=2

        colonna1 = [
            [
                sg.Button('Passaggio successivo', key='passaggio_successivo', disabled=False),
                sg.Button('Concludi', key='concludi', disabled=False),
            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 20), key="informazioni_algoritmo", autoscroll=True
                )
            ],
        ]

        colonna2 = [
            [
                sg.Image('Output/' + cartella_save+ nome +'/iterazione1/' + spazio.nome + '_grafico.png', key="immagine", size=(1000, 2000))
            ]
        ]

        layout_grafici = [
            [
                sg.Column(colonna1),
                sg.VSeperator(),
                sg.Column(colonna2, scrollable=True),
            ]
        ]

        window_crea_spazio_comportamentale_manuale = sg.Window('Creazione manuale spazio comportamentale', layout_grafici, location=(0, 0),
                                          size=(800, 600), keep_on_top=True)

        #window_crea_spazio_comportamentale_manuale['informazioni_algoritmo'].update(window_crea_spazio_comportamentale_manuale['informazioni_algoritmo'].get()+"\niniziato analizzando stato inziiale\n"+commento)

        while True:
            event, values = window_crea_spazio_comportamentale_manuale.read()
            if event == sg.WINDOW_CLOSED or event == "concludi":
                abilita_algoritmo2_creato_spazio()
                if fine_a==False:
                    window_spazio_comportamentale['informazioni'].update(
                        window_spazio_comportamentale[
                            'informazioni'].get() + "\nConcludo l'esecuzione senza aver generato tutto lo spazio comportamentale \n")

                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale['informazioni'].get() + "\nCreato lo spazio comportamentale: \n" + spazio.riassunto())
                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale[
                        'informazioni'].get() + "\nLo spazio è stato ridenominato e salvato su file correttamente")
                break
            elif event == "passaggio_successivo":
                nodi_a, nodo_attuale_a, transizioni_a, fine_a, commento = crea_spazio_comportamentale_manuale2(rete, osservazione_lineare, nodi_a, nodo_attuale_a,
                                                                                            transizioni_a)
                window_crea_spazio_comportamentale_manuale['informazioni_algoritmo'].update(
                    window_crea_spazio_comportamentale_manuale[
                        'informazioni_algoritmo'].get() + "\n" + commento)

                nodi_finali_a = []
                nodi_iniziali_a = []
                for n in nodi_a:
                    if n.finale:
                        nodi_finali_a.append(n)
                    if n.iniziale:
                        nodi_iniziali_a.append(n)
                spazio = Spazio_comportamentale(nome_spazio, nodi_finali_a, nodi_iniziali_a, nodi_a, transizioni_a)
                #stampa_spazio_su_file(spazio, cartella_save + nome)
                sistema_transizioni(spazio)
                ridenominazione_spazio_appena_creato(spazio)
                listOfGlobals['spazio_comportamentale_oss'] = spazio
                stampa_spazio_su_file(spazio, cartella_save +nome + "/iterazione"+str(i))
                window_crea_spazio_comportamentale_manuale["immagine"].update('Output/' + cartella_save +nome +'/iterazione'+str(i)+"/" + spazio.nome + '_grafico.png')
                i = i+1

        window_crea_spazio_comportamentale_manuale.close()



        # window_spazio_comportamentale['informazioni'].update(
        #     window_spazio_comportamentale['informazioni'].get() + "\nCreato lo spazio comportamentale: \n" + spazio_comportamentale.to_string())
        # listOfGlobals['spazio_comportamentale'] = spazio_comportamentale
        # window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=True)
        # window_spazio_comportamentale['salva'].update(disabled=False)
        # window_spazio_comportamentale['potatura'].update(disabled=False)


    def salva_su_file(nome):
        '''Salva lo spazio comportamentale creato su file
        nome spazio_grafico.png
        nome spazio_riassunto.txt
        nome spazio_salvataggio
        nome spazio_ridenominazione_grafico.png'''
        listOfGlobals = globals()
        cartella_save = listOfGlobals['cartella_save']
        spazio_comportamentale = listOfGlobals['spazio_comportamentale']

        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale['informazioni'].get() + "\n" + "Salvo file nella cartella: " + cartella_save)

        stampa_spazio_su_file(spazio_comportamentale, cartella_save+nome)
        stampa_spazio_ridenominato_su_file(spazio_comportamentale, cartella_save + nome)


        # salvo spazio potato su file
        spazio_salvataggio = crea_spazio_da_spazio(spazio_comportamentale)
        spazio_salvataggio.spazio_potato = False
        salva_spazio_su_file(spazio_salvataggio, cartella_save + nome)


        window_spazio_comportamentale['salva'].update(disabled=True)
        window_spazio_comportamentale['stampa'].update(disabled=False)

    def salva_su_file2(nome):
        '''Salva lo spazio comportamentale creato su file
        nome spazio_grafico.png
        nome spazio_riassunto.txt
        nome spazio_salvataggio
        nome spazio_ridenominazione_grafico.png'''
        listOfGlobals = globals()
        cartella_save = listOfGlobals['cartella_save']
        spazio_comportamentale_oss = listOfGlobals['spazio_comportamentale_oss']

        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale['informazioni'].get() + "\n" + "Salvo file nella cartella: " + cartella_save)

        stampa_spazio_su_file(spazio_comportamentale_oss, cartella_save+nome, "_oss")
        stampa_spazio_ridenominato_su_file(spazio_comportamentale_oss, cartella_save + nome, "_oss")

        #salva spazio su file
        spazio_salvataggio = crea_spazio_da_spazio(spazio_comportamentale_oss)
        spazio_salvataggio.spazio_potato = False
        salva_spazio_su_file(spazio_salvataggio, cartella_save + nome, "_oss")

        abilita_algoritmo2_salva()



    def stampa_grafici(nome):
        listOfGlobals = globals()
        spazio_comportamentale = listOfGlobals['spazio_comportamentale']
        cartella_save = listOfGlobals['cartella_save']

        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale['informazioni'].get() + "\n" + "Leggo file PNG: " + 'Output/' + cartella_save +nome + spazio_comportamentale.nome + '_grafico.png')

        colonna1 = [
            [
                sg.Text("Grafico spazio comportamentale"),
                sg.Image(filename='Output/' + cartella_save + nome + '/' + spazio_comportamentale.nome + '_grafico.png')
            ]
        ]

        layout_grafici = [
            [
                sg.Column(colonna1, scrollable=True),
                sg.VSeperator()
            ]
        ]

        window_mostra_grafici = sg.Window('Mostra grafico spazio comportamentale', layout_grafici, location=(0,0), size=(800,600), keep_on_top=True)

        while True:
            event, values = window_mostra_grafici.read()
            if event == sg.WINDOW_CLOSED:
                break
        window_mostra_grafici.close()

    def stampa_grafici2(nome):
        listOfGlobals = globals()
        spazio_comportamentale_oss = listOfGlobals['spazio_comportamentale_oss']
        cartella_save = listOfGlobals['cartella_save']

        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale['informazioni'].get() + "\n" + "Leggo file PNG: " + 'Output/' + cartella_save +nome + spazio_comportamentale_oss.nome + '_grafico_oss.png')

        colonna1 = [
            [
                sg.Text("Grafico spazio comportamentale"),
                sg.Image(filename='Output/' + cartella_save + nome + '/' + spazio_comportamentale_oss.nome + '_grafico_oss.png')
            ]
        ]

        layout_grafici = [
            [
                sg.Column(colonna1, scrollable=True),
                sg.VSeperator()
            ]
        ]

        window_mostra_grafici = sg.Window('Mostra grafico spazio comportamentale', layout_grafici, location=(0,0), size=(800,600), keep_on_top=True)

        while True:
            event, values = window_mostra_grafici.read()
            if event == sg.WINDOW_CLOSED:
                break
        window_mostra_grafici.close()

    def stampa_grafici_potatura(nome):
        listOfGlobals = globals()
        spazio_comportamentale_potato = listOfGlobals['spazio_comportamentale_potato']
        cartella_save = listOfGlobals['cartella_save']

        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale['informazioni'].get() + "\n" + "Leggo file PNG: " + 'Output/' + cartella_save + nome + spazio_comportamentale_potato.nome + '_potatura_grafico.png')

        colonna1 = [
            [
                sg.Text("Grafico spazio comportamentale potato"),
                sg.Image(filename='Output/' + cartella_save + nome + spazio_comportamentale_potato.nome + '_potatura_grafico.png')
            ]
        ]

        layout_grafici = [
            [
                sg.Column(colonna1, scrollable=True),
                sg.VSeperator()
            ]
        ]

        window_mostra_grafici = sg.Window('Mostra grafico spazio comportamentale', layout_grafici, location=(0,0), size=(800,600), keep_on_top=True)

        while True:
            event, values = window_mostra_grafici.read()
            if event == sg.WINDOW_CLOSED:
                break
        window_mostra_grafici.close()

    def stampa_grafici_potatura2(nome):
        listOfGlobals = globals()
        spazio_comportamentale_potato_oss = listOfGlobals['spazio_comportamentale_potato_oss']
        cartella_save = listOfGlobals['cartella_save']

        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale['informazioni'].get() + "\n" + "Leggo file PNG: " + 'Output/' + cartella_save + nome + spazio_comportamentale_potato_oss.nome + '_potatura_grafico_oss.png')

        colonna1 = [
            [
                sg.Text("Grafico spazio comportamentale potato"),
                sg.Image(filename='Output/' + cartella_save + nome + spazio_comportamentale_potato_oss.nome + '_potatura_grafico_oss.png')
            ]
        ]

        layout_grafici = [
            [
                sg.Column(colonna1, scrollable=True),
                sg.VSeperator()
            ]
        ]

        window_mostra_grafici = sg.Window('Mostra grafico spazio comportamentale', layout_grafici, location=(0,0), size=(800,600), keep_on_top=True)

        while True:
            event, values = window_mostra_grafici.read()
            if event == sg.WINDOW_CLOSED:
                break
        window_mostra_grafici.close()

    def potatura(nome):
        listOfGlobals = globals()
        spazio_comportamentale = listOfGlobals['spazio_comportamentale']
        spazio_comportamentale_potato = listOfGlobals['spazio_comportamentale_potato']
        spazio_comportamentale_potato = deepcopy(spazio_comportamentale)
        cartella_save = listOfGlobals['cartella_save']
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\n" + "Inizio processo di potatura e ridenominazione")

        spazio_comportamentale_potato = potatura_e_ridenominazione(spazio_comportamentale_potato)
        if spazio_comportamentale_potato.nodi_finali is None:
            sg.Popup('Attenzione!',
                     'Lo spazio comportamentale non ha nodi finali. Dopo la potatura è risultato vuoto')
            return
        if len(spazio_comportamentale_potato.nodi_finali)==0:
            sg.Popup('Attenzione!',
                     'Lo spazio comportamentale non ha nodi finali. Dopo la potatura è risultato vuoto')
            return

        stampa_spazio_potato_su_file(spazio_comportamentale_potato, cartella_save + nome)

        #salvo spazio potato su file
        spazio_salvataggio = crea_spazio_da_spazio_potato(spazio_comportamentale_potato)
        spazio_salvataggio.spazio_potato=True
        salva_spazio_potato_su_file(spazio_salvataggio, cartella_save + nome)

        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\n" + "Spazio correttamente creato e salvato")
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\n" + spazio_comportamentale_potato.riassunto_potatura())

        window_spazio_comportamentale['stampa_potatura'].update(disabled=False)
        window_spazio_comportamentale['potatura'].update(disabled=True)
        listOfGlobals['spazio_comportamentale_potato'] = spazio_comportamentale_potato

    def potatura2(nome):
        listOfGlobals = globals()
        spazio_comportamentale_oss = listOfGlobals['spazio_comportamentale_oss']
        spazio_comportamentale_potato_oss = listOfGlobals['spazio_comportamentale_potato_oss']
        spazio_comportamentale_potato_oss = deepcopy(spazio_comportamentale_oss)
        cartella_save = listOfGlobals['cartella_save']
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\n" + "Inizio processo di potatura e ridenominazione")

        spazio_comportamentale_potato_oss = potatura_e_ridenominazione(spazio_comportamentale_potato_oss)
        if spazio_comportamentale_potato_oss.nodi_finali is None:
            sg.Popup('Attenzione!',
                     'Lo spazio comportamentale non ha nodi finali. Dopo la potatura è risultato vuoto')
            return
        if len(spazio_comportamentale_potato_oss.nodi_finali)==0:
            sg.Popup('Attenzione!',
                     'Lo spazio comportamentale non ha nodi finali. Dopo la potatura è risultato vuoto')
            return

        stampa_spazio_potato_su_file(spazio_comportamentale_potato_oss, cartella_save + nome, "_oss")
        print("SPAZIO POTATO")
        for n in spazio_comportamentale_potato_oss.nodi:
            print(n.to_string()+" potato: "+str(n.potato))
        #salvo spazio su file
        spazio_salvataggio = crea_spazio_da_spazio_potato(spazio_comportamentale_potato_oss)
        spazio_salvataggio.spazio_potato=True
        salva_spazio_potato_su_file(spazio_salvataggio, cartella_save + nome, "_oss" )





        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\n" + "Spazio correttamente creato e salvato")
        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale[
                'informazioni'].get() + "\n" + spazio_comportamentale_potato_oss.riassunto_potatura())

        abilita_algoritmo2_potatura()

        listOfGlobals['spazio_comportamentale_potato_oss'] = spazio_comportamentale_potato_oss


    window_spazio_comportamentale = sg.Window('Spazio comportamentale', crea_layout_spazio_comportamentale())

    while True:
        event, values = window_spazio_comportamentale.read()
        if event == sg.WIN_CLOSED:
            return True
        elif event == "reset" or event == "reset_algoritmo2":
            reset()
        elif event == "conferma_cartella":
            conferma_cartella()
        elif event == "avvio_algoritmo1":
            algoritmo_crea_spazio_comportamentale()
        elif event == "avvio_algoritmo1_manuale":
            algoritmo_crea_spazio_comportamentale_manuale("/algoritmo1/")
        elif event == "conferma_nome_spazio":
            conferma_nome_spazio()
        elif event == "salva":
            salva_su_file("/algoritmo1/")
        elif event == "stampa":
            stampa_grafici("/algoritmo1/")
        elif event == "potatura":
            potatura("/algoritmo1/")
        elif event == "stampa_potatura":
            stampa_grafici_potatura("/algoritmo1/")
        elif event == "conferma_osservazione_lineare":
            conferma_osservazione_lineare()
        elif event == "avvio_algoritmo2":
            algoritmo_crea_spazio_comportamentale2()
        elif event == "salva_spazio2":
            salva_su_file2("/algoritmo2/")
        elif event == "stampa_spazio2":
            stampa_grafici2("/algoritmo2/")
        elif event == "potatura_spazio2":
            potatura2("/algoritmo2/")
        elif event == "stampa_potatura_spazio2":
            stampa_grafici_potatura2("/algoritmo2/")
        elif event == "avvio_algoritmo2_manuale":
            algoritmo_crea_spazio_comportamentale_manuale2("/algoritmo2/")


def gui_importa_rete():
    '''Metodo per gestire la finestra finalizzata ad importare una rete'''

    # Variabili
    global stato, cartella, automi, links, rete, cartella_save
    stato = "1"
    cartella = ""
    cartella_save = ""
    automi = []
    links = []
    rete = None

    def crea_layout_importa_rete():
        colonna1 = [
            [
                sg.Text("Seleziona cartella"),
                sg.Input(key='input_cartella', size=(20, 1)),
                sg.Button('Conferma', key='conferma_cartella')
            ],
            [
                sg.Button("Importa rete", key="importa_rete", disabled=True),
            ],
            [
                sg.Button("Reset", key="reset", disabled=False),
                sg.Button("Salva su file", key="salva", disabled=True),
                sg.Button("Mostra grafici", key="stampa", disabled=True)
            ],
            [
                sg.Button("Spazio comportamentale", key="spazio_comportamentale", disabled=True),
            ],
            [
                sg.Text("Automi:"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 10), key="automi", autoscroll=True
                )
            ],
            [
                sg.Text("Link:"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 5), key="link", autoscroll=True
                )
            ],
            [
                sg.Text("Reti:"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 10), key="rete", autoscroll=True
                )
            ],
        ]

        colonna2 = [
            [
                sg.Text("Informazioni"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 20), key="informazioni", autoscroll=True
                )
            ],
        ]

        layout_importa_rete = [
            [
                sg.Column(colonna1),
                sg.VSeperator(),
                sg.Column(colonna2),
            ]
        ]

        return layout_importa_rete

    def aggiorna_elenco_automi():
        '''aggiorna l'elenco degli automi importati con la rete'''

        listOfGlobals = globals()
        automi = listOfGlobals['automi']

        window_importa_rete['automi'].update("")
        if len(automi)!=0:
            for a in automi:
                window_importa_rete['automi'].update(
                    window_importa_rete['automi'].get() + "\n"+a.to_string())

    def aggiorna_elenco_links():
        '''Aggiorna l'elenco di link importati con la rete'''

        listOfGlobals = globals()
        links = listOfGlobals['links']

        window_importa_rete['link'].update("")
        if len(links)!=0:
            for l in links:
                window_importa_rete['link'].update(
                    window_importa_rete['link'].get() + "\n"+l.to_string())

    def aggiorna_rete():
        '''Aggiorna l'elenco delle transizioni'''

        listOfGlobals = globals()
        rete = listOfGlobals['rete']

        window_importa_rete['rete'].update("")
        if rete is not None:
            window_importa_rete['rete'].update(
                window_importa_rete['rete'].get() + "\n"+rete.to_string())

    def conferma_cartella():
        '''permette di selezionare la cartella di salvataggio'''

        listOfGlobals = globals()
        cartella = listOfGlobals['cartella']
        stato = listOfGlobals['stato']
        cartella_save = listOfGlobals['cartella_save']

        stato="conferma cartella"

        if values['input_cartella'] != "":

            cartella = values['input_cartella']
            x = datetime.datetime.now()
            data_attuale = str(x.strftime("%Y_%m_%d_%H_%M"))
            cartella_save = data_attuale + "_" + cartella
            window_importa_rete['conferma_cartella'].update(disabled=True)
            window_importa_rete['input_cartella'].update(disabled=True)
            window_importa_rete['importa_rete'].update(disabled=False)
            window_importa_rete['informazioni'].update(window_importa_rete['informazioni'].get()+"\nCartella selezionata: "+cartella)
            listOfGlobals['cartella']=cartella
            listOfGlobals['cartella_save'] = cartella_save
            listOfGlobals['stato']=stato
        else:
            sg.Popup('Attenzione!',
                     'Inserire un nome non vuoto')

    def spazio_comportamentale():
        '''Apre una nuova finestra per poter eseguire i 3 algoritmi'''

        listOfGlobals = globals()
        automi = listOfGlobals['automi']
        links = listOfGlobals['links']
        rete = listOfGlobals['rete']
        cartella_save = listOfGlobals['cartella_save']
        cartella = listOfGlobals['cartella']
        stato = listOfGlobals['stato']
        print("Tutto: " + cartella + "; " + cartella_save)
        gui_crea_spazio_comportamentale(automi, links, rete, cartella_save, cartella, stato, None, "")

    def salva_su_file():
        '''Salva le informazioni della rete su file'''

        listOfGlobals = globals()
        cartella = listOfGlobals['cartella']
        cartella_save = listOfGlobals['cartella_save']
        automi = listOfGlobals['automi']
        links = listOfGlobals['links']
        rete = listOfGlobals['rete']

        window_importa_rete['informazioni'].update(
            window_importa_rete['informazioni'].get() + "\n" + "Salvo file nella cartella: "+cartella_save)

        for a in automi:
            stampa_automa_su_file(a, cartella=cartella_save)
        stampa_rete_su_file(rete, cartella=cartella_save)

        window_importa_rete['informazioni'].update(
            window_importa_rete['informazioni'].get() + "\n" + "Creati file PNG dei grafici")

        salva_rete_su_file_txt(rete, cartella_save, rete.nome)
        salva_rete_su_file(rete, cartella_save, rete.nome)
        salva_rete_su_file_txt(rete, cartella_save, rete.nome)
        salva_links_su_file_txt(rete, cartella_save, "links")

        for a in automi:
            salva_automa_su_file(a, cartella_save, a.nome)
            salva_automa_su_file_txt(a, cartella_save, a.nome)

        window_importa_rete['informazioni'].update(
            window_importa_rete['informazioni'].get() + "\n" + "Creati file per la rete, i links e gli automi")


        window_importa_rete['salva'].update(disabled=True)
        window_importa_rete['stampa'].update(disabled=False)
        listOfGlobals['cartella_save'] = cartella_save

    def stampa_grafici():
        '''Mostra i grafici degli automi, links e transizioni'''

        listOfGlobals = globals()
        automi = listOfGlobals['automi']
        links = listOfGlobals['links']
        rete = listOfGlobals['rete']
        cartella_save = listOfGlobals['cartella_save']

        immagini=[]
        titoli=[]

        for a in automi:
            immagini.append(sg.Image(filename='Output/' + cartella_save + '/' + a.nome + '_grafico.png'))
            titoli.append(sg.Text(a.nome))
        immagine_rete = sg.Image(filename='Output/' + cartella_save + '/' + rete.nome + '_grafico.png')



        grafici_automi = [
            titoli,
            immagini
        ]

        grafici_reti = [
            immagine_rete
        ]

        layout_grafici = [
            [
                sg.Column(grafici_automi)
            ],
            [
                immagine_rete
            ]
        ]

        window_mostra_grafici = sg.Window('Mostra grafici', layout_grafici)

        while True:
            event, values = window_mostra_grafici.read()
            if event == sg.WINDOW_CLOSED:
                break
        window_mostra_grafici.close()

    def importa_rete():
        '''Gestisce l'importazione della rete
        il file deve contenere una classe di tipo Rete
        è possibile trovare un file di questo tipo nella cartella dei salvataggi di una precedente esecuzione del programma'''

        listOfGlobals = globals()

        rete = carica_rete_da_file()

        if (isinstance(rete, str)):
            window_importa_rete['informazioni'].update(
                window_importa_rete['informazioni'].get() + "\n" + "PROBLEMA LETTURA FILE\n" + rete)
        else:
            window_importa_rete['informazioni'].update(
                window_importa_rete['informazioni'].get() + "\n" + "FILE LETTO CORRETTAMENTE\n" + rete.to_string())

            listOfGlobals['automi'] = rete.automi
            listOfGlobals['links'] = rete.links
            listOfGlobals['rete'] = rete

            aggiorna_elenco_automi()
            aggiorna_elenco_links()
            aggiorna_rete()

            window_importa_rete['conferma_cartella'].update(disabled=True)
            window_importa_rete['input_cartella'].update(disabled=True)
            window_importa_rete['importa_rete'].update(disabled=True)
            window_importa_rete['salva'].update(disabled=False)
            window_importa_rete['stampa'].update(disabled=True)
            window_importa_rete['spazio_comportamentale'].update(disabled=False)


    def reset():
        '''Riporta la finestra nello stato iniziale'''

        listOfGlobals = globals()
        listOfGlobals['cartella'] = ""
        listOfGlobals['cartella_save'] = ""
        listOfGlobals['stato'] = "1"
        listOfGlobals['automi'] = []
        listOfGlobals['links'] = []
        listOfGlobals['rete'] = None
        aggiorna_elenco_automi()
        aggiorna_elenco_links()
        aggiorna_rete()
        window_importa_rete['conferma_cartella'].update(disabled=False)
        window_importa_rete['input_cartella'].update(disabled=False)
        window_importa_rete['importa_rete'].update(disabled=True)
        window_importa_rete['salva'].update(disabled=True)
        window_importa_rete['stampa'].update(disabled=True)
        window_importa_rete['informazioni'].update("RESET")
        window_importa_rete['spazio_comportamentale'].update(disabled=True)

    window_importa_rete = sg.Window('Importa rete', crea_layout_importa_rete())
    while True:
        event, values = window_importa_rete.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "conferma_cartella":
            conferma_cartella()
        elif event == "importa_rete":
            importa_rete()
        elif event == "reset":
            reset()
        elif event == "salva":
            salva_su_file()
            print("cartella salvataggio: "+cartella_save)
        elif event == "stampa":
            stampa_grafici()
        elif event == "spazio_comportamentale":
            out = spazio_comportamentale()

