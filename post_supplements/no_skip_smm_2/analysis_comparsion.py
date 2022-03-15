# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
from archbs import IIDBootstrap
import challenge
from tqdm.auto import tqdm

sns.set_theme()
data = pd.read_csv('expert.tsv', sep='\t')
data2 = pd.read_csv('expert_removed.tsv', sep='\t')
data['Starting Lives'] = 96
data = pd.concat([data, data2], ignore_index=True)
sample_size = data.shape[0]
min_lives = data['Lives'].min()
level_count = 3000
resample_size = 400000
ci_sizes = np.linspace(0.01, 0.99, 99)

def cal_cdf(data):
    sample_probabilities = np.zeros(4 - data['Lives'].min())
    
    applicables = data[data['Lives'] < 0]
    rate = 1 / data.shape[0]
    lives, counts = np.unique(applicables['Lives'], return_counts=True)
    for l, c in zip(lives, counts):
        sample_probabilities[l - 4] = c * rate

    remainings = data
    base = 1 - applicables.shape[0] / data.shape[0]
    for i in range(3):
        remainings = remainings[(remainings['Lives'] >= i) & (remainings['Starting Lives'] < 99 - i)]
        if remainings.shape[0] == 0:
            base = 0
            break
        p = base * (remainings['Lives'] == i).sum() / remainings.shape[0]
        sample_probabilities[-4 + i] = p
        base -= p
    sample_probabilities[-1] = base
    return challenge.level_survivial_prob(sample_probabilities, level_count)[1]

survivals = cal_cdf(data)

%matplotlib widget

# %%

fig, ax = plt.subplots()
fig.suptitle('Panga Beating Super Mario Marker 2 No-skip Endless Expert Levels', fontsize=18)
ax.set_xlabel('Levels')
ax.set_ylabel('Probability')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
xs = np.arange(1, level_count + 1)
sns.lineplot(x=xs, y=survivals, ax=ax)
ax.set_xlim(0, xs[-1])
fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

all_cis = {}
reuse = False
bs = IIDBootstrap(data, seed=0)
for method in ['bca', 'percentile', 'bc']:
    cis = np.zeros((level_count, ci_sizes.shape[0] * 2 + 3))
    all_cis[method] = cis
    cis[:, -1] = 1
    with tqdm(total=100, desc=method) as pbar:
        ci = bs.conf_int(cal_cdf, method=method, size=0.0001, reps=resample_size, reuse=reuse)
        reuse = True
        cis[:, cis.shape[1] // 2] = (ci[0] + ci[1]) / 2
        pbar.update(1)
        for i in range(ci_sizes.shape[0]):
            ci = bs.conf_int(cal_cdf, method=method, size=ci_sizes[i], reps=resample_size, reuse=reuse)
            ci[0][ci[0] < 0] = 0
            ci[1][ci[1] > 1] = 1
            cis[:, cis.shape[1] // 2 - i - 1] = ci[0]
            cis[:, cis.shape[1] // 2 + i + 1] = ci[1]
            pbar.update(1)

# %%

fig, ax = plt.subplots()
fig.suptitle('Panga Beating Super Mario Marker 2 No-skip Endless Expert Levels', fontsize=18)
ax.set_xlabel('Levels')
ax.set_ylabel('Probability')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
xs = np.arange(1, level_count + 1)
sns.lineplot(x=xs, y=survivals, ax=ax, label='Sample Probability')

for m in range(3):
    method = ['Percentile', 'BC', 'BCa'][m]
    cis = all_cis[method.lower()]
    ax.plot(xs, cis[:, cis.shape[1] // 2 - 95], color=sns.color_palette()[m + 1], linestyle='dashed')
    ax.plot(xs, cis[:, cis.shape[1] // 2 + 95], linestyle='dashed', color=sns.color_palette()[m + 1])
    ax.plot(xs, cis[:, cis.shape[1] // 2 - 99], color=sns.color_palette()[m + 1], label=method)
    ax.plot(xs, cis[:, cis.shape[1] // 2 + 99], color=sns.color_palette()[m + 1])

ax.plot([], color='grey', label='99% CI')
ax.plot([], color='grey', linestyle='dashed', label='95% CI')
ax.set_xlim(0, xs[-1])
ax.legend()
fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

fig, ax = plt.subplots()
ax.set_xlabel('Probability of Success')
ax.set_ylabel('Cumulative Probability')
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
fig.suptitle('Panga Beating 1000 Super Mario Marker 2 No-skip Endless Expert Levels', fontsize=18)
all_ymin = 1
all_ymax = 0
for m in range(3):
    method = ['Percentile', 'BC', 'BCa'][m]
    cis = all_cis[method.lower()]
    ys = np.linspace(0, 1, cis.shape[1])
    sns.lineplot(x=cis[999], y=ys, ax=ax, zorder=2, label=method)
        
ax.legend()
ax.set_xlim(-0.01, 1.01)
ax.set_ylim(-0.01, 1.01)
fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

plt.show()

# %%