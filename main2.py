from Classi.Automa.automa import *
from Classi.GestioneFile.grafici import *
from Classi.Automa.rete import *
from Classi.GestioneFile.input_output import *

# stato_1 = Stato('stato1')
# print(stato_1.to_string())
# stato_2 = Stato('stato2')
#
# stati = [stato_1, stato_2]
#
# s = [x for x in stati if x.nome == "stato3"][0]
# print(s)
# #
# print("S")
# print(s.to_string())
#
# stato_1.nome="stato1_aggiornato"
# print("S_modifica")
# print(s.to_string())


print("importa automi")
automi=[]
cartella="test"

a=carica_automa_da_file_txt(cartella, "automa1_save.txt")
if (isinstance(a, Automa)):
    print("AUTOMA LETTO CORRETTAMENTE")
    automi.append(a)
else:
    print("PROBLEMA LETTURA AUTOMA\n"+a)

#a=carica_automa_da_file_txt(cartella, "automa1_save_wrong_format.txt")
a=carica_automa_da_file_txt(cartella, "automa2_save.txt")
if (isinstance(a, Automa)):
    print("AUTOMA LETTO CORRETTAMENTE")
    automi.append(a)
else:
    print("PROBLEMA LETTURA AUTOMA\n"+a)


print("Importa LINK")
#links = carica_links_da_file_txt(cartella, "links_save_wrong_format.txt", automi)
links = carica_links_da_file_txt(cartella, "links_save.txt", automi)
if (isinstance(links, list)):
    print("LINKS LETTO CORRETTAMENTE")
else:
    print("PROBLEMA LETTURA LINKS\n"+links)


print("\nImporta transizioni")
#rete = carica_rete_da_file_txt(cartella, "rete_save_wrong_format.txt", automi, links)
rete = carica_rete_da_file_txt(cartella, "rete_save.txt", automi, links)
if (isinstance(rete, Rete)):
    print("RETE LETTA CORRETTAMENTE")
else:
    print("PROBLEMA LETTURA DELLA RETE\n"+rete)


rete.stampa()

