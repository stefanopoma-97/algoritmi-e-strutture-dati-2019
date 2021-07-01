from Classi.GestioneFile.grafici import *
from Classi.Automa.rete import *
from Classi.GestioneFile.input_output import *

# Creo un nuovo automa
automa1 = Automa('automa1')
automa2 = Automa('automa2')

# definisco i suoi stati
stato1 = Stato("20")
stato2 = Stato("21")

stato3 = Stato("30")
stato4 = Stato("31")

automa1.stati = [stato1, stato2]
automa1.stato_corrente = [stato1]
automa1.stati_iniziali = [stato1]

automa2.stati = [stato3, stato4]
automa2.stato_corrente = [stato3]
automa2.stati_iniziali = [stato3]

# creo transizioni tra stati
transizione1 = Transizione("t1")
transizione1.stato_sorgente = stato1
transizione1.stato_destinazione = stato2

transizione2 = Transizione("t2")
transizione2.stato_sorgente = stato2
transizione2.stato_destinazione = stato1

transizione3 = Transizione("t3")
transizione3.stato_sorgente = stato1
transizione3.stato_destinazione = stato1

transizione4 = Transizione("t4")
transizione4.stato_sorgente = stato3
transizione4.stato_destinazione = stato4

# automaticamente lo stato verrà popolato con l'array delle transizioni uscenti
stato1.transizioni = [transizione1, transizione3]
#stato1.add_transizione(transizione1)
#stato1.add_transizione(transizione2)

stato2.transizioni = [transizione2]
stato3.transizioni = [transizione4]

# le transizioni vengono arricchiete da osservazione, rilevanza e eventi
transizione1.osservazione = "o1"
transizione1.rilevanza = "r1"

transizione2.osservazione = "o2"

transizione3.rilevanza = "r3"

# eventi
evento1 = Evento("e1")
evento2 = Evento("e2")

#transizione1.input = [evento1]
transizione1.add_input(evento1)
#transizione1.output = [evento1, evento2]
transizione1.add_output(evento1)
transizione1.add_output(evento2)

transizione2.input = [evento2]

# Creo link
link1 = Link("L1", automa1, automa2)
link2 = Link("L2", automa2, automa1)

evento1.link=link1
evento2.link=link2

print("Automa 1")
automa1.stampa()
print("Automa 1 txt")
print(automa1.to_string_txt())

print("Automa 2 txt")
print(automa2.to_string_txt())




#automa2.stampa()


#STAMPA SU FILE
cartella="1"
print("grafico")
#stampa_automa(automa1)

stampa_automa_su_file(automa1, cartella=cartella)
stampa_automa_su_file(automa2, cartella=cartella)

#stampa_automi_su_file([automa1, automa2],cartella="test doppio")



#RETE

rete = Rete("rete 1", [automa1, automa2], [link1, link2])
#rete.stampa()
print("Link txt")
print(rete.to_string_link_txt())

print("Transizioni txt")
print(rete.to_string_txt())

#STAMPA RETE SU FILE
#stampa_rete_su_file(rete,cartella=cartella)


#INPUT / OUTPUT FILE
salva_automa_su_file(automa1, cartella, 'automa1_save')
# salva_automa_su_file_txt(automa1, cartella, 'automa1_save')
# salva_automa_su_file_txt(automa2, cartella, 'automa2_save')
# automa_load = carica_automa_da_file(cartella, 'automa1_save')
# print("LOAD")
# automa_load.stampa()

# salva_rete_su_file(rete,cartella,"rete_save")
# salva_rete_su_file_txt(rete,cartella,"rete_save")
# salva_links_su_file_txt(rete,cartella,"links_save")
# rete_load = carica_rete_da_file(cartella, 'rete_save')
# print("LOAD")
# rete_load.stampa()

#CHIUEDI FILE INPUT
# from tkinter.filedialog import askopenfilename
#
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# print(filename)

# transizioni=[]
# for a in rete.automi:
#     transizioni+=get_transizioni(a)
#
# print(transizioni_to_string(transizioni))