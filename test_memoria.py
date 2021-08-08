import gc
import tracemalloc
from Classi.GestioneFile.grafici import *
from Classi.Automa.rete import *
from Classi.GestioneFile.input_output import *
from Classi.Spazio.spazio_comportamentale import *
from Classi.Algoritmi.algoritmi_spazio_comportamentale import *
import timeit
import statistics


def crea_rete1():
    a1 = carica_automa_da_file_txt("Input/RETE1/C2.txt")
    a2 = carica_automa_da_file_txt("Input/RETE1/C3.txt")
    automi = [a1, a2]

    links = carica_links_da_file_txt(automi, "Input/RETE1/links.txt")

    rete = carica_rete_da_file_txt(automi, links, "Input/RETE1/rete 1.txt")
    del a1
    del a2
    del automi
    del links

    return rete

def crea_rete2():
    a1 = carica_automa_da_file_txt("Input/RETE2/S.txt")
    a2 = carica_automa_da_file_txt("Input/RETE2/B.txt")
    automi = [a1, a2]
    links = carica_links_da_file_txt(automi, "Input/RETE2/links.txt")
    rete = carica_rete_da_file_txt(automi, links, "Input/RETE2/rete 2.txt")
    del a1
    del a2
    del automi
    del links
    return rete

def crea_rete3():
    a1 = carica_automa_da_file_txt("Input/RETE3/C1.txt")
    a2 = carica_automa_da_file_txt("Input/RETE3/C2.txt")
    a3 = carica_automa_da_file_txt("Input/RETE3/C3.txt")
    automi = [a1, a2, a3]
    links = carica_links_da_file_txt(automi, "Input/RETE3/links.txt")
    rete = carica_rete_da_file_txt(automi, links, "Input/RETE3/rete 3.txt")
    del a1
    del a2
    del a3
    del automi
    del links
    return rete

def crea_rete4():
    a1 = carica_automa_da_file_txt("Input/RETE4/CANCELLO.txt")
    a2 = carica_automa_da_file_txt("Input/RETE4/TELECOMANDO.txt")
    automi = [a1, a2]
    links = carica_links_da_file_txt(automi, "Input/RETE4/links.txt")
    rete = carica_rete_da_file_txt(automi, links, "Input/RETE4/rete 4.txt")
    del a1
    del a2
    del automi
    del links
    return rete

def crea_rete5():
    a1 = carica_automa_da_file_txt("Input/RETE5/CANCELLO.txt")
    a2 = carica_automa_da_file_txt("Input/RETE5/TELECOMANDO.txt")
    a3 = carica_automa_da_file_txt("Input/RETE5/PERSONA.txt")
    automi = [a1, a2, a3]
    links = carica_links_da_file_txt(automi, "Input/RETE5/links.txt")
    rete = carica_rete_da_file_txt(automi, links, "Input/RETE5/rete 5.txt")
    del a1
    del a2
    del a3
    del automi
    del links
    return rete

def crea_spazio1():
    spazio=carica_spazio_da_file("Input/spazio1_salvataggio")
    return spazio

def crea_spazio2():
    spazio=carica_spazio_da_file("Input/spazio2_salvataggio")
    return spazio

def crea_spazio3():
    spazio=carica_spazio_da_file("Input/spazio3_salvataggio")
    return spazio

def crea_spazio4():
    spazio=carica_spazio_da_file("Input/spazio4_salvataggio")
    return spazio

def crea_spazio5():
    spazio=carica_spazio_da_file("Input/spazio5_salvataggio")
    return spazio

def crea_spazio1_oss():
    spazio=carica_spazio_da_file("Input/spazio1_potato_salvataggio_oss")
    return spazio

def crea_spazio2_oss():
    spazio=carica_spazio_da_file("Input/spazio2_potato_salvataggio_oss")
    return spazio

def crea_spazio3_oss():
    spazio=carica_spazio_da_file("Input/spazio3_potato_salvataggio_oss")
    return spazio

def crea_spazio4_oss():
    spazio=carica_spazio_da_file("Input/spazio4_potato_salvataggio_oss")
    return spazio

def crea_spazio5_oss():
    spazio=carica_spazio_da_file("Input/spazio5_potato_salvataggio_oss")
    return spazio


def spazio_comportamentale(rete):
    return crea_spazio_comportamentale(rete)





gc.collect()

data=[]

for u in range(100):
    tracemalloc.start()
    spazio=crea_spazio3_oss()
    diagnosi_sistemo_spazio(spazio)
    diagnosi_algoritmo_su_spazio_migliorato(spazio)
    data.append((tracemalloc.get_traced_memory())[0])


print("MEDIA: "+str(statistics.mean(data)))


out = open("Output/Test memoria/algoritmo3 rete3 migliorato.txt", "w")

out.write(str(statistics.mean(data)))
out.close()

print(str(statistics.mean(data)))



