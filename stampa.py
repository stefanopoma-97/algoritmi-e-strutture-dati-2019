import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

nome="algoritmo2(rete) rete 3 Nuova ridenominazione"
file="Output/Test tempo/"+nome+".txt"
out="Output/Test tempo/"+nome+".png"

data= pd.read_csv(file, delimiter="\n")
Y = data.squeeze()
X = pd.Series(range(1,200))
media=Y.mean()


plt.bar(X, Y)

plt.xlabel('Iterazioni')
plt.ylabel('Tempi (s)')
plt.title(nome+" - Media: "+str(media)+"s")
plt.savefig(out)
plt.show()

print("Media: "+str(Y.mean()))




