# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import container
import matplotlib.ticker as mtick
import pandas as pd
import statsmodels.stats.proportion as proportion
import challenge

sns.set_theme()
data = pd.read_csv('expert.tsv', sep='\t')

sample_probabilities = challenge.life_change_prob(data)

data.loc[data['Starting Lives'] < 97, 'Starting Lives'] = '< 97'

# %%

%matplotlib widget

t = 0.0005
s = 3
y_scale_functions = [lambda x: np.minimum(x, t) * s + x, lambda x: x]

fig, ax = plt.subplots()
fig.suptitle("Panga's Uncensored Life Change After Beating a Level", fontsize=18)
ax.set_yscale('function', functions=y_scale_functions)
lives = np.unique(data['Lives'])
break_index = np.argmax(lives >= -20)
xs = np.arange(0, lives.shape[0] + 1) + 0.5
x_labels = lives.tolist()
x_labels.insert(break_index, "")
starting_lives = ['< 97', 97, 98, 99]
shrink = 0.8
width = shrink / len(starting_lives)
d = dict()
for i in range(sample_probabilities.shape[0]):
    if sample_probabilities[i] > 0:
        d[i - 99] = sample_probabilities[i]
ys = []
labels = []
for l in lives:
    y = d[l]
    if y > 0:
        labels.append(f'{y * 100:0.4f}%')
    else:
        labels.append('')
    ys.append(y)
ys.insert(break_index, 0)
labels.insert(break_index, '')
c = ax.bar(xs, ys)
ax.bar_label(c, labels=labels, label_type='edge', color=sns.color_palette()[0], fontsize=10, rotation=90, position=(1, 2))
ax.set_xticks(np.arange(0, lives.shape[0] + 1))
ax.set_xticklabels([])
ax.grid(axis='x', color='w', alpha=0.5)
ax.set_xticks(xs, minor=True)
ax.set_xticklabels(x_labels, minor=True)
ax.set_xlim(0, lives.shape[0] + 1)
ax.set_ylim(0, ax.get_ylim()[1] + 0.05)
ax.set_xlabel('Lives')
ax.set_ylabel('Proportion')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    
fig.set_size_inches(10, 5)
plt.tight_layout()

fig.savefig('life_change_uncensored_pmf.png', dpi=100)
fig.savefig('life_change_uncensored_pmf_2x.png', dpi=200)

# %%

t = 0.0005
s = 3
y_scale_functions = [lambda x: np.minimum(x, t) * s + x, lambda x: x]

fig, ax = plt.subplots()
fig.suptitle("Panga's Life Change After Beating a Level", fontsize=18)
ax.set_yscale('function', functions=y_scale_functions)
lives = np.unique(data['Lives'])
break_index = np.argmax(lives >= -20)
xs = np.arange(0, lives.shape[0] + 1) + 0.5
x_labels = lives.tolist()
x_labels.insert(break_index, "")
starting_lives = ['< 97', 97, 98, 99]
shrink = 0.8
width = shrink / len(starting_lives)
total = data.shape[0]
for i in range(len(starting_lives)):
    counts = np.unique(data[data['Starting Lives'] == starting_lives[i]]['Lives'], return_counts=True)
    d = dict(zip(*counts))
    d = {**dict(zip(lives, np.zeros_like(lives))), **d}
    ys = []
    labels = []
    for l in lives:
        y = d[l] / total
        if y > 0:
            labels.append(f'{y * 100:0.4f}%')
        else:
            labels.append('')
        ys.append(y)
    ys.insert(break_index, 0)
    labels.insert(break_index, '')
    c = ax.bar(xs - (len(starting_lives) / 2 - i - 0.5) * width, ys, width, label=starting_lives[i])
    ax.bar_label(c, labels=labels, label_type='edge', color=sns.color_palette()[i], fontsize=5, rotation=90, position=(1, 2))
