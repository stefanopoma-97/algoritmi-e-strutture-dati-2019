import tracemalloc
from Classi.GestioneFile.grafici import *
from Classi.Automa.rete import *
from Classi.GestioneFile.input_output import *
from Classi.Spazio.spazio_comportamentale import *
from Classi.Algoritmi.algoritmi_spazio_comportamentale import *


def crea_rete1():
    a1 = carica_automa_da_file_txt("Input/RETE1/C2.txt")
    a2 = carica_automa_da_file_txt("Input/RETE1/C3.txt")
    automi = [a1, a2]

    links = carica_links_da_file_txt(automi, "Input/RETE1/links.txt")

    rete = carica_rete_da_file_txt(automi, links, "Input/RETE1/rete 1.txt")
    return rete

def spazio_comportamentale(rete):
    return crea_spazio_comportamentale(rete)

out = open("Output/Test memoria/Memoria rete 1.txt", "w")
tracemalloc.start()
out.write(str(tracemalloc.get_traced_memory())+"\n")

rete = crea_rete1()
out.write(str(tracemalloc.get_traced_memory())+"\n")

# spazio = spazio_comportamentale(rete)
# out.write(str(tracemalloc.get_traced_memory())+"\n")
#
# spazio = spazio_comportamentale(rete)
# out.write(str(tracemalloc.get_traced_memory())+"\n")
#
# spazio = spazio_comportamentale(rete)
# out.write(str(tracemalloc.get_traced_memory())+"\n")


spazio_oss = crea_spazio_comportamentale2(rete, ["o3","o2"])
out.write(str(tracemalloc.get_traced_memory())+"\n")






