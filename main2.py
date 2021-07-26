
lista_sequenza=["fr|ε","f"]
etichetta=""
for tra in lista_sequenza:
    print("\tValore di rilevanza:"+tra)
    if tra!=" ":
        if etichetta=="":
            etichetta=tra
        else:
            if ("|" in etichetta) and ("|" in tra):
                divisione_etichetta = etichetta.split("|")
                divisione_tra = tra.split("|")
                out=""
                for e in divisione_etichetta:
                    for t in divisione_tra:
                        #print("Analizzo: "+e+", "+t)
                        if e != "ε" and t != "ε":
                            out = out + e + t + "|"
                        elif e == "ε" and t != "ε":
                            out = out + t + "|"
                        elif e != "ε" and t == "ε":
                            out = out + e + "|"
                        else:
                            out = out + "ε|"
                        #print("out: "+out+"\n")
                etichetta = out[:-1]
            elif "|" in tra:
                divisione = tra.split("|")
                out = ""
                for el in divisione:
                    if el != "ε":
                        el = etichetta + el
                        out = out + el + "|"
                    else:
                        el = etichetta
                        out = out + el + "|"
                etichetta = out[:-1]
            elif "|" in etichetta:
                divisione = etichetta.split("|")
                out = ""
                for el in divisione:
                    if el != "ε":
                        el = el + tra
                        out = out + el + "|"
                    else:
                        el = tra
                        out = out + el + "|"
                etichetta = out[:-1]
            else:
                etichetta=etichetta+tra

    print("ETICHETTA: "+etichetta)

if etichetta=="":
    etichetta=" "

print(etichetta)
