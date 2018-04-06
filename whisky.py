import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
whisky = pd.read_csv("whiskies.txt")
whisky["Region"] = pd.read_csv("regions.txt")
# to view data in a panda dataframe
#whisky.iloc[0:5]
flavors = whisky.iloc[:,2:14]

#pearson correlation
corr_flavors = pd.DataFrame.corr(flavors)

plt.figure(figsize=(10,10))
plt.pcolor(corr_flavors)
plt.colorbar()
plt.savefig("corr_flavors.pdf")

corr_whisky = pd.DataFrame.corr(flavors.transpose())

plt.figure(figsize=(10,10))
plt.pcolor(corr_whisky)
plt.axis("tight")
plt.colorbar()
plt.savefig("corr_whisky.pdf")

#spectral co-cluster
from sklearn.cluster.bicluster import SpectralCoclustering
model = SpectralCoclustering(n_clusters=6,random_state=0)
model.fit(corr_whisky)
#print(model.rows_)
np.sum(model.rows_, axis=1)
model.row_labels_

#comparing correlation matrices

whisky['Group'] = pd.Series(model.row_labels_, index = whisky.index)

whisky = whisky.ix[np.argsort(model.row_labels_)]
#instead of .ix u can use .iloc or .loc -- see the doc for further clarification

whisky = whisky.reset_index(drop=True)
correlations = pd.DataFrame.corr(whisky.iloc[:,2:14].transpose())
correlations = np.array(correlations)

plt.figure(figsize=(14,7))
plt.subplot(121)
plt.pcolor(corr_whisky)
plt.title('Original')
plt.axis("tight")
plt.subplot(122)
plt.pcolor(correlations)
plt.title("Rearranged")
plt.axis("tight")
plt.savefig("Correlations.pdf")