ax.set_xticks(np.arange(0, lives.shape[0] + 1))
ax.set_xticklabels([])
ax.grid(axis='x', color='w', alpha=0.5)
ax.set_xticks(xs, minor=True)
ax.set_xticklabels(x_labels, minor=True)
ax.set_xlim(0, lives.shape[0] + 1)
ax.set_ylim(0, ax.get_ylim()[1] * 1.05)
ax.set_xlabel('Lives')
ax.set_ylabel('Proportion')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.legend(title='Starting Lives')
    
fig.set_size_inches(10, 5)
plt.tight_layout()

fig.savefig('life_change_pmf.png', dpi=100)
fig.savefig('life_change_pmf_2x.png', dpi=200)

# %%

t = 0.0005
s = 15
y_scale_functions = [lambda x: np.minimum(x, t) * s + x, lambda x: x]

fig, ax = plt.subplots()
fig.suptitle("Panga's Life Change After Beating a Level", fontsize=18)
ax.set_yscale('function', functions=y_scale_functions)
lives = np.unique(data['Lives'])
break_index = np.argmax(lives >= -20)
xs = np.arange(0, lives.shape[0] + 1) + 0.5
x_labels = lives.tolist()
x_labels.insert(break_index, "")
starting_lives = ['< 97', 97, 98, 99]
shrink = 0.8
width = shrink / len(starting_lives)
for i in range(len(starting_lives)):
    counts = np.unique(data[data['Starting Lives'] == starting_lives[i]]['Lives'], return_counts=True)
    total = counts[1].sum()
    d = dict(zip(*counts))
    d = {**dict(zip(lives, np.zeros_like(lives))), **d}
    ys = []
    labels = []
    for l in lives:
        y = d[l] / total
        if y > 0:
            labels.append(f'{y * 100:0.4f}%')
        else:
            labels.append('')
        ys.append(y)
    ys.insert(break_index, 0)
    labels.insert(break_index, '')
    c = ax.bar(xs - (len(starting_lives) / 2 - i - 0.5) * width, ys, width, label=starting_lives[i])
    ax.bar_label(c, labels=labels, label_type='edge', color=sns.color_palette()[i], fontsize=5, rotation=90, position=(1, 2))
ax.set_xticks(np.arange(0, lives.shape[0] + 1))
ax.set_xticklabels([])
ax.grid(axis='x', color='w', alpha=0.5)
ax.set_xticks(xs, minor=True)
ax.set_xticklabels(x_labels, minor=True)
ax.set_xlim(0, lives.shape[0] + 1)
ax.set_ylim(0, ax.get_ylim()[1] * 1.05)
ax.set_xlabel('Lives')
ax.set_ylabel('Proportion Within Group')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.legend(title='Starting Lives')
    
fig.set_size_inches(10, 5)
plt.tight_layout()

fig.savefig('life_change_pmf_group.png', dpi=100)
fig.savefig('life_change_pmf_group_2x.png', dpi=200)

# %%

fig, ax = plt.subplots()
fig.suptitle("Panga's Life Change After Beating a Level", fontsize=18)
lives = np.unique(data['Lives'])
xs = np.arange(-99, 4)
starting_lives = ['< 97']
shrink = 0.8
width = shrink / len(starting_lives)
for i in range(len(starting_lives)):
    counts = np.unique(data[data['Starting Lives'] == starting_lives[i]]['Lives'], return_counts=True)
    total = counts[1].sum()
    d = dict(zip(*counts))
    d = {**dict(zip(lives, np.zeros_like(lives))), **d}
    ys = []
    labels = []
    for l in range(-99, 4):
        if l in d:
            y = d[l] / total
        else:
            y = 0
        if y > 0:
            labels.append(f'{y * 100:0.4f}%')
        else:
            labels.append('')
        ys.append(y)
    c = ax.bar(xs - (len(starting_lives) / 2 - i - 0.5) * width, ys, width, label=starting_lives[i])
    ax.bar_label(c, labels=labels, label_type='edge', color=sns.color_palette()[i], fontsize=5, rotation=90, position=(1, 2))
ax.xaxis.set_major_locator(mtick.MultipleLocator(10))
ax.xaxis.set_minor_locator(mtick.MultipleLocator(1))
ax.grid(axis='x', color='w', alpha=0.5)
ax.grid(which='minor', axis='x', color='w', alpha=0.3)
ax.set_xlim(-99.9, 4)
ax.set_ylim(0, ax.get_ylim()[1] * 1.07)
ax.set_xlabel('Lives')
ax.set_ylabel('Proportion Within Group')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.legend(title='Starting Lives')
    
fig.set_size_inches(10, 5)
plt.tight_layout()

fig.savefig('life_change_pmf_group_97.png', dpi=100)
fig.savefig('life_change_pmf_group_97_2x.png', dpi=200)

# %%

censored = data.copy()
for i in range(3):
    censored.loc[censored['Lives'] == 3 - i, 'Lives'] = 2 - i
    censored.loc[(censored['Starting Lives'] == f'< {96 + i}') | (censored['Starting Lives'] == 96 + i), 'Starting Lives'] = f'< {97 + i}'

    fig, ax = plt.subplots()
    fig.suptitle("Censored Panga's Life Change After Beating a Level", fontsize=18)
    fg = sns.histplot(censored, x='Lives', hue='Starting Lives', hue_order=[f'< {97 + i}', 97 + i], stat='percent', common_norm=False, discrete=True, multiple='dodge', shrink=0.8, ax=ax)
    ax.xaxis.set_major_locator(mtick.MultipleLocator(1))
    ax.set_xlim(-10 - 0.5, data['Lives'].max() + 0.5)

    # # add annotations
    # for c in ax.containers:

    #     # custom label calculates percent and add an empty string so 0 value bars don't have a number
    #     labels = [f'{w:0.1f}%' if (w := v.get_height()) > 0 else '' for v in c]

    #     ax.bar_label(c, labels=labels, label_type='edge', fontsize=10, rotation=90, padding=4)

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
    legend_handles = []
     
    lives = np.arange(-5, 3 - i)
    xs = lives + 0.5
    starting_lives = [f'< {97 + i}', 97 + i]
    x_offsets = [-0.2, 0.2]
    width = 0.4
    all_cis = {}
    all_pdf = {}
    all_99_cis = {}
    for s in range(len(starting_lives)):
        counts = np.unique(censored[(censored['Starting Lives'] == starting_lives[s]) & (censored['Lives'] >= lives[0])]['Lives'], return_counts=True)
        total = np.count_nonzero(censored['Starting Lives'] == starting_lives[s])
        d = dict(zip(*counts))
        d = {**dict(zip(lives, np.zeros_like(lives))), **d}
        ys = []
        labels = []
        for l in range(lives.shape[0]):
            life = lives[l]
            y = d[life] / total
            if y > 0:
                labels.append(f'{y * 100:.0f}%')
            else:
                labels.append('')
            ys.append(y)
            
            cis = {0.5: d[life] / total}
            cis[0] = 0
            cis[1] = 1
            all_99_cis[(s, l)] = proportion.proportion_confint(d[life], total, 0.01, method='wilson')
            for alpha in np.linspace(0.01, 100-0.01, 300):
                ci = proportion.proportion_confint(d[life], total, alpha / 100, method='wilson')
                cis[1 - alpha / 200] = ci[1]
                cis[alpha / 200] = ci[0]
            alphas = np.array(sorted(cis.keys()))
            cis = np.array([cis[a] for a in alphas])
            pdf = np.zeros_like(cis)
            pdf[1:-1] = (alphas[2:] - alphas[:-2]) / (cis[2:] - cis[:-2])
            all_cis[(s, l)] = cis
            all_pdf[(s, l)] = pdf
    
    max_pdf = max((all_pdf[key].max() for key in all_pdf))
    for s in range(len(starting_lives)):
        for l in range(lives.shape[0]):
            cis = all_cis[(s, l)]
            pdf = all_pdf[(s, l)]
            pdf *= width / 2 / max_pdf            
            h = ax.fill_betweenx(cis, xs[l] + x_offsets[s] - pdf, xs[l] + x_offsets[s] + pdf, color=sns.color_palette()[s], linewidth=0, label=starting_lives[s])
            
            lower, upper = all_99_cis[(s, l)]
            errorbar_handle = ax.errorbar(xs[l] + x_offsets[s], (lower + upper) * 0.5, yerr=(upper - lower) * 0.5, label='99% CI', linewidth=0, ecolor='gray', capthick=0.5, capsize=4)
        legend_handles.append(h)
    h = ax.plot(np.NaN, np.NaN, '-', color='none', label=' ', zorder=1)
    legend_handles.extend(h)
    legend_handles.append(errorbar_handle)
            
    ax.set_xticks(np.arange(lives[0], 3))
    ax.set_xticklabels([])
    ax.grid(axis='x', color='w', alpha=0.5)
    ax.set_xticks(np.arange(lives[0], 3) + 0.5, minor=True)
    xlabels = [l for l in range(lives[0], 0)]
    for l in range(0, 3):
        if l < 3 - i - 1:
            xlabels.append(l)
        elif l == 3 - i - 1:
            xlabels.append(f'≥ {l}')
        else:
            xlabels.append('')
    ax.set_xticklabels(xlabels, minor=True)
    ax.set_xlim(lives[0], 3)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax.set_ylim(0, 1)
    
    ax.legend(handles=legend_handles, title='Starting Lives', loc='upper left')

    fig.supylabel('Probability Density Function\nof Proportion Within Group', ha='center')
    fig.supxlabel('Lives')
    fig.set_size_inches(10, 5)
    plt.tight_layout()
    
    fig.savefig(f'life_change_pdf_{97 + i}.png', dpi=100, bbox_inches="tight")
    fig.savefig(f'life_change_pdf_{97 + i}_2x.png', dpi=200, bbox_inches="tight")

# %%

# %%

gs_kw = dict(width_ratios=[3, 2, 1])
fig, axs = plt.subplots(1, 3, gridspec_kw=gs_kw)
fig.suptitle("Censored Panga's Life Change After Beating a Level", fontsize=18)
color = 0
censored = data.copy()
for i in range(3):
    ax = axs[i]
    censored.loc[censored['Lives'] == 3 - i, 'Lives'] = 2 - i
    censored.loc[(censored['Starting Lives'] == f'< {96 + i}') | (censored['Starting Lives'] == 96 + i), 'Starting Lives'] = f'< {97 + i}'
    
    lives = np.arange(0, 3 - i)
    xs = lives + 0.5
    x_labels = lives.tolist()
    starting_lives = [f'< {97 + i}', 97 + i]
    shrink = 0.8
    width = shrink / len(starting_lives)
    for s in range(len(starting_lives)):
        counts = np.unique(censored[(censored['Starting Lives'] == starting_lives[s]) & (censored['Lives'] >= 0)]['Lives'], return_counts=True)
        total = np.count_nonzero(censored['Starting Lives'] == starting_lives[s])
        d = dict(zip(*counts))
        d = {**dict(zip(lives, np.zeros_like(lives))), **d}
        ys = []
        labels = []
        for l in lives:
            y = d[l] / total
            if y > 0:
                labels.append(f'{y * 100:.0f}%')
            else:
                labels.append('')
            ys.append(y)
        c = ax.bar(xs - (len(starting_lives) / 2 - s - 0.5) * width, ys, width, color=sns.color_palette()[color], label=starting_lives[s])
        ax.bar_label(c, labels=labels, label_type='edge', color=sns.color_palette()[color], fontsize=15, position=(1, 2))
        color += 1
    ax.set_xticks(np.arange(0, lives.shape[0] + 1))
    ax.set_xticklabels([])
    ax.grid(axis='x', color='w', alpha=0.5)
    ax.set_xticks(xs, minor=True)
    ax.set_xticklabels(x_labels, minor=True)
    ax.set_xlim(0, lives.shape[0])
    ax.set_ylim(0, ax.get_ylim()[1] * 1.4)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax.legend(title='Starting Lives')

fig.supylabel('Proportion Within Group')
fig.supxlabel('Lives')

fig.set_size_inches(10, 5)
plt.tight_layout()

# %%

gs_kw = dict(width_ratios=[3, 2, 1])
fig, axs = plt.subplots(1, 3, gridspec_kw=gs_kw)
fig.suptitle("Censored Panga's Life Change After Beating a Level", fontsize=18)
color = 0
censored = data.copy()
legend_loc = ['upper right', 'upper right', 'lower right']
for i in range(3):
    ax = axs[i]
    censored.loc[censored['Lives'] == 3 - i, 'Lives'] = 2 - i
    censored.loc[(censored['Starting Lives'] == f'< {96 + i}') | (censored['Starting Lives'] == 96 + i), 'Starting Lives'] = f'< {97 + i}'
    
    lives = np.arange(0, 3 - i)
    xs = lives + 0.5
    x_labels = lives.tolist()
    starting_lives = [f'< {97 + i}', 97 + i]
    x_offsets = [-0.2, 0.2]
    width = 0.3
    for s in range(len(starting_lives)):
        counts = np.unique(censored[(censored['Starting Lives'] == starting_lives[s]) & (censored['Lives'] >= 0)]['Lives'], return_counts=True)
        total = np.count_nonzero(censored['Starting Lives'] == starting_lives[s])
        d = dict(zip(*counts))
        d = {**dict(zip(lives, np.zeros_like(lives))), **d}
        ys = []
        labels = []
        all_pdf = []
        all_cis = []
        for l in lives:
            y = d[l] / total
            if y > 0:
                labels.append(f'{y * 100:.0f}%')
            else:
                labels.append('')
            ys.append(y)
            
            cis = {0.5: d[l] / total}
            cis[0] = 0
            cis[1] = 1
            for alpha in np.linspace(0.01, 100-0.01, 300):
                ci = proportion.proportion_confint(d[l], total, alpha / 100, method='wilson')
                cis[1 - alpha / 200] = ci[1]
                cis[alpha / 200] = ci[0]
            alphas = np.array(sorted(cis.keys()))
            cis = np.array([cis[a] for a in alphas])
            pdf = np.zeros_like(cis)
            pdf[1:-1] = (alphas[2:] - alphas[:-2]) / (cis[2:] - cis[:-2])
            pdf *= width / 2 / pdf.max()
            label = starting_lives[s] if l == 0 else None
            ax.fill_betweenx(cis, xs[l] + x_offsets[s] - pdf, xs[l] + x_offsets[s] + pdf, color=sns.color_palette()[color], label=label)
            
        color += 1
    ax.set_xticks(np.arange(0, lives.shape[0] + 1))
    ax.set_xticklabels([])
    ax.grid(axis='x', color='w', alpha=0.5)
    ax.set_xticks(xs, minor=True)
    ax.set_xticklabels(x_labels, minor=True)
    ax.set_xlim(0, lives.shape[0])
    if i == 0:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    else:
        ax.set_yticklabels([])
    ax.set_ylim(0, 1)
    ax.legend(title='Starting Lives', loc=legend_loc[i])

fig.supylabel('Probability Density Function\nof Proportion Within Group', ha='center')
fig.supxlabel('Lives')

fig.set_size_inches(10, 5)
plt.tight_layout()

# %%
