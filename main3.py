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
osservazione1=["o3","o2"]
osservazione2=["act", "sby", "nop"]
spazio = crea_spazio_comportamentale2(rete1, osservazione1)
stampa_spazio_su_file(spazio, "SPAZIO")

spazio_potato = potatura_e_ridenominazione(spazio)
stampa_spazio_potato_su_file(spazio_potato, "SPAZIO")