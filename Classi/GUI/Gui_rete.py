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
        listOfGlobals = globals()
        automi = listOfGlobals['automi']

        window_crea_rete['automi'].update("")
        if len(automi)!=0:
            for a in automi:
                window_crea_rete['automi'].update(
                    window_crea_rete['automi'].get() + "\n"+a.to_string())


    def aggiorna_elenco_links():
        listOfGlobals = globals()
        links = listOfGlobals['links']

        window_crea_rete['link'].update("")
        if len(links)!=0:
            for l in links:
                window_crea_rete['link'].update(
                    window_crea_rete['link'].get() + "\n"+l.to_string())

    def aggiorna_rete():
        listOfGlobals = globals()
        rete = listOfGlobals['rete']

        window_crea_rete['rete'].update("")
        if rete is not None:
            window_crea_rete['rete'].update(
                window_crea_rete['rete'].get() + "\n"+rete.to_string())

    def conferma_cartella():
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
    global stato, cartella, automi, links, rete, cartella_save, spazio_comportamentale, nome_spazio, elenco_cartelle, spazio_importato, spazio_comportamentale_potato
    stato = s
    cartella = c2
    cartella_save = c
    automi = a
    links = l
    rete = r
    elenco_cartelle = []
    spazio_comportamentale = spazio
    spazio_importato = copy.deepcopy(spazio)
    nome_spazio = nome_S
    spazio_comportamentale_potato = None

    print("Pagina creazione spazio comportamentale")
    print("cartella_save: "+cartella_save)
    print("automi: " + str(len(automi)))
    print("links: " + str(len(links)))
    #print("rete: " + rete.to_string())

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
                sg.Text("Algoritmo 1"),
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
                sg.Text("Algoritmo 2"),
            ],
            [

                sg.Text("Inserisci un osservazione lineare"),
                sg.Input(key='input_osservazione_lineare', size=(20, 1), disabled=True),
                sg.Button('Conferma', key='conferma_osservazione_lineare')

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

    def conferma_cartella():
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
                    window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=True)
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
                    window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=True)
                    window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=True)
                    window_spazio_comportamentale['avvio_algoritmo1_manuale'].update(disabled=True)
                    window_spazio_comportamentale['salva'].update(disabled=False)
                    window_spazio_comportamentale['potatura'].update(disabled=False)
                    window_spazio_comportamentale['reset'].update(disabled=False)
                    window_spazio_comportamentale['informazioni'].update(
                        window_spazio_comportamentale[
                            'informazioni'].get() + "\nCartella selezionata: " + cartella_save)
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
                window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=False)
                window_spazio_comportamentale['avvio_algoritmo1_manuale'].update(disabled=False)
                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale['informazioni'].get() + "\nNome spazio impostato: " + nome_spazio)
                listOfGlobals['nome_spazio'] = nome_spazio
        else:
            sg.Popup('Attenzione!',
                     'Inserire un nome non vuoto')

    def reset():
        window_spazio_comportamentale['conferma_cartella'].update(disabled=False)
        window_spazio_comportamentale['input_cartella'].update("", disabled=False)
        window_spazio_comportamentale['conferma_nome_spazio'].update(disabled=True)
        window_spazio_comportamentale['input_nome_spazio'].update("", disabled=True)
        window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=True)
        window_spazio_comportamentale['avvio_algoritmo1_manuale'].update(disabled=True)
        window_spazio_comportamentale['salva'].update(disabled=True)
        window_spazio_comportamentale['stampa'].update(disabled=True)
        window_spazio_comportamentale['stampa_potatura'].update(disabled=True)
        window_spazio_comportamentale['potatura'].update(disabled=True)
        window_spazio_comportamentale['informazioni'].update("RESET")
        listOfGlobals = globals()
        listOfGlobals['spazio_comportamentale']=None

    def algoritmo_crea_spazio_comportamentale():
        listOfGlobals = globals()
        rete = listOfGlobals['rete']
        spazio_comportamentale = listOfGlobals['spazio_comportamentale']
        nome_spazio = listOfGlobals['nome_spazio']

        spazio_comportamentale = crea_spazio_comportamentale(rete)
        spazio_comportamentale.nome=nome_spazio


        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale['informazioni'].get() + "\nCreato lo spazio comportamentale: \n" + spazio_comportamentale.riassunto())
        listOfGlobals['spazio_comportamentale'] = spazio_comportamentale
        window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=True)
        window_spazio_comportamentale['avvio_algoritmo1_manuale'].update(disabled=True)
        window_spazio_comportamentale['salva'].update(disabled=False)
        window_spazio_comportamentale['potatura'].update(disabled=False)

    def algoritmo_crea_spazio_comportamentale_manuale(nome):
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
                window_spazio_comportamentale['avvio_algoritmo1'].update(disabled=True)
                window_spazio_comportamentale['avvio_algoritmo1_manuale'].update(disabled=True)
                window_spazio_comportamentale['salva'].update(disabled=False)
                window_spazio_comportamentale['potatura'].update(disabled=False)
                if fine_a==False:
                    window_spazio_comportamentale['informazioni'].update(
                        window_spazio_comportamentale[
                            'informazioni'].get() + "\nConcludo l'esecuzione senza aver generato tutto lo spazio comportamentale \n")

                window_spazio_comportamentale['informazioni'].update(
                    window_spazio_comportamentale['informazioni'].get() + "\nCreato lo spazio comportamentale: \n" + spazio.riassunto())
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


    def salva_su_file(nome):
        listOfGlobals = globals()
        cartella_save = listOfGlobals['cartella_save']
        spazio_comportamentale = listOfGlobals['spazio_comportamentale']

        window_spazio_comportamentale['informazioni'].update(
            window_spazio_comportamentale['informazioni'].get() + "\n" + "Salvo file nella cartella: " + cartella_save)

        stampa_spazio_su_file(spazio_comportamentale, cartella_save+nome)
        stampa_spazio_ridenominato_su_file(spazio_comportamentale, cartella_save + nome)

        salva_spazio_su_file(spazio_comportamentale, cartella_save+nome)


        window_spazio_comportamentale['salva'].update(disabled=True)
        window_spazio_comportamentale['stampa'].update(disabled=False)

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



    window_spazio_comportamentale = sg.Window('Spazio comportamentale', crea_layout_spazio_comportamentale())

    while True:
        event, values = window_spazio_comportamentale.read()
        if event == sg.WIN_CLOSED:
            return True
        elif event == "reset":
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




def gui_importa_rete():
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
        listOfGlobals = globals()
        automi = listOfGlobals['automi']

        window_importa_rete['automi'].update("")
        if len(automi)!=0:
            for a in automi:
                window_importa_rete['automi'].update(
                    window_importa_rete['automi'].get() + "\n"+a.to_string())

    def aggiorna_elenco_links():
        listOfGlobals = globals()
        links = listOfGlobals['links']

        window_importa_rete['link'].update("")
        if len(links)!=0:
            for l in links:
                window_importa_rete['link'].update(
                    window_importa_rete['link'].get() + "\n"+l.to_string())

    def aggiorna_rete():
        listOfGlobals = globals()
        rete = listOfGlobals['rete']

        window_importa_rete['rete'].update("")
        if rete is not None:
            window_importa_rete['rete'].update(
                window_importa_rete['rete'].get() + "\n"+rete.to_string())

    def conferma_cartella():
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

