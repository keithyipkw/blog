# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import ListedColormap
import colour
import pandas as pd
from archbs import IIDBootstrap
import challenge
from tqdm.auto import tqdm

level_count = 3000
resample_size = 40000
ci_sizes = np.linspace(0.01, 0.99, 99)
method = 'bca'

sns.set_theme()
data = pd.read_csv('expert.tsv', sep='\t')

def cal_cdf(samples):
    return challenge.level_survivial(samples, level_count)[1]

survivals = cal_cdf(data['Lives'])

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

bs = IIDBootstrap(data['Lives'], seed=0)
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

# %%

for i in [1000, 2000, 3000]:
    ci_str = []
    for ci in [95, 99]:
        low = cis[i - 1, cis.shape[1] // 2 - ci] * 100
        high = cis[i - 1, cis.shape[1] // 2 + ci] * 100
        ci_str.append(f'{ci}% CI [{low:.3g}%, {high:.3g}%]')
    print(f'{i}: {survivals[i - 1] * 100:.3g}%, {", ".join(ci_str)}')

# %%

fig, ax = plt.subplots()
fig.suptitle('Panga Beating Super Mario Marker 2 No-skip Endless Expert Levels', fontsize=18)
ax.set_xlabel('Levels')
ax.set_ylabel('Probability')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
xs = np.arange(1, level_count + 1)
sns.lineplot(x=xs, y=survivals, ax=ax)
for i in range(cis.shape[1] - 1):
    if i == 0:
        alpha = 0
    elif i == cis.shape[1] // 2:
        alpha = 1
    elif i < cis.shape[1] // 2:
        alpha = ci_sizes[i - 1]
    else:
        alpha = ci_sizes[ci_sizes.shape[0] - i + 1]
    ax.fill_between(xs, cis[:, i], cis[:, i + 1], color=sns.color_palette()[0], linewidth=0, alpha=alpha)
ax.set_xlim(0, xs[-1])
fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

x = np.repeat(np.arange(cis.shape[0])[..., np.newaxis], cis.shape[1], -1).ravel()

y = cis.ravel()

base = np.array([0, cis.shape[1], 1, cis.shape[1], cis.shape[1] + 1, 1])
offset = (np.repeat(np.arange(cis.shape[0] - 1)[..., np.newaxis], cis.shape[1] - 1, 1) * cis.shape[1] + np.arange(cis.shape[1] - 1)).ravel()
triangle = (base[np.newaxis, ...] + offset[..., np.newaxis]).reshape(-1, 3)

z = np.concatenate(([0], ci_sizes))
z = np.concatenate((z, [1], np.flip(z)))
z = np.repeat(z[np.newaxis, ...], cis.shape[0], 0).ravel()

fig, ax = plt.subplots()

CAM16UCS = colour.convert([sns.color_palette()[0], ax.get_facecolor()[:3]], 'Output-Referred RGB', 'CAM16UCS')
gradient = colour.utilities.lerp(
    CAM16UCS[0][np.newaxis],
    CAM16UCS[1][np.newaxis],
    np.linspace(0, 1, ci_sizes.shape[0])[..., np.newaxis])
RGB = colour.convert(gradient, 'CAM16UCS', 'Output-Referred RGB')

cmap = ListedColormap(RGB)

fig.suptitle('Panga Beating Super Mario Marker 2 No-skip Endless Expert Levels', fontsize=18)
ax.set_xlabel('Levels')
ax.set_ylabel('Probability')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

cs = ax.tricontourf(x, y, triangle, 1 - z, 101, cmap=cmap, vmin=0, vmax=1)
cbar = fig.colorbar(cs, ticks=np.linspace(0, 1, 11), pad=0.02)
cbar.set_ticklabels([f'{i:.0%}' for i in np.linspace(0, 1, 11)])
cbar.ax.set_ylabel('Confidence Interval')

fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

fig, ax = plt.subplots()
fig.suptitle('Panga Beating Super Mario Marker 2 No-skip Endless Expert Levels', fontsize=18)
ax.set_xlabel('Levels')
ax.set_ylabel('Probability')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
xs = np.arange(1, level_count + 1)
sns.lineplot(x=xs, y=survivals, ax=ax, label='Sample Probability')

ax.fill_between(xs, cis[:, cis.shape[1] // 2 - 95], cis[:, cis.shape[1] // 2 + 95], color=sns.color_palette()[0], linewidth=0, alpha=0.2, label='95% CI')

ax.fill_between(xs, cis[:, cis.shape[1] // 2 - 99], cis[:, cis.shape[1] // 2 - 95], color=sns.color_palette()[0], linewidth=0, alpha=0.1, label='99% CI')
ax.fill_between(xs, cis[:, cis.shape[1] // 2 + 99], cis[:, cis.shape[1] // 2 + 95], color=sns.color_palette()[0], linewidth=0, alpha=0.1)

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
ys = np.linspace(0, 1, cis.shape[1])
sns.lineplot(x=cis[999], y=ys, ax=ax, zorder=2, label='CDF')
xmin, xmax = ax.get_xlim()
ymin, ymax = ax.get_ylim()
x = survivals[999]
y = np.interp(x, cis[999], ys)
ax.plot(x, y, color=sns.color_palette()[1], marker='x', markersize=10, linewidth=0, label='Sample Probability')

for i in range(2):
    ci = [95, 99][i]
    low = cis[999, cis.shape[1] // 2 - ci]
    high = cis[999, cis.shape[1] // 2 + ci]
    ax.vlines(low, -2, 2, color=sns.color_palette()[2 + i], label=f'{ci}% CI')
    ax.vlines(high, -2, 2, color=sns.color_palette()[2 + i])
    
# for i in range(2):
#     ci = [95, 99][i]
#     half = (100 - ci) / 200
#     ax.hlines(half, -2, 2, color=sns.color_palette()[2 + i], label=f'{ci}% CI')
#     ax.hlines(1 - half, -2, 2, color=sns.color_palette()[2 + i])

# for i in range(2):
#     ci = [95, 99][i]
#     low = cis[999, cis.shape[1] // 2 - ci]
#     high = cis[999, cis.shape[1] // 2 + ci]
#     half = (100 - ci) / 200
    
#     ax.plot(low, half, color=sns.color_palette()[2 + i], marker='x', markersize=10, linewidth=0, label=f'{ci}% CI')
#     ax.plot(high, 1 - half, color=sns.color_palette()[2 + i], marker='x', markersize=10, linewidth=0)
    
ax.legend()
ax.set_xlim(-0.01, 1)
ax.set_ylim(ymin, ymax)
fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

fig, ax = plt.subplots()
ax.set_xlabel('Probability of Success')
ax.set_ylabel('Probability Density Function')
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
fig.suptitle('Panga Beating 1000 Super Mario Marker 2 No-skip Endless Expert Levels', fontsize=18)
sns.lineplot(x=cis[999], y=1 / (cis.shape[1] - 1) / np.diff(np.concatenate((cis[999], [0]))), ax=ax)
fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

fig, ax = plt.subplots()
fig.suptitle('Panga Beating 1000 Super Mario Marker 2 No-skip Endless Expert Levels', fontsize=18)
z = np.concatenate(([0], ci_sizes))
z = np.concatenate((z, [1], np.flip(z)))
sns.lineplot(x=cis[999], y=1 - z, ax=ax, zorder=2, label='Confidence Interval')
xmin, xmax = ax.get_xlim()
ymin, ymax = ax.get_ylim()

x = survivals[999]
y = abs(np.interp(x, cis[999], ys) - 0.5) * 2
ax.plot(x, y, color=sns.color_palette()[1], marker='x', markersize=10, linewidth=0, label='Sample Probability')

for i in range(2):
    ci = [95, 99][i]
    # line = ['solid', (0, (5, 5))][i]
    line = 'solid'
    low = cis[999, cis.shape[1] // 2 - ci]
    high = cis[999, cis.shape[1] // 2 + ci]
    ax.vlines(low, -2, 2, color=sns.color_palette()[2 + i], linestyles=line, label=f'{ci}% CI')
    ax.vlines(high, -2, 2, color=sns.color_palette()[2 + i], linestyles=line)

# for i in range(2):
#     ci = [95, 99][i]
#     ax.hlines(ci / 100, -2, 2, color=sns.color_palette()[2 + i], label=f'{ci}% CI')

# for i in range(2):
#     ci = [95, 99][i]
#     low = cis[999, cis.shape[1] // 2 - ci]
#     high = cis[999, cis.shape[1] // 2 + ci]
    
#     ax.plot(low, ci / 100, color=sns.color_palette()[2 + i], marker='x', markersize=10, linewidth=0, label=f'{ci}% CI')
#     ax.plot(high, ci / 100, color=sns.color_palette()[2 + i], marker='x', markersize=10, linewidth=0)
    
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.set_xlabel('Probability')
ax.set_ylabel('Confidence Interval')
ax.legend()
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

plt.show()

# %%