import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
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
    h = 0.5
    ax.barh(ys, means, xerr=sds* 3, tick_label=['Drug A', 'Drug B'], height=h, align='center', color='none', linewidth=0, ecolor='black', capsize=6)
    for d in range(0, 2):
        sd = sds[d]
        mean = means[d]
        y = ys[d]
        label = '1 SE' if d == 0 else None
        ax.errorbar([mean + (i - 2 + 0.5) * sd for i in range(0, 4)], np.full(4, y), xerr=sd * 0.5, label=label, color='black', capsize=4)
        cdict = color_segment(sns.color_palette()[d])
        cmap = LinearSegmentedColormap('error_bar', cdict)   
        grad = stats.norm.pdf(np.linspace(-3, 3, 1001))
        grad = np.atleast_2d(grad)
        ax.imshow(grad, cmap=cmap, extent=[mean - 3 * sd, mean + 3 * sd, y - h * 0.5, y + h * 0.5], aspect='auto', zorder=1)
    
    ax.set_xlim(0, 21)
    ax.set_ylim(-0.5, 1.5)
    ax.invert_yaxis()
    ax.set_xlabel('Effect')
    ax.grid(False, axis='y')
    ax.legend(handlelength=1)
    fig.set_size_inches(10, 2.5)
    plt.tight_layout()
    plt.show()

def color_segment(color):
    return {
        'red': [[0.0, color[0], color[0]], [1.0, color[0], color[0]]],
        'green': [[0.0, color[1], color[1]], [1.0, color[1], color[2]]],
        'blue': [[0.0, color[2], color[2]], [1.0, color[2], color[2]]],
        'alpha': [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]
    }

if __name__ == "__main__":
    main()