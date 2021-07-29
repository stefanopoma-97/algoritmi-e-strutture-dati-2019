from Classi.GestioneFile.grafici import *
from Classi.Automa.rete import *
from Classi.GestioneFile.input_output import *
from Classi.Spazio.spazio_comportamentale import *
from Classi.Algoritmi.algoritmo_spazio_comportamentale import *


import re
REGEX_AUTOMA="^[a-zA-Z0-9]+\\n[0-9]+(\,[0-9]+)*\\n([0-9]+(\,[0-9]+)*)?\\n[0-9]+\>[a-zA-Z0-9]+\>[0-9]+(\,[0-9]+\>[a-zA-Z0-9]+\>[0-9]+)*\\n"
REGEX_LINK="^[a-zA-Z0-9]+\>[a-zA-Z0-9]+\>[a-zA-Z0-9]+\\n([a-zA-Z0-9]+\>[a-zA-Z0-9]+\>[a-zA-Z0-9]+\\n)*"
REGEX_RETE="^[a-zA-Z0-9 ]+\\n([a-zA-Z0-9]+\,[a-zA-Z0-9]+\,(([a-zA-Z0-9]+\([a-zA-Z0-9]+\))| )\/\{((([a-zA-Z0-9]+\([a-zA-Z0-9]+\))(\;[a-zA-Z0-9]+\([a-zA-Z0-9]+\))*)| )\}\,([a-zA-Z0-9]+| )\,([a-zA-Z0-9]+| )\\n)*"

stringa= "automa1\n20,21\n\n20>t1>21,20>t3>20,21>t2>20\n"
f = open('Input/test/automa1_save.txt', "r")
stringa2=f.read()

x = re.search(REGEX_AUTOMA, stringa2)
if x:
  print("YES! We have a match automa!")
else:
  print("No match")


f = open('Input/test/links_save.txt', "r")
stringa2=f.read()
print(repr(stringa2))

x = re.fullmatch(REGEX_LINK, stringa2)
if x:
  print("YES! We have a match links!")
else:
  print("No match")


# f = open('Input/test/rete_save.txt', "r")
# stringa2=f.read()
#
# x = re.search(REGEX_RETE, stringa2)
# if x:
#   print("YES! We have a match rete!")
# else:
#   print("No match")
a1 = carica_automa_da_file_txt("Input/RETE1/C2.txt")
a2 = carica_automa_da_file_txt("Input/RETE1/C3.txt")
automi = [a1, a2]

links = carica_links_da_file_txt(automi, "Input/RETE1/links.txt")

rete1 = carica_rete_da_file_txt(automi, links, "Input/RETE1/rete 1.txt")

a1 = carica_automa_da_file_txt("Input/RETE2/S.txt")
a2 = carica_automa_da_file_txt("Input/RETE2/B.txt")
automi = [a1, a2]

links = carica_links_da_file_txt(automi, "Input/RETE2/links.txt")

rete2 = carica_rete_da_file_txt(automi, links, "Input/RETE2/rete 2.txt")


a1 = carica_automa_da_file_txt("Input/RETE3/C1.txt")
a2 = carica_automa_da_file_txt("Input/RETE3/C2.txt")
a3 = carica_automa_da_file_txt("Input/RETE3/C3.txt")
automi = [a1, a2, a3]

links = carica_links_da_file_txt(automi, "Input/RETE3/links.txt")

rete3 = carica_rete_da_file_txt(automi, links, "Input/RETE3/rete 3.txt")
#print(rete.to_string())

# automi = rete.automi
# links = rete.links
# stati = rete.get_stati()
# transizioni = rete.get_transizioni()
# automi[0].stampa()
# print(stati[1].to_string())
#
# automi[0].stato_corrente=[stati[1]]
# automi[0].stampa()
#
# print("STATI Correnti")
#
# stati_correnti = rete.get_stati_correnti()
# print(stati_to_string(stati_correnti))
# link1=links[0]
# link2=links[1]
# print(link1.to_string())
# print(link2.to_string())
#
#
#
#
# dizionario = dict()
# dizionario[link1.nome]=[link1, link1.evento.nome]
# dizionario[link2.nome]=[link2, link2.evento.nome]
#
#
#
# nodo1 = Nodo(stati, "", False, dizionario, True)
# nodo2 = Nodo(stati, "", False, dizionario, True)
#
# tran = Transizione_spazio("t1",nodo1,nodo2,"o","r")
# print(tran.to_string())


# spazio = crea_spazio_comportamentale(rete)
# print("\n\n\n----------------")
# print(spazio.to_string())
#
#
# spazio_ridenominato = potatura_e_ridenominazione(spazio)
#
# stampa_spazio_su_file(spazio, "SPAZIO")
# stampa_spazio_ridenominato_su_file(spazio_ridenominato, "SPAZIO")
#
#
# print("NUMERO DI TRANSIZIONI: "+str(len(spazio.transizioni)))
# print("NUMERO DI TRANSIZIONI metodo: "+str(len(get_transizioni_spazio(spazio))))
# spazio1 = carica_spazio_da_file("Input/RETE1/spazio1_salvataggio")
# spazio2 = carica_spazio_da_file("Input/RETE2/spazio2_salvataggio")
# spazio3 = carica_spazio_da_file("Input/RETE3/spazio3_salvataggio")

