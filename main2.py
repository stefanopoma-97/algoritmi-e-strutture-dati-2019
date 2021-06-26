from Classi.Automa.automa import *

stato_1 = Stato('stato1')
print(stato_1.to_string())
stato_2 = Stato('stato1')

stati = [stato_1, stato_2]

s = [x for x in stati if x.nome == "stato1"][0]

print("S")
print(s.to_string())

stato_1.nome="stato1_aggiornato"
print("S_modifica")
print(s.to_string())

