from Classi.Algoritmi.algoritmo_spazio_comportamentale import *



lista_sequenza=["fr|ε","f|r"]
etichetta=""
for tra in lista_sequenza:
    if tra!=" ":
        if etichetta=="":
            etichetta=tra
        else:
            etichetta= crea_etichetta_and(etichetta, tra)

    print("ETICHETTA: "+etichetta)

if etichetta=="":
    etichetta=" "

print(etichetta)
