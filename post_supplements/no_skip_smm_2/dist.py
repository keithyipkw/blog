# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

sns.set_theme()
data = pd.read_csv('expert.tsv', sep='\t')
data2 = pd.read_csv('expert_removed.tsv', sep='\t')
data['Starting Lives'] = '< 97'
data = pd.concat([data, data2], ignore_index=True)

# %%

%matplotlib widget

fig, ax = plt.subplots()
fig.suptitle("Panga's Life Change After Beating a Level", fontsize=18)
fg = sns.histplot(data, x='Lives', hue='Starting Lives', hue_order=['< 97', 97, 98, 99], stat='percent', common_norm=False, discrete=True, multiple='dodge', shrink=0.8, ax=ax)
ax.xaxis.set_major_locator(mtick.MultipleLocator(1))
ax.set_xlim(data['Lives'].min() - 0.5, data['Lives'].max() + 0.5)

# for rect in ax.patches:
#     x = rect.get_x() + rect.get_width() / 2.
#     y = rect.get_height()
#     ax.annotate(f"{y:.0f}", (x, y), ha='center', va='bottom', clip_on=True)

    
# add annotations
for c in ax.containers:

    # custom label calculates percent and add an empty string so 0 value bars don't have a number
    labels = [f'{w:0.1f}%' if (w := v.get_height()) > 0 else '' for v in c]

    ax.bar_label(c, labels=labels, label_type='edge', fontsize=4.5, rotation=90, padding=2)

ax.margins(y=0.2)
    
fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

censored = data.copy()
for i in range(3):
    censored.loc[censored['Lives'] == 3 - i, 'Lives'] = 2 - i
    censored.loc[(censored['Starting Lives'] == f'< {96 + i}') | (censored['Starting Lives'] == 96 + i), 'Starting Lives'] = f'< {97 + i}'

    fig, ax = plt.subplots()
    fig.suptitle("Censored Panga's Life Change After Beating a Level", fontsize=18)
    fg = sns.histplot(censored, x='Lives', hue='Starting Lives', hue_order=[f'< {97 + i}', 97 + i], stat='percent', common_norm=False, discrete=True, multiple='dodge', shrink=0.8, ax=ax)
    ax.xaxis.set_major_locator(mtick.MultipleLocator(1))
    ax.set_xlim(data['Lives'].min() - 0.5, data['Lives'].max() + 0.5)

    # add annotations
    for c in ax.containers:

        # custom label calculates percent and add an empty string so 0 value bars don't have a number
        labels = [f'{w:0.1f}%' if (w := v.get_height()) > 0 else '' for v in c]

        ax.bar_label(c, labels=labels, label_type='edge', fontsize=7.5, rotation=90, padding=2)

    ax.margins(y=0.2)
        
    fig.set_size_inches(10, 5)
    plt.tight_layout()

# %%