spazio1_potato_salvataggio_oss = carica_spazio_da_file("Input/spazio1_potato_salvataggio_oss")
spazio2_salvataggio= carica_spazio_da_file("Input/spazio2_salvataggio")
spazio2_potato_salvataggio= carica_spazio_da_file("Input/spazio2_potato_salvataggio")
spazio2_potato_salvataggio_oss = carica_spazio_da_file("Input/spazio2_potato_salvataggio_oss")
spazio3_salvataggio= carica_spazio_da_file("Input/spazio3_salvataggio")
spazio3_potato_salvataggio= carica_spazio_da_file("Input/spazio3_potato_salvataggio")
spazio3_potato_salvataggio_oss = carica_spazio_da_file("Input/spazio3_potato_salvataggio_oss")
osservazione1=["o3","o2"]
osservazione2=["act", "sby", "nop"]
osservazione3=["o1", "o2"]


#SPAZIO 1
# ridenominazione_spazio_appena_creato(spazio1_potato_salvataggio_oss)
#
# #modificato con 1 transizione sorgente a stato iniziale
# spazio1_potato_salvataggio_oss_modificato= deepcopy(spazio1_potato_salvataggio_oss)
# spazio1_potato_salvataggio_oss_modificato.nodi_iniziali[0].transizioni_sorgente = [spazio1_potato_salvataggio_oss_modificato.transizioni[0]]
#
#DIAGNOSI
# stampa_spazio_ridenominato_su_file(spazio1_potato_salvataggio_oss,"SPAZIO","__0__")
# diagnosi_sistemo_spazio(spazio1_potato_salvataggio_oss)
# ridenominazione_spazio_appena_creato(spazio1_potato_salvataggio_oss)
#
# print("----------------ITERAZIONE 1\n\n")
# diagnosi1=diagnosi_algoritmo_su_spazio_migliorato(spazio1_potato_salvataggio_oss)
#
# stampa_spazio_ridenominato_su_file(diagnosi1,"SPAZIO","__1__")

# print("----------------ITERAZIONE 2\n\n")
# diagnosi2=diagnosi_algoritmo_su_spazio_migliorato(diagnosi1)
# stampa_spazio_ridenominato_su_file(diagnosi2,"SPAZIO","__2__")
#
# print("----------------ITERAZIONE 3\n\n")
# diagnosi3=diagnosi_algoritmo_su_spazio_migliorato(diagnosi2)
# stampa_spazio_ridenominato_su_file(diagnosi3,"SPAZIO","__3__")
#
# print("----------------ITERAZIONE 4\n\n")
# diagnosi4=diagnosi_algoritmo_su_spazio_migliorato(diagnosi3)
# stampa_spazio_ridenominato_su_file(diagnosi4,"SPAZIO","__4__")
#
# print("----------------ITERAZIONE 5\n\n")
# diagnosi5=diagnosi_algoritmo_su_spazio_migliorato(diagnosi4)
# stampa_spazio_ridenominato_su_file(diagnosi5,"SPAZIO","__5__")
#
# print("----------------ITERAZIONE 6\n\n")
# diagnosi6=diagnosi_algoritmo_su_spazio_migliorato(diagnosi5)
# stampa_spazio_ridenominato_su_file(diagnosi6,"SPAZIO","__6__")
#
# print("----------------ITERAZIONE 7\n\n")
# diagnosi7=diagnosi_algoritmo_su_spazio_migliorato(diagnosi6)
# stampa_spazio_ridenominato_su_file(diagnosi7,"SPAZIO","__7__")
#
# print("----------------ITERAZIONE 8\n\n")
# diagnosi8=diagnosi_algoritmo_su_spazio_migliorato(diagnosi7)
# stampa_spazio_ridenominato_su_file(diagnosi8,"SPAZIO","__8__")
#
# print("----------------ITERAZIONE 9\n\n")
# diagnosi9=diagnosi_algoritmo_su_spazio_migliorato(diagnosi8)
# stampa_spazio_ridenominato_su_file(diagnosi9,"SPAZIO","__9__")
#
# print("----------------ITERAZIONE 10\n\n")
# diagnosi10=diagnosi_algoritmo_su_spazio_migliorato(diagnosi9)
# stampa_spazio_ridenominato_su_file(diagnosi10,"SPAZIO","__10__")



#SPAZIO 2
ridenominazione_spazio_appena_creato(spazio2_potato_salvataggio_oss)
stampa_spazio_ridenominato_su_file(spazio2_potato_salvataggio_oss,"SPAZIO","__0__")
diagnosi_sistemo_spazio(spazio2_potato_salvataggio_oss)


print("----------------ITERAZIONE 1\n\n")
diagnosi1=diagnosi_algoritmo_su_spazio_migliorato(spazio2_potato_salvataggio_oss)

stampa_spazio_ridenominato_su_file(diagnosi1,"SPAZIO","__FINE__")

# print("----------------ITERAZIONE 2\n\n")
# diagnosi2=diagnosi_algoritmo_su_spazio_migliorato(diagnosi1)
# stampa_spazio_ridenominato_su_file(diagnosi2,"SPAZIO","__2__")
#
# print("----------------ITERAZIONE 3\n\n")
# diagnosi3=diagnosi_algoritmo_su_spazio_migliorato(diagnosi2)
# stampa_spazio_ridenominato_su_file(diagnosi3,"SPAZIO","__3__")


#diagnosi=diagnosi(spazio3_potato_salvataggio_oss)
#ridenominazione_spazio_appena_creato(diagnosi)
#stampa_spazio_ridenominato_su_file(diagnosi,"SPAZIO")


#crea_spazio_comportamentale2_da_spazio(spazio3_salvataggio, ["o1","o2"])


