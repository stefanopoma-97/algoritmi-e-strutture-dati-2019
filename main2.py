from Classi.Algoritmi.algoritmo_spazio_comportamentale import *


# ε
lista_sequenza=["i|t","(a)*","o|u"]
etichetta=""
for tra in lista_sequenza:
    etichetta= crea_etichetta_and(etichetta, tra)

    print("ETICHETTA: "+etichetta)

if etichetta=="":
    etichetta=" "

print(etichetta)
