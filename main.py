from Classi.Automa.automa import *
from graphviz import Digraph




automa1 = Automa('automa 1')

stato1 = Stato("20")
stato2 = Stato("21")

automa1.stati=[stato1, stato2]
automa1.stato_corrente=[stato1]
automa1.stati_iniziali=[stato1]



transizione1 = transizione("t1")
transizione1.stato_sorgente=stato1
transizione1.stato_destinazione=stato2

transizione2 = transizione("t2")
transizione2.stato_sorgente=stato2
transizione2.stato_destinazione=stato1

transizione3 = transizione("t3")
transizione3.stato_sorgente=stato1
transizione3.stato_destinazione=stato1

stato1.transizioni=[transizione1,transizione3]
stato2.transizioni=[transizione2]


tran=[]
tran=get_transizioni(automa1)
print(transizioni_to_string(tran))

for t in tran:
    print(t.to_string())

print('Automa')
automa1.stampa()





# print("grafico")
# gra = Digraph()
# print("ciclo nomi stati")
# for s in automa1.stati:
#     gra.node(s.nome)
#     print(s.nome)
# print("ciclo transizioni")
# tr=[]
# for t in get_transizioni(automa1):
#     edge= t.stato_sorgente.nome+t.stato_destinazione.nome
#     print(edge)
#     tr+=[edge]
# gra.edges(['20 21'])
# print(tr)
#
# print(gra.source)

gra = Digraph()

gra.node('Gk', label='20')
gra.node('U', label='21')


gra.edges(['GkU'])
print(gra.source)