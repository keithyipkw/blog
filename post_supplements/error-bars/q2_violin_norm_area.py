import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import scipy.stats as stats

def main():
    sns.set()
    fig, ax = plt.subplots()
    ax.set_title('Test Result', size=20)
    ax.barh([0, 1], [10, 14], xerr=[1, 2], tick_label=['Drug A', 'Drug B'], height=0.5, align='center', ecolor='black', capsize=10)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xlabel('Effect')
    ax.grid(False, axis='y')
    fig.set_size_inches(10, 2.5)
    plt.tight_layout()
    plt.show()

def main():
    sns.set()
    fig, ax = plt.subplots()
    ax.set_title('Test Result', size=20)
    
    sds = np.array([1.0, 2.0])
    means = [10.0, 14.0]
    ys = [0, 1]
    ax.barh(ys, means, xerr=sds* 3, tick_label=['Drug A', 'Drug B'], height=0.5, align='center', color='none', linewidth=0, ecolor='black', capsize=6)
    pdfs = []
    xs = []
    for d in range(0, 2):
        sd = sds[d]
        mean = means[d]
        x = np.linspace(mean - 4 * sd, mean + 4 * sd, 1001)
        xs.append(x)
        pdfs.append(stats.norm.pdf(x, loc=mean, scale=sd))
    
    max_pdf = max((max(pdf) for pdf in pdfs))
    for d in range(0, 2):
        sd = sds[d]
        mean = means[d]
        y = ys[d]
        label = '1 SE' if d == 0 else None
        ax.errorbar([mean + (i - 2 + 0.5) * sd for i in range(0, 4)], np.full(4, y), xerr=sd * 0.5, label=label, color='black', capsize=4)
        x = xs[d]
        pdf = pdfs[d]
        pdf = pdf / max_pdf * 0.25
        ax.fill_between(x, y + pdf, y - pdf)
    
    ax.set_ylim(-0.5, 1.5)
    ax.invert_yaxis()
    ax.set_xlabel('Effect')
    ax.grid(False, axis='y')
    ax.legend(handlelength=1)
    fig.set_size_inches(10, 2.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()