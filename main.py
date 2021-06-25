from Classi.Automa.automa import *
from Classi.Automa.grafici import *
from graphviz import Digraph



#Creo un nuovo automa
automa1 = Automa('automa 1')

#definisco i suoi stati
stato1 = Stato("20")
stato2 = Stato("21")

automa1.stati=[stato1, stato2]
automa1.stato_corrente=[stato1]
automa1.stati_iniziali=[stato1]


#creo transizioni tra stati
transizione1 = Transizione("t1")
transizione1.stato_sorgente=stato1
transizione1.stato_destinazione=stato2

transizione2 = Transizione("t2")
transizione2.stato_sorgente=stato2
transizione2.stato_destinazione=stato1

transizione3 = Transizione("t3")
transizione3.stato_sorgente=stato1
transizione3.stato_destinazione=stato1

#automaticamente lo stato verrà popolato con l'array delle transizioni uscenti
stato1.transizioni=[transizione1,transizione3]
stato2.transizioni=[transizione2]


# tran=[]
# tran=get_transizioni(automa1)
# print(transizioni_to_string(tran))
#
# for t in tran:
#     print(t.to_string())

#le transizioni vengono arricchiete da osservazione, rilevanza e eventi
transizione1.osservazione="o1"
transizione1.rilevanza="r1"

transizione2.osservazione="o2"

transizione3.rilevanza="r3"

print('Automa')
automa1.stampa()

print("grafico")
#stampa_automa(automa1)

#stampa_automa_su_file(automa1,"automa1")



