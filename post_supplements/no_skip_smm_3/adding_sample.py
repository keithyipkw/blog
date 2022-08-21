# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import challenge

sns.set_theme()
data = pd.read_csv('expert.tsv', sep='\t')[['Starting Lives', 'Lives']]
level_count = 3000

sample_probabilities = challenge.life_change_prob(data)
baseline = challenge.level_survivial_prob(sample_probabilities, level_count)[1]

comparands = np.zeros((103, level_count))
data = data.append({'Starting Lives': 96, 'Lives': 0}, ignore_index=True)
for i in range(comparands.shape[0]):
    data.at[data.shape[0] - 1, 'Lives'] = i - 99
    comparing_probabilities = challenge.life_change_prob(data)
    comparands[i] = challenge.level_survivial_prob(comparing_probabilities, level_count)[1]

%matplotlib widget

# %%

x = np.arange(1, level_count + 1)
dfs = []
lines = []
colors = []
for l in [3, -20, -40, -60, -80, -99]:
    i = l + 99
    label = f'{l}-Life Gain' if l >= 0 else f'{-l}-Life Loss'
    dfs.append(pd.DataFrame({'x': x, 'y': comparands[i], 'label': label}))
    lines.append('')
    colors.append(sns.color_palette()[len(colors) + 1])
dfs.append(pd.DataFrame({'x': x, 'y': baseline, 'label': 'Baseline'}))
lines.append((3, 3))
colors.append(sns.color_palette()[0])
df = pd.concat(dfs, ignore_index=True)

fig, ax = plt.subplots()
fig.suptitle('Panga\'s Success Rates After Adding a Sample', fontsize=18)
g = sns.lineplot(data=df, x='x', y='y', style='label', hue='label', palette=colors, dashes=lines)
g.set(ylabel=None)
g.legend().set_title(None)

ax.set_xlabel('Levels')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
fig.set_size_inches(10, 5)
plt.tight_layout()
ax.set_yscale('log')
ax.set_ylim(0.001, 1.25)
ax.grid(b=True, which='minor', color='w', linewidth=0.5)
def format_y(y, _):
    if y >= 0.01:
        return f'{y * 100:.0f}%'
    else:
        return f'{y * 100:.1g}%'
ax.yaxis.set_major_formatter(mtick.FuncFormatter(format_y))
ax.yaxis.set_major_locator(mtick.LogLocator(10, [0.1, 0.5], 2))
ax.yaxis.set_minor_locator(mtick.LogLocator(10, np.arange(1.0, 10.0) * 0.1, 10))
plt.savefig('pangas_success_rates_adding_1_sample.png')
plt.savefig('pangas_success_rates_adding_1_sample_2x.png', dpi=200)
plt.show(block=False)

# %%

fig, ax = plt.subplots()
level = 1000
fig.suptitle(f'Panga\'s Success Rates of Beating {level} Levels After Adding a Sample', fontsize=18)
sns.lineplot(x=np.arange(-99, 4), y=baseline[level - 1], label='Baseline')
sns.lineplot(x=np.arange(-99, 4), y=comparands[:, level - 1], label='Adding a Sample')
ax.set_xlabel('Life Changes')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
ax.set_ylim(0.095, 0.155)
fig.set_size_inches(10, 5)
plt.tight_layout()
plt.savefig(f'pangas_success_rates_{level}_levels_adding_1_sample.png')
plt.savefig(f'pangas_success_rates_{level}_levels_adding_1_sample_2x.png', dpi=200)
plt.show(block=False)

# %%