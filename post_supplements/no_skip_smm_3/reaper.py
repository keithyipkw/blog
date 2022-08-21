# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

sns.set_theme()
data = pd.read_csv('expert.tsv', sep='\t')[['Starting Lives', 'Lives']]
level_count = 3000

# %%

%matplotlib widget

x = np.arange(1, level_count + 1)
prob = data[data['Lives'] == -99].shape[0] / data.shape[0]
y = np.power(1 - prob, x)

fig, ax = plt.subplots()
fig.suptitle('Panga\'s Probabilities of Avoiding Reaper Levels', fontsize=18)
ax.plot(x, y)

ax.set_xlabel('Levels')
ax.set_ylabel('Probability')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
fig.set_size_inches(10, 5)
plt.tight_layout()
ax.yaxis.set_major_locator(mtick.MultipleLocator(0.1))
plt.savefig('pangas_probabilities_avoiding_reaper.png', dpi=100)
plt.savefig('pangas_probabilities_avoiding_reaper_2x.png', dpi=200)
plt.show(block=False)

# %%
