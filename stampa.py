import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

nome="algoritmo 1 rete 1 (non ricorsivo)"
file="Output/Test memoria/"+nome+".txt"
out="Output/Test memoria/"+nome+".png"

data= pd.read_csv(file, delimiter="\n")
Y = data.squeeze()
X = pd.Series(range(1,200))
media=Y.mean()


plt.bar(X, Y)

plt.xlabel('Iterazioni')
plt.ylabel('Tempi (s)')
plt.title(nome)
plt.savefig(out)
plt.show()

print("Media: "+str(Y.mean()))




