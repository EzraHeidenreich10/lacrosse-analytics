import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Gather data from file
data = pd.read_csv('heatmap_test_data.csv')

# Label rows/columns
row_labels = ['Top', 'Mid', 'Bottom']
col_labels = ['L', 'Mid', 'R']

# Create the heatmap
sns.heatmap(data, vmin=0, vmax=50, cmap='Blues', cbar=True, yticklabels=row_labels, xticklabels=col_labels, annot=True)

# Show heatmap
plt.show()
    