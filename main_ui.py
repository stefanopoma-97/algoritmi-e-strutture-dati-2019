import PySimpleGUI as sg
from tkinter.filedialog import askopenfilename
from Classi.GestioneFile.input_output import *
from Classi.Automa.automa import *
from Classi.Automa.rete import *
from Classi.GestioneFile.grafici import *
from Classi.Automa.rete import *
from Classi.GestioneFile.input_output import *
import datetime




#rile
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# f = open(filename, "r")
# stringa_regex = f.read()
# print(stringa_regex)


#FUNZIONI
def crea_rete():
    # Variabili
    global stato, cartella, automi, links, rete, cartella_save
    stato = "1"
    cartella = ""
    cartella_save = ""
    automi = []
    links = []
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
                sg.Button("Carica rete 1", key="rete1", disabled=False)
            ],
            [
                sg.Text("Automi:"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 10), key="automi"
                )
            ],
            [
                sg.Text("Link:"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 5), key="link"
                )
            ],
            [
                sg.Text("Reti:"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 10), key="rete"
                )
            ],
        ]

        colonna2 = [
            [
                sg.Text("Informazioni"),

            ],
            [
                sg.Multiline(
                    "", enable_events=True, size=(40, 20), key="informazioni"
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

        stato="conferma cartella"

        if values['input_cartella'] != "":

            cartella = values['input_cartella']
            window_crea_rete['conferma_cartella'].update(disabled=True)
            window_crea_rete['input_cartella'].update(disabled=True)
            window_crea_rete['carica_automa'].update(disabled=False)
            window_crea_rete['informazioni'].update(window_crea_rete['informazioni'].get()+"\nCartella selezionata: "+cartella)
            listOfGlobals['cartella']=cartella
            listOfGlobals['stato']=stato
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


        x = datetime.datetime.now()
        data_attuale = str(x.strftime("%Y_%m_%d_%H_%M"))
        cartella_save = data_attuale +"_"+cartella

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

        a1 = carica_automa_da_file_txt("Input/test/automa1_save.txt")
        a2 = carica_automa_da_file_txt("Input/test/automa2_save.txt")
        automi = [a1, a2]

        links = carica_links_da_file_txt(automi, "Input/test/links_save.txt")

        rete = carica_rete_da_file_txt(automi, links, "Input/test/rete_save.txt")

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
        window_crea_rete['informazioni'].update("Caricata rete 1")


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
        window_crea_rete['input_cartella'].update(disabled=False)
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



layout = [[sg.Text("Home\nQuesta è la home, seleziona cosa vuoi fare")],
          [sg.Button("Crea una rete", key='crea_rete', size=(35, 2))],
          [sg.Button("ESCI", key="esci")]]

# Crea la finestra
window = sg.Window("Home", layout)

# loop per gli eventi
while True:
    event, values = window.read()

    if event == "esci" or event == sg.WIN_CLOSED:
        break
    elif event == "crea_rete":
        print("Avvio creazione rete")
        crea_rete()

window.close()


