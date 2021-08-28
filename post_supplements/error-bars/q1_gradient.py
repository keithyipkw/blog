import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import scipy.stats as stats

def main():
    sns.set()
    fig, ax = plt.subplots()
    ax.set_title('Production Quality', size=20)
    
    sd = 2.0
    mean = 100.0
    ax.barh([0], [mean], xerr=[sd * 3], tick_label=['Rod'], align='center', color='none', linewidth=0, ecolor='black', capsize=10)[0]
    ax.errorbar([mean + (i - 2 + 0.5) * sd for i in range(0, 4)], np.full(4, 0), xerr=sd * 0.5, label='1 SD', color='black', capsize=5)

    y = -0.4
    h = 0.8
    cdict = color_segment(sns.color_palette()[0])
    cmap = LinearSegmentedColormap('error_bar', cdict)   
    grad = stats.norm.pdf(np.linspace(-3, 3, 1001))
    grad = np.atleast_2d(grad)
    ax.imshow(grad, cmap=cmap, extent=[mean - 3 * sd, mean + 3 * sd, y, y + h], aspect='auto', zorder=1)

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

def color_segment(color):
    return {
        'red': [[0.0, color[0], color[0]], [1.0, color[0], color[0]]],
        'green': [[0.0, color[1], color[1]], [1.0, color[1], color[2]]],
        'blue': [[0.0, color[2], color[2]], [1.0, color[2], color[2]]],
        'alpha': [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]
    }

if __name__ == "__main__":
    main()