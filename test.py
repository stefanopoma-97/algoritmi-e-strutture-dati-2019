import gc

import cp as cp

from Classi.GestioneFile.grafici import *
from Classi.Automa.rete import *
from Classi.GestioneFile.input_output import *
from Classi.Spazio.spazio_comportamentale import *
from Classi.Algoritmi.algoritmi_spazio_comportamentale import *
from copy import deepcopy
import timeit
import tracemalloc






#TEMPO

SETUP_RETE1= '''
from Classi.GestioneFile.input_output import carica_automa_da_file_txt
from Classi.GestioneFile.input_output import carica_links_da_file_txt
from Classi.GestioneFile.input_output import carica_rete_da_file_txt
import cp as cp

from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale_migliorato
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale_non_ricorsivo
from Classi.Algoritmi.algoritmi_spazio_comportamentale import istanzio_nodo_iniziale
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2_migliorato

from copy import deepcopy
import gc

a1 = carica_automa_da_file_txt("Input/RETE1/C2.txt")
a2 = carica_automa_da_file_txt("Input/RETE1/C3.txt")
automi = [a1, a2]
links = carica_links_da_file_txt(automi, "Input/RETE1/links.txt")
rete = carica_rete_da_file_txt(automi, links, "Input/RETE1/rete 1.txt")
'''
SETUP_RETE2= '''
from Classi.GestioneFile.input_output import carica_automa_da_file_txt
from Classi.GestioneFile.input_output import carica_links_da_file_txt
from Classi.GestioneFile.input_output import carica_rete_da_file_txt

from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale_migliorato
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2
from Classi.Algoritmi.algoritmi_spazio_comportamentale import istanzio_nodo_iniziale
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale_non_ricorsivo

from copy import deepcopy
import gc

a1 = carica_automa_da_file_txt("Input/RETE2/S.txt")
a2 = carica_automa_da_file_txt("Input/RETE2/B.txt")
automi = [a1, a2]
links = carica_links_da_file_txt(automi, "Input/RETE2/links.txt")
rete = carica_rete_da_file_txt(automi, links, "Input/RETE2/rete 2.txt")
'''
SETUP_RETE3= '''
from Classi.GestioneFile.input_output import carica_automa_da_file_txt
from Classi.GestioneFile.input_output import carica_links_da_file_txt
from Classi.GestioneFile.input_output import carica_rete_da_file_txt
from Classi.GestioneFile.grafici import stampa_spazio_su_file
from Classi.GestioneFile.input_output import salva_spazio_su_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale_migliorato
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale_non_ricorsivo
from Classi.Algoritmi.algoritmi_spazio_comportamentale import istanzio_nodo_iniziale
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2_migliorato

from copy import deepcopy
import gc

a1 = carica_automa_da_file_txt("Input/RETE3/C1.txt")
a2 = carica_automa_da_file_txt("Input/RETE3/C2.txt")
a3 = carica_automa_da_file_txt("Input/RETE3/C3.txt")
automi = [a1, a2, a3]
links = carica_links_da_file_txt(automi, "Input/RETE3/links.txt")
rete = carica_rete_da_file_txt(automi, links, "Input/RETE3/rete 3.txt")
'''
SETUP_RETE4= '''
from Classi.GestioneFile.input_output import carica_automa_da_file_txt
from Classi.GestioneFile.input_output import carica_links_da_file_txt
from Classi.GestioneFile.input_output import carica_rete_da_file_txt

from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale_non_ricorsivo

from copy import deepcopy
import gc

a1 = carica_automa_da_file_txt("Input/RETE4/CANCELLO.txt")
a2 = carica_automa_da_file_txt("Input/RETE4/TELECOMANDO.txt")
automi = [a1, a2]
links = carica_links_da_file_txt(automi, "Input/RETE4/links.txt")
rete = carica_rete_da_file_txt(automi, links, "Input/RETE4/rete 4.txt")
'''
SETUP_RETE5= '''
from Classi.GestioneFile.input_output import carica_automa_da_file_txt
from Classi.GestioneFile.input_output import carica_links_da_file_txt
from Classi.GestioneFile.input_output import carica_rete_da_file_txt

from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale_migliorato
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale_non_ricorsivo
from Classi.Algoritmi.algoritmi_spazio_comportamentale import istanzio_nodo_iniziale
from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2_migliorato

from copy import deepcopy
import gc

a1 = carica_automa_da_file_txt("Input/RETE5/CANCELLO.txt")
a2 = carica_automa_da_file_txt("Input/RETE5/TELECOMANDO.txt")
a3 = carica_automa_da_file_txt("Input/RETE5/PERSONA.txt")
automi = [a1, a2, a3]
links = carica_links_da_file_txt(automi, "Input/RETE5/links.txt")
rete = carica_rete_da_file_txt(automi, links, "Input/RETE5/rete 5.txt")
'''

