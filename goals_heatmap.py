import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv('heatmap_test_data.csv')

row_labels = ['Top', 'Mid', 'Bottom']
col_labels = ['L', 'Mid', 'R']

sns.heatmap(data, vmin=0, vmax=50, cmap='Reds', cbar=True, yticklabels=row_labels, xticklabels=col_labels)

plt.show()
    