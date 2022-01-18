# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

sns.set_theme()
data = pd.read_csv('expert_removed.tsv', sep='\t')

# %%

%matplotlib widget

fig, ax = plt.subplots()
fig.suptitle("Panga's Life Change After Beating a Level", fontsize=18)
sns.histplot(data, x='Lives', hue='Current Lives', discrete=True, multiple='dodge', ax=ax)
ax.xaxis.set_major_locator(mtick.MultipleLocator(1))
ax.set_xlim(data['Lives'].min() - 0.5, data['Lives'].max() + 0.5)

for rect in ax.patches:
    x = rect.get_x() + rect.get_width() / 2.
    y = rect.get_height()
    ax.annotate(f"{y:.0f}", (x, y), ha='center', va='bottom', clip_on=True)
    
# fig.set_size_inches(10, 5)
plt.tight_layout()