# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import challenge
from tqdm.auto import tqdm

show_levels = [999, 1999, 2999]
level_count = max(show_levels) + 1
count = 40000

sns.set_theme()
data = pd.read_csv('expert.tsv', sep='\t')
data2 = pd.read_csv('expert_removed.tsv', sep='\t')
data['Starting Lives'] = 96
data = pd.concat([data, data2], ignore_index=True)
sample_size = data.shape[0]

# for lives [min ... 0 1 2 3]
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
    p = base * (remainings['Lives'] == i).sum() / remainings.shape[0]
    sample_probabilities[-4 + i] = p
    base -= p
sample_probabilities[-1] = base

# %%

fig, ax = plt.subplots()
fig.suptitle("Panga's Life Change After Beating a Level", fontsize=18)
fg = sns.barplot(x=[i for i in range(data['Lives'].min(), 4)], y=sample_probabilities, color=sns.color_palette()[0], ax=ax)
ax.xaxis.set_major_locator(mtick.MultipleLocator(1))
# ax.set_xlim(data['Lives'].min() - 0.5, data['Lives'].max() + 0.5)

# add annotations
for c in ax.containers:

    # custom label calculates percent and add an empty string so 0 value bars don't have a number
    labels = [f'{w * 100:0.1f}%' if (w := v.get_height()) > 0 else '' for v in c]

    ax.bar_label(c, labels=labels, label_type='edge', fontsize=12, rotation=90, padding=2)

ax.margins(y=0.2)
    
fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

def cal_cdf(_, params=None, state=None):
    if params is None:
        return challenge.level_survivial_prob(sample_probabilities, level_count)[1]
    resample = state.multinomial(sample_size, sample_probabilities) / sample_size
    return challenge.level_survivial_prob(resample, level_count)[1]

survivals = cal_cdf(None)

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

multinomial = np.zeros((count, len(show_levels)))
rng = np.random.default_rng(0)
for i in tqdm(range(count)):
    resample = rng.multinomial(sample_size, sample_probabilities) / sample_size
    multinomial[i] = challenge.level_survivial_prob(resample, level_count)[1][show_levels]

def resample_data(data):
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

resamples = np.zeros((count, len(show_levels)))
rng = np.random.RandomState(0)
for i in tqdm(range(count)):
    resample = resample_data(data.sample(sample_size, random_state=rng, replace=True))
    resamples[i] = challenge.level_survivial_prob(resample, level_count)[1][show_levels]

# %%

censored = np.zeros((count, len(show_levels)))
rng = np.random.default_rng(0)
for i in tqdm(range(count)):
    resample = rng.multinomial(sample_size, sample_probabilities)
    resample = np.repeat(range(4 - sample_probabilities.shape[0], 4), resample)
    rng.shuffle(resample)
    
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
    resample = resample_data(resample_df)
    censored[i] = challenge.level_survivial_prob(resample, level_count)[1][show_levels]

# %%

def dkw_confidence_band(F, n, alpha):
    epsilon = np.sqrt(np.log(2./alpha) / (2 * n))
    lower = np.clip(F - epsilon, 0, 1)
    upper = np.clip(F + epsilon, 0, 1)
    return lower, upper

for l in range(len(show_levels)):
    show_level = show_levels[l]
    fig, ax = plt.subplots()
    fig.suptitle(f'Cumulative Distribution Functions of Sample Probability of Panga Beating {show_level + 1} Levels', fontsize=18)
    ax.set_xlabel('Sample Probability of Success')
    ax.set_ylabel('Proportion')
    groups = [('Original', np.sort(censored[:, l])),
              ('Multinomial', np.sort(multinomial[:, l])),
              ('Simple Resampling', np.sort(resamples[:, l]))]
    for g in range(len(groups)):
        method, x = groups[g]
        y = np.arange(1, x.shape[0] + 1) / x.shape[0]
        ax.step(x, y, where='post', color=sns.color_palette()[g], label=method)
        lower, upper = dkw_confidence_band(y, x.shape[0], 0.01)
        ax.fill_between(x, lower, upper, color=sns.color_palette()[g], alpha=0.3)
    ax.fill_between([], [], [], color='grey', alpha=0.3, label='99% CI')
    ax.legend()
    fig.set_size_inches(10, 5)
    plt.tight_layout()
    fig.savefig(f'beat_{show_level + 1}_cdf.png')
    fig.savefig(f'beat_{show_level + 1}_cdf_2x.png', dpi=200)
