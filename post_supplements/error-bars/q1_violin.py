import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import scipy.stats as stats

def main():
    sns.set()
    fig, ax = plt.subplots()
    ax.set_title('Production Quality', size=20)
    
    sd = 2.0
    mean = 100.0
    ax.barh([0], [mean], xerr=[sd * 3], tick_label=['Rod'], align='center', color='none', linewidth=0, ecolor='black', capsize=10)[0]
    ax.errorbar([mean + (i - 2 + 0.5) * sd for i in range(0, 4)], np.full(4, 0), xerr=sd * 0.5, label='1 SD', color='black', capsize=5)

    x = np.linspace(mean - 4 * sd, mean + 4 * sd, 1001)
    pdf = stats.norm.pdf(x, loc=mean, scale=sd)
    pdf = pdf / np.max(pdf) * 0.4
    ax.fill_between(x, pdf, -pdf)

    ax.set_xlabel('Length (mm)')
    ax.grid(False, axis='y')
    ax.axvline(97.95, label='Tolerance', color='r')
    ax.axvline(102.05, color='r')
    ax.set_ylim(-1, 1)
    ax.set_xlim(90, 110)
    ax.legend(handlelength=1)
    fig.set_size_inches(10, 2.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()