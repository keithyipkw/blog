# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import challenge

sns.set_theme()
data = pd.read_csv('expert.tsv', sep='\t')

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

transition = challenge.transition(sample_probabilities)
transition = transition[1:, 1:]
states = np.zeros(99)
states[14] = 1
decays = []
for i in range(10000):
    next = states.dot(transition)
    decays.append(next.sum() / states.sum())
    states = next
    
print(f'{decays[-1] * 100:.4g}%')

%matplotlib widget

# %%

fig, ax = plt.subplots()
fig.suptitle('Decay Rates of Panga\'s Sample Success Rate', fontsize=18)
ax.plot(np.arange(1, 1001), decays[0:1000])
ax.set_xlabel('Level')
ax.set_ylabel('Per Level')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
fig.set_size_inches(10, 5)
plt.tight_layout()
plt.savefig('pangas_sample_success_rate_decay.png')
plt.savefig('pangas_sample_success_rate_decay_2x.png', dpi=200)
plt.show(block=False)

# %%

fig, ax = plt.subplots()
fig.suptitle('Limiting Distribution of Panga\'s Lives', fontsize=18)
ax.bar(np.arange(1, len(states) + 1), states / states.sum())
ax.set_xlabel('Number of Lives')
ax.set_ylabel('Normalized Proportion')
fig.set_size_inches(10, 5)
plt.tight_layout()
plt.savefig('pangas_lives_limit_distribution.png')
plt.savefig('pangas_lives_limit_distribution_2x.png', dpi=200)
plt.show(block=False)

# %%

w, v = np.linalg.eig(transition.T)
is_real = np.logical_and(np.abs(np.imag(w)) < 0.0001, np.all(np.abs(np.imag(v)) < 0.0001, axis=0))

sign = np.signbit(np.real(v))
same_sign = np.logical_or(np.all(sign, axis=0), np.all(sign == False, axis=0))

valid = np.argwhere(np.logical_and(is_real, same_sign)).flatten()
print(valid)
for i in valid:
    print(np.real(w[valid[i]]))
    a = np.real(v[:, valid[i]])
    a = a / a.sum()
    print(a)