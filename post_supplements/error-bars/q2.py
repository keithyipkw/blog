import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def main():
    sns.set()
    fig, ax = plt.subplots()
    ax.set_title('Test Result', size=20)
    ax.barh([0, 1], [10, 14], xerr=[1, 2], tick_label=['Drug A', 'Drug B'], height=0.5, align='center', ecolor='black', capsize=10)
    ax.set_ylim(-0.5, 1.5)
    ax.invert_yaxis()
    ax.set_xlabel('Effect')
    ax.grid(False, axis='y')
    fig.set_size_inches(10, 2.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()