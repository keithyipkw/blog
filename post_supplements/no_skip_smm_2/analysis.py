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
method = 'bc'

def life_change_prob(data):
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
    return sample_probabilities

sample_probabilities = life_change_prob(data)
survivals = challenge.level_survivial_prob(sample_probabilities, level_count)[1]

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
fig.savefig('pangas_sample_success_rates.png')
fig.savefig('pangas_sample_success_rates_2x.png', dpi=200)

# %%

def prob_para(_, params=None, state=None):
    if params is None:
        return challenge.level_survivial_prob(sample_probabilities, level_count)[1]
    
    resample = state.multinomial(sample_size, sample_probabilities)
    resample = np.repeat(range(4 - sample_probabilities.shape[0], 4), resample)
    state.shuffle(resample)
    
    starting_lives = np.zeros(resample.shape, np.int32)
    starting_lives[0] = 15
    for j in range(sample_size - 1):
        lives = min(99, starting_lives[j] + resample[j])
        if lives <= 0:
            lives = 15
        starting_lives[j + 1] = lives
    resample = np.minimum(99 - starting_lives, resample)
    resample_df = pd.DataFrame({
        'Starting Lives': starting_lives,
        'Lives': resample,
    })
    resample = life_change_prob(resample_df)
    return challenge.level_survivial_prob(resample, level_count)[1]
    
bs = IIDBootstrap(np.zeros(0), seed=0)
cis = np.zeros((level_count, ci_sizes.shape[0] * 2 + 3))
cis[:, -1] = 1
with tqdm(total=100, desc='CI') as pbar:
    ci = bs.conf_int(prob_para, method=method, size=0.0001, sampling='parametric', reps=resample_size)
    cis[:, cis.shape[1] // 2] = (ci[0] + ci[1]) / 2
    pbar.update(1)
    for i in range(ci_sizes.shape[0]):
        ci = bs.conf_int(prob_para, method=method, size=ci_sizes[i], sampling='parametric', reps=resample_size, reuse=True)
        ci[0][ci[0] < 0] = 0
        ci[1][ci[1] > 1] = 1
        cis[:, cis.shape[1] // 2 - i - 1] = ci[0]
        cis[:, cis.shape[1] // 2 + i + 1] = ci[1]
        pbar.update(1)

# %%

with open(f'{resample_size}.txt', 'a') as f:
    for i in [1000, 2000, 3000]:
        ci_str = []
        for ci in [95, 99]:
            low = cis[i - 1, cis.shape[1] // 2 - ci] * 100
            high = cis[i - 1, cis.shape[1] // 2 + ci] * 100
            ci_str.append(f'{ci}% CI [{low:.3g}%, {high:.3g}%]')
        line = f'{i}: {survivals[i - 1] * 100:.3g}%, {", ".join(ci_str)}'
        print(line)
        f.write(line + '\n')

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
ax.yaxis.set_major_locator(mtick.MultipleLocator(base=0.1))

cs = ax.tricontourf(x, y, triangle, 1 - z, 101, cmap=cmap, vmin=0, vmax=1)
cbar = fig.colorbar(cs, ticks=np.linspace(0, 1, 11), pad=0.02)
cbar.set_ticklabels([f'{i:.0%}' for i in np.linspace(0, 1, 11)])
cbar.ax.set_ylabel('Confidence Interval')

fig.set_size_inches(10, 5)
plt.tight_layout()
fig.savefig('pangas_probabilities.png')
fig.savefig('pangas_probabilities_2x.png', dpi=200)

# %%

fig, ax = plt.subplots()
fig.suptitle('Panga Beating Super Mario Marker 2 No-skip Endless Expert Levels', fontsize=18)
ax.set_xlabel('Levels')
ax.set_ylabel('Probability')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.yaxis.set_major_locator(mtick.MultipleLocator(base=0.1))
xs = np.arange(1, level_count + 1)
sns.lineplot(x=xs, y=survivals, ax=ax, label='Sample Probability')

ax.fill_between(xs, cis[:, cis.shape[1] // 2 - 95], cis[:, cis.shape[1] // 2 + 95], color=sns.color_palette()[0], linewidth=0, alpha=0.2, label='95% CI')

ax.fill_between(xs, cis[:, cis.shape[1] // 2 - 99], cis[:, cis.shape[1] // 2 - 95], color=sns.color_palette()[0], linewidth=0, alpha=0.1, label='99% CI')
ax.fill_between(xs, cis[:, cis.shape[1] // 2 + 99], cis[:, cis.shape[1] // 2 + 95], color=sns.color_palette()[0], linewidth=0, alpha=0.1)

ax.set_xlim(0, xs[-1])
ax.legend()
fig.set_size_inches(10, 5)
plt.tight_layout()
fig.savefig('pangas_probabilities_simplified.png')
fig.savefig('pangas_probabilities_simplified_2x.png', dpi=200)

# %%

fig, ax = plt.subplots()
ax.set_xlabel('Probability of Success')
ax.set_ylabel('Cumulative Probability')
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.xaxis.set_major_locator(mtick.MultipleLocator(base=0.1))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.yaxis.set_major_locator(mtick.MultipleLocator(base=0.1))
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
fig.savefig('pangas_cdf_1000.png')
fig.savefig('pangas_cdf_1000_2x.png', dpi=200)

# %%

fig, ax = plt.subplots()
ax.set_xlabel('Probability of Success')
ax.set_ylabel('Probability Density Function')
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.xaxis.set_major_locator(mtick.MultipleLocator(base=0.1))
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
ax.xaxis.set_major_locator(mtick.MultipleLocator(base=0.1))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.yaxis.set_major_locator(mtick.MultipleLocator(base=0.1))
ax.set_xlabel('Probability')
ax.set_ylabel('Confidence Interval')
ax.legend()
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
fig.set_size_inches(10, 5)
plt.tight_layout()
fig.savefig('pangas_probability_1000.png')
fig.savefig('pangas_probability_1000_2x.png', dpi=200)

# %%

plt.show()

# %%