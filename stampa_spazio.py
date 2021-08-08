import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


nome="algoritmo 1 (non ricorsivo)"
file="Output/Test memoria/"+nome+".txt"
out="Output/Test memoria/"+nome+".png"

# data = pd.read_csv(file, delimiter="\n")
# print(data)



data = [['spazio 1', 245815.59], ['spazio 2', 315996.92], ['spazio 3', 1608562.43], ['spazio 4', 630016.78], ['spazio 5', 1262122.44]]
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
plt.title("Creazione spazio da rete (non ricorsivo)")
plt.xlabel('Creazione spazi')
plt.ylabel('Memoria byte')
plt.savefig(out)
plt.show()
#
# print("Media: "+str(media))
