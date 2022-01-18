import os
import errno
import numpy as np
from scipy import stats
import seaborn as sns
from matplotlib import pyplot as plt

def save_sample(sample, name):
    ax = plt.subplots(figsize=(1.5, 0.75))[1]
    sns.histplot(sample, binwidth=1, binrange=(0, 16), ax=ax)
    ax.set_xlim(0, 16)
    remove_labels(ax)
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.savefig(name)
    plt.close()

def save_pdf(name):
    save_pdf_ci(name, False)

def save_ci(name):
    save_pdf_ci(name, True)

def save_pdf_ci(name, ci):
    ax = plt.subplots(figsize=(1.5, 0.75))[1]
    x = np.linspace(-5, 5, 100)
    y = stats.norm.pdf(x)
    sns.lineplot(x=x, y=y, color=sns.color_palette()[1])
    if ci:
        ax.axvline(-2, color=sns.color_palette()[2])
        ax.axvline(2, color=sns.color_palette()[2])
    ax.set_xlim(-5, 5)
    remove_labels(ax)
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.savefig(name)
    plt.close()

def save_statistic(name):
    ax = plt.subplots(figsize=(1.5, 0.75))[1]
    sns.histplot(np.random.normal(0, 1, size=300), binwidth=0.5, binrange=(-5, 5), ax=ax, color=sns.color_palette()[1])
    ax.set_xlim(-5, 5)
    remove_labels(ax)
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.savefig(name)
    plt.close()

def remove_labels(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.axes.get_xaxis().set_visible(False)
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.axes.get_yaxis().set_visible(False)

folder = 'bs_example/'
sns.set()
np.random.seed(0)

if not os.path.exists(os.path.dirname(folder)):
    try:
        os.makedirs(os.path.dirname(folder))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

population = np.random.gamma(2, 2, 300)
save_sample(population, f'{folder}population.png')

for i in range(3, -1, -1):
    sample = np.random.choice(population, size=population.shape[0])
    save_sample(sample, f'{folder}sample{i}.png')

resamples = []
for i in range(4):
    resample = np.random.choice(sample, size=population.shape[0])
    resamples.append(resample)
    save_sample(resample, f'{folder}resample{i}.png')

for i in range(2):
    save_statistic(f'{folder}statistic{i}.png')

for i in range(4):
    reresample = np.random.choice(resamples[i], size=population.shape[0])
    save_sample(reresample, f'{folder}re-resample{i}.png')

save_pdf(f'{folder}pdf.png')

save_ci(f'{folder}ci.png')