SETUP_SPAZIO1= '''
from Classi.GestioneFile.input_output import carica_spazio_da_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2_da_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_sistemo_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import potatura
from Classi.Algoritmi.algoritmi_spazio_comportamentale import potatura_migliorato

from copy import deepcopy
import gc

spazio=carica_spazio_da_file("Input/spazio1_salvataggio")
'''
SETUP_SPAZIO2= '''
from Classi.GestioneFile.input_output import carica_spazio_da_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2_da_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_sistemo_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import potatura


from copy import deepcopy
import gc

spazio=carica_spazio_da_file("Input/spazio2_salvataggio")
'''
SETUP_SPAZIO3= '''
from Classi.GestioneFile.input_output import carica_spazio_da_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2_da_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_sistemo_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import potatura
from Classi.Algoritmi.algoritmi_spazio_comportamentale import potatura_migliorato

from copy import deepcopy
import gc

spazio=carica_spazio_da_file("Input/spazio3_salvataggio")
'''
SETUP_SPAZIO4= '''
from Classi.GestioneFile.input_output import carica_spazio_da_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2_da_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_sistemo_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import potatura

from copy import deepcopy
import gc

spazio=carica_spazio_da_file("Input/spazio4_salvataggio")
'''
SETUP_SPAZIO5= '''
from Classi.GestioneFile.input_output import carica_spazio_da_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import crea_spazio_comportamentale2_da_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_sistemo_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import potatura
from Classi.Algoritmi.algoritmi_spazio_comportamentale import potatura_migliorato

from copy import deepcopy
import gc

spazio=carica_spazio_da_file("Input/spazio5_salvataggio")
'''

SETUP_SPAZIO1_OSS= '''
from Classi.GestioneFile.input_output import carica_spazio_da_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_sistemo_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio

from copy import deepcopy
import gc

spazio=carica_spazio_da_file("Input/spazio1_potato_salvataggio_oss")
'''
SETUP_SPAZIO2_OSS= '''
from Classi.GestioneFile.input_output import carica_spazio_da_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_sistemo_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio

from copy import deepcopy
import gc

spazio=carica_spazio_da_file("Input/spazio2_potato_salvataggio_oss")
'''
SETUP_SPAZIO3_OSS= '''
from Classi.GestioneFile.input_output import carica_spazio_da_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_sistemo_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio_migliorato

from copy import deepcopy
import gc

spazio=carica_spazio_da_file("Input/spazio3_potato_salvataggio_oss")
'''
SETUP_SPAZIO4_OSS= '''
from Classi.GestioneFile.input_output import carica_spazio_da_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_sistemo_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio_migliorato

from copy import deepcopy
import gc

#accendoDaChiuso,apri,apertura,aperto,stopDaAperto,spentoAperto,accendoDaAperto,chiudiDaAcceso,chiusura

spazio=carica_spazio_da_file("Input/spazio4_potato_salvataggio_oss")
'''
SETUP_SPAZIO5_OSS= '''
from Classi.GestioneFile.input_output import carica_spazio_da_file

from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_sistemo_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio
from Classi.Algoritmi.algoritmi_spazio_comportamentale import diagnosi_algoritmo_su_spazio_migliorato

from copy import deepcopy
import gc

#accendoDaChiuso,apri,apertura,aperto,stopDaAperto,spentoAperto,accendoDaAperto,chiudiDaAcceso,chiusura,chiuso,stopDaChiuso

spazio=carica_spazio_da_file("Input/spazio5_potato_salvataggio_oss")
'''

