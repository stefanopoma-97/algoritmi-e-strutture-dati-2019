import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


nome="algoritmo 3 (migliorato)"
file="Output/Test memoria/"+nome+".txt"
out="Output/Test memoria/"+nome+".png"

# data = pd.read_csv(file, delimiter="\n")
# print(data)



data = [['spazio 1', 145985.46], ['spazio 2', 141191.1], ['spazio 3', 1424106.23], ['spazio 4', 417443.21], ['spazio 5', 669667.57]]
# Create the pandas DataFrame
df = pd.DataFrame(data, columns=['Rete', 'Kb'])


# Y = data.squeeze()
# X = pd.Series(range(1,100))
#
#
# media=Y.mean()
#
#
fig, ax = plt.subplots()
plt.bar(df['Rete'],height=df['Kb'], color='red')
plt.title("Algoritmo 3 (migliorato)")
plt.xlabel('Creazione spazi')
plt.ylabel('Memoria byte')
plt.savefig(out)
plt.show()
#
# print("Media: "+str(media))
