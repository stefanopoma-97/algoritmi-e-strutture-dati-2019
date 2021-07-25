stringa="g|ε"
aggiunta="a"

if "|" in stringa:
    divisione = stringa.split("|")
    out=""
    for el in divisione:
        print("analizzo: "+el)
        if el!="ε":
            el=aggiunta+el
            out = out + el + "|"
        else:
            el=aggiunta
            out = out + el + "|"
    out = out[:-1]

print(out)