TEST_RETE_ALGORITMO1='''
gc.disable()
spazio = crea_spazio_comportamentale(rete)

'''
TEST_RETE_ALGORITMO1_MIGLIORATO='''
gc.disable()
spazio = crea_spazio_comportamentale_migliorato(rete)

'''
TEST_RETE_ALGORITMO1_NON_RICORSIVO='''

spazio = crea_spazio_comportamentale_non_ricorsivo(rete)

'''
TEST_RETE_ALGORITMO1_NON_RICORSIVO_STAMPA='''

spazio = crea_spazio_comportamentale_non_ricorsivo(rete)
stampa_spazio_su_file(spazio,"Output")

'''
TEST_RETE_ALGORITMO1_NON_RICORSIVO_SALVA='''

spazio = crea_spazio_comportamentale_non_ricorsivo(rete)
salva_spazio_su_file(spazio,"Output")

'''
TEST_RETE1_ALGORITMO2='''
spazio = crea_spazio_comportamentale2(rete, ["o3","o2"])

'''
TEST_RETE2_ALGORITMO2='''
spazio = crea_spazio_comportamentale2(rete2, ["act","sby","nop"])
del a1
del a2
del automi
del links
del rete2
del spazio
gc.collect(generation=2)
'''
TEST_RETE3_ALGORITMO2='''
spazio = crea_spazio_comportamentale2(rete, ["o1","o2"])

'''
TEST_RETE4_ALGORITMO2='''
spazio = crea_spazio_comportamentale2(rete4, ["accendoDaChiuso","apri","apertura","aperto","stopDaAperto","spento aperto","accendoDaAperto","chiudiDaAcceso","chiusura"])

del a1
del a2
del automi
del links
del rete4
del spazio
gc.collect(generation=2)
'''
TEST_RETE5_ALGORITMO2='''
spazio = crea_spazio_comportamentale2(rete5, ["accendoDaChiuso","apri","apertura","aperto","stopDaAperto","spento aperto","accendoDaAperto","chiudiDaAcceso","chiusura","chiuso","stopDaChiuso"])
del a1
del a2
del a3
del automi
del links
del rete5
del spazio
gc.collect(generation=2)
'''
TEST_RETE5_ALGORITMO2_MIGLIORATO='''
spazio = crea_spazio_comportamentale2_migliorato(rete, ["accendoDaChiuso","apri","apertura","aperto","stopDaAperto","spento aperto","accendoDaAperto","chiudiDaAcceso","chiusura","chiuso","stopDaChiuso"])

'''
TEST_RETE3_ALGORITMO2_MIGLIORATO='''
spazio = crea_spazio_comportamentale2_migliorato(rete, ["o1","o2"])

'''
TEST_SPAZIO1_ALGORITMO2='''
spazio = crea_spazio_comportamentale2_da_spazio(spazio1, ["o3","o2"])
del spazio1
del spazio
gc.collect(generation=2)
'''
TEST_SPAZIO2_ALGORITMO2='''
spazio = crea_spazio_comportamentale2_da_spazio(spazio2, ["act","sby","nop"])
del spazio2
del spazio
gc.collect(generation=2)
'''
TEST_SPAZIO3_ALGORITMO2='''
spazio = crea_spazio_comportamentale2_da_spazio(spazio, ["o1","o2"])
'''
TEST_SPAZIO4_ALGORITMO2='''
spazio = crea_spazio_comportamentale2_da_spazio(spazio, ["accendoDaChiuso","apri","apertura","aperto","stopDaAperto","spento aperto","accendoDaAperto","chiudiDaAcceso","chiusura"])
'''
TEST_SPAZIO5_ALGORITMO2='''
spazio = crea_spazio_comportamentale2_da_spazio(spazio, ["accendoDaChiuso","apri","apertura","aperto","stopDaAperto","spento aperto","accendoDaAperto","chiudiDaAcceso","chiusura","chiuso","stopDaChiuso"])
'''
TEST_SPAZIO1_ALGORITMO3='''
diagnosi_sistemo_spazio(spazio)
diagnosi_algoritmo_su_spazio(spazio)
del spazio
gc.collect(generation=2)
'''
TEST_SPAZIO2_ALGORITMO3='''
diagnosi_sistemo_spazio(spazio)
diagnosi_algoritmo_su_spazio(spazio)
del spazio
gc.collect(generation=2)
'''
TEST_SPAZIO3_ALGORITMO3='''
diagnosi_sistemo_spazio(spazio)
diagnosi_algoritmo_su_spazio(spazio)
del spazio
gc.collect(generation=2)
'''
TEST_SPAZIO3_MIGLIORATO_ALGORITMO3='''
diagnosi_sistemo_spazio(spazio)
diagnosi_algoritmo_su_spazio_migliorato(spazio)
del spazio
gc.collect(generation=2)
'''
TEST_SPAZIO4_ALGORITMO3='''
diagnosi_sistemo_spazio(spazio)
diagnosi_algoritmo_su_spazio(spazio)
del spazio
gc.collect(generation=2)
'''
TEST_SPAZIO5_ALGORITMO3='''
diagnosi_sistemo_spazio(spazio)
diagnosi_algoritmo_su_spazio(spazio)
del spazio
gc.collect(generation=2)
'''
TEST_SPAZIO5_MIGLIORATO_ALGORITMO3='''
diagnosi_sistemo_spazio(spazio)
diagnosi_algoritmo_su_spazio_migliorato(spazio)
del spazio
gc.collect(generation=2)
'''
TEST_POTATURA='''
potatura(spazio.nodi_finali)
del spazio
gc.collect(generation=2)
'''
TEST_POTATURA_MIGLIORATO='''
potatura_migliorato(spazio.nodi_finali)
del spazio
gc.collect(generation=2)
'''


dates = timeit.repeat(setup=SETUP_RETE3, stmt=TEST_RETE_ALGORITMO1_NON_RICORSIVO_SALVA, repeat=200, number=1)

print("FINITO ESECUZIONE")
out = open("Output/Test tempo/algoritmo1 rete 3 - salva.txt", "w")

for d in dates:
    out.write(str(d)+"\n")
out.close()



