import PySimpleGUI as sg
from tkinter.filedialog import askopenfilename
from Classi.GestioneFile.input_output import *
from Classi.Automa.automa import *
from Classi.Automa.rete import *
from Classi.GestioneFile.grafici import *
from Classi.Automa.rete import *
from Classi.GestioneFile.input_output import *
import datetime
from Classi.GUI.Gui_rete import *



#FUNZIONI


#Main e finestra principale
layout = [[sg.Text("Home\nQuesta è la home, seleziona cosa vuoi fare")],
          [sg.Button("Crea una rete", key='crea_rete', size=(35, 2))],
            [sg.Button("Importa rete da file", key='importa_rete', size=(35, 2))],
            [sg.Button("Importa Spazio comportamentale da file", key='importa_spazio', size=(35, 2))],
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
        gui_crea_rete()
    elif event == "importa_rete":
        print("Avvio importa rete")
        gui_importa_rete()
    elif event == "importa_spazio":
        print("Avvio importa spazio")
        spazio = carica_spazio_da_file()
        if (isinstance(spazio, str)):
            sg.Popup('Attenzione!',
                     'Errore: '+spazio)
        else:
            gui_crea_spazio_comportamentale([], [], None, "", "", None, spazio, spazio.nome)

window.close()



