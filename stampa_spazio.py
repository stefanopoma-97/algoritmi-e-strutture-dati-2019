import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


nome="creazione rete"
file="Output/Test memoria/"+nome+".txt"
out="Output/Test memoria/"+nome+".png"

# data = pd.read_csv(file, delimiter="\n")
# print(data)



data = [['rete 1', 107208.56], ['rete 2', 124570.92], ['rete 3', 113986.58], ['rete 4', 165188.22], ['rete 4', 237808.44]]
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

plt.xlabel('Creazione reti')
plt.ylabel('Memoria Kb')
plt.savefig(out)
plt.show()
#
# print("Media: "+str(media))
