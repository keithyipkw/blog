# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
from archbs import IIDBootstrap
import challenge
from tqdm.auto import tqdm
import statsmodels.stats.proportion as proportion

%matplotlib widget

sns.set_theme()
dist = {}
for i in range(-20, -9):
    dist[i] = 1
dist[-10] = 3
dist[-9] = 3
dist[-8] = 3
dist[-7] = 6
dist[-6] = 6
dist[-5] = 12
dist[-4] = 15
dist[-3] = 30
dist[-2] = 63
dist[-1] = 140
dist[0] = 240
dist[1] = 160
dist[2] = 140
dist[3] = 1000 - sum(dist.values())

data = []
for i in dist:
    data.append(np.repeat(i, dist[i]))
data = np.concatenate(data)

# %%

fig, ax = plt.subplots()
fig.suptitle("Example of Life Change After Beating a Level", fontsize=18)
sns.histplot(data, discrete=True, ax=ax)
ax.xaxis.set_major_locator(mtick.MultipleLocator(1))
ax.set_xlim(data.min() - 0.5, data.max() + 0.5)

for rect in ax.patches:
    x = rect.get_x() + rect.get_width() / 2.
    y = rect.get_height()
    ax.annotate(f"{y:.0f}", (x, y), ha='center', va='bottom', clip_on=True)
    
fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

level_count = 1000
resample_size = 10000
ci_sizes = np.linspace(0.01, 0.99, 99)
method = 'percentile'

def cal_cdf(samples):
    return challenge.level_survivial(samples, level_count)[1]

def cal_cis(data):
    bs = IIDBootstrap(data, seed=0)
    cis = np.zeros((level_count, ci_sizes.shape[0] * 2 + 3))
    cis[:, -1] = 1
    with tqdm(total=100) as pbar:
        ci = bs.conf_int(cal_cdf, method=method, size=0.0001, reps=resample_size)
        cis[:, cis.shape[1] // 2] = (ci[0] + ci[1]) / 2
        pbar.update(1)
        for i in range(ci_sizes.shape[0]):
            ci = bs.conf_int(cal_cdf, method=method, size=ci_sizes[i], reps=resample_size, reuse=True)
            ci[0][ci[0] < 0] = 0
            ci[1][ci[1] > 1] = 1
            cis[:, cis.shape[1] // 2 - i - 1] = ci[0]
            cis[:, cis.shape[1] // 2 + i + 1] = ci[1]
            pbar.update(1)
    return cis

def binom_cis(win, loss):
    total = win + loss
    cis = {0.5: win / total}
    cis[0] = 0
    cis[1] = 1
    for alpha in ci_sizes * 100:
        ci = proportion.proportion_confint(win, total, alpha / 100, method='wilson')
        cis[1 - alpha / 200] = ci[1]
        cis[alpha / 200] = ci[0]
    
    return np.array([cis[i] for i in sorted(cis.keys())])

cis1 = cal_cis(data)
cis2 = cal_cis(np.repeat(data, 2))
binom1 = binom_cis(1, 1)
binom2 = binom_cis(2, 2)

# %%

fig, ax = plt.subplots()
ax.set_xlabel('Probability of Success')
ax.set_ylabel('Cumulative Probability')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.yaxis.set_major_locator(mtick.MultipleLocator(0.1))
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.xaxis.set_major_locator(mtick.MultipleLocator(0.1))
ax.set_title('Example CDF of Beating 1000 Levels', size=20)
ys = np.linspace(0, 1, cis1.shape[1])

sns.lineplot(x=cis1[999], y=ys, ax=ax, zorder=2, label='Markov Chain: 1000 samples')
sns.lineplot(x=binom1, y=ys, ax=ax, zorder=2, label='Binomial: 1 win & 1 loss')

# sns.lineplot(x=cis2[999], y=ys, ax=ax, zorder=2, label='Markov Process: 2000 Samples')
# sns.lineplot(x=binom2, y=ys, ax=ax, zorder=2, label='Binomial: 2 Win & 2 Loss')

# ax.hlines(0.025, 0, 1, color=sns.color_palette()[2], label=f'95% CI')
# ax.hlines(0.975, 0, 1, color=sns.color_palette()[2])

ax.legend()
fig.set_size_inches(10, 5)
plt.tight_layout()
# %%
