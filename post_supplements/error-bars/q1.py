import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def main():
    sns.set()
    fig, ax = plt.subplots()
    ax.set_title('Production Quality', size=20)
    ax.barh([0], [100], xerr=[2], tick_label=['Rod'], align='center', ecolor='black', capsize=10)
    ax.set_xlabel('Length (mm)')
    ax.grid(False, axis='y')
    ax.axvline(97.95, label='Tolerance', color='r')
    ax.axvline(102.05, color='r')
    ax.set_ylim(-1, 1)
    ax.set_xlim(95, 105)
    ax.legend()
    fig.set_size_inches(10, 2.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()