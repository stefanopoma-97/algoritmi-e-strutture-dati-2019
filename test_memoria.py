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
    return rete

def spazio_comportamentale(rete):
    return crea_spazio_comportamentale(rete)

# out = open("Output/Test memoria/Memoria rete 1.txt", "w")
# tracemalloc.start()
# out.write("inizio programma")
# out.write(str(tracemalloc.get_traced_memory())+" Byte\n\n")
#
# rete = crea_rete1()
# out.write("Importata la rete 1")
# out.write(str(tracemalloc.get_traced_memory())+" Byte\n\n")

# spazio = spazio_comportamentale(rete)
# out.write("Creato lo spazio comportamentale")
# out.write(str(tracemalloc.get_traced_memory())+" Byte\n\n")
#
# spazio = spazio_comportamentale(rete)
# out.write("Creato lo spazio comportamentale 2")
# out.write(str(tracemalloc.get_traced_memory())+" Byte\n\n")

# spazio = potatura_e_ridenominazione(spazio)
# out.write("Potatura spazio")
# out.write(str(tracemalloc.get_traced_memory())+" Byte\n\n")
#
# spazio_oss = crea_spazio_comportamentale2(rete, ["o3","o2"])
# out.write("Creazione spazio compartamentale relativo ad una osservazione lineare")
# out.write(str(tracemalloc.get_traced_memory())+" Byte\n\n")



#del spazio
#del spazio_oss
# gc.collect(generation=2)
# gc.collect(generation=1)
# gc.collect()
#
# out.write("eliminato tutto")
# out.write(str(tracemalloc.get_traced_memory())+" Byte\n\n")


# spazio_oss_potato = potatura_e_ridenominazione(spazio_oss)
# diagnosi_sistemo_spazio(spazio_comportamentale)
# ridenominazione_spazio_appena_creato(spazio_comportamentale)
# #diagnosi_algoritmo_su_spazio(spazio_oss_potato)
# out.write("Diagnosi")
# out.write(str(tracemalloc.get_traced_memory())+" Byte\n\n")

#out.close()





data=[]

for u in range(10):
    tracemalloc.start()
    #data.append((tracemalloc.get_traced_memory())[0])

    crea_rete1()
    data.append((tracemalloc.get_traced_memory())[0])


print("FINITO ESECUZIONE")
#out = open("Output/Test spazio/creazione rete - rete 1.txt", "w")

for d in data:
    print(str(d))

print("MEDIA: "+str(statistics.mean(data)))


