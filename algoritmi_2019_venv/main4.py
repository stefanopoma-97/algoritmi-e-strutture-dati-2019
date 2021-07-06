from copy import deepcopy
from Classi.Automa.automa import *

stato1 = Stato("nome1")
stato2 = deepcopy(stato1)
stato2.nome="nome 2"

print(stato1.to_string())
print(stato2.to_string())