# %%
import numpy as np
import scipy
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import statsmodels.api as sm
from tqdm.auto import tqdm

level_count = 3000

sns.set_theme()
data = pd.read_csv('expert.tsv', sep='\t')
data2 = pd.read_csv('expert_removed.tsv', sep='\t')
data['Starting Lives'] = 96
data = pd.concat([data, data2], ignore_index=True)
sample_size = data.shape[0]

# for lives [min ... 0 1 2 3]
sample_probabilities = np.zeros(4 - data['Lives'].min())
min_lives = data['Lives'].min()

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
def resample_data(data):
    sample_probabilities = np.zeros(4 - min_lives)
    
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

values = np.arange(4 - sample_probabilities.shape[0], 4)
count = 1000000
resamples = np.zeros((count, sample_probabilities.shape[0]))
for i in tqdm(range(count)):
    a = resample_data(data.sample(frac=1, replace=True, random_state=i))
    resamples[i] = a

multi = scipy.stats.binom.cdf(np.arange(1, sample_size + 1)[:, None], sample_size, sample_probabilities)

censored = np.zeros((count, sample_probabilities.shape[0]))
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
    censored[i] = resample_data(resample_df)

print(resamples.mean(axis=0))
print(resamples.std(axis=0))
print()
print(multi.mean(axis=0))
print(multi.std(axis=0))
print()
print(censored.mean(axis=0))
print(censored.std(axis=0))

# %%

%matplotlib widget

def dkw_confidence_band(F, n, alpha):
    epsilon = np.sqrt(np.log(2./alpha) / (2 * n))
    lower = np.clip(F - epsilon, 0, 1)
    upper = np.clip(F + epsilon, 0, 1)
    return lower, upper

for i in range(sample_probabilities.shape[0] - 5, sample_probabilities.shape[0]):
    life_change = i - sample_probabilities.shape[0] + 4
    fig, ax = plt.subplots()
    if life_change < 0:
        fig.suptitle(f'Cumulative Distribution Functions of Sample Probability of {-life_change} Life Loss', fontsize=18)
        ax.set_xlabel(f'Sample Probability of {-life_change} Life Loss')
    else:
        fig.suptitle(f'Cumulative Distribution Functions of Sample Probability of {life_change} Life Gain', fontsize=18)
        ax.set_xlabel(f'Sample Probability of {life_change} Life Gain')
    ax.set_ylabel('Proportion')
    groups = [('Original', np.sort(censored[:, i]), None, True),
              ('Multinomial', None, multi[:, i], False),
              ('Simple Resampling', np.sort(resamples[:, i]), None, True)]
    for g in range(len(groups)):
        method, x, y, ci = groups[g]
        if x is None:
            x = np.arange(1, y.shape[0] + 1) / y.shape[0]
        else:
            y = np.arange(1, x.shape[0] + 1) / x.shape[0]
        
        ax.step(x, y, where='post', color=sns.color_palette()[g], label=method)
        if ci:
            lower, upper = dkw_confidence_band(y, x.shape[0], 0.01)
            ax.fill_between(x, lower, upper, color=sns.color_palette()[g], alpha=0.3)
    ax.fill_between([], [], [], color='grey', alpha=0.3, label='99% CI')
    ax.legend()
    fig.set_size_inches(10, 5)
    ax.set_ylim(-0.05, 1.05)
    xmin, xmax = np.percentile(np.concatenate([censored[:, i], resamples[:, i]]), (0.1, 99.9))
    ax.set_xlim(xmin, xmax)
    plt.tight_layout()
    fig.savefig(f'{life_change}_life_gain_cdf.png')
    fig.savefig(f'{life_change}_life_gain_cdf_2x.png', dpi=200)