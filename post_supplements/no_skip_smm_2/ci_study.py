# %%
import time
import multiprocessing as mp
import signal
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import psutil
from scipy import stats
import ci_study_worker as worker

if __name__ == '__main__':
    level_count = 3000
    resample_size = 40000
    experiment_count = 4000

    ci_sizes = [0.95, 0.99]
    # methods = ['basic', 'percentile', 'bc', 'bca']
    methods = ['bca', 'bc', 'percentile']

    parent = psutil.Process()
    parent.nice(psutil.IDLE_PRIORITY_CLASS)
        
    sns.set_theme()
    np.set_printoptions(precision=4)

    process_count = mp.cpu_count()
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = mp.Pool(processes=process_count)
    data = pd.read_csv('expert.tsv', sep='\t')
    data2 = pd.read_csv('expert_removed.tsv', sep='\t')
    data['Starting Lives'] = 96
    data = pd.concat([data, data2], ignore_index=True)

    hit_rates = {}

    start_time = time.time()
    with mp.Pool(processes=process_count) as pool:
        results = pool.starmap(worker.simulation, ((data, level_count, ci_sizes, methods, resample_size, experiment_count, process_count, i) for i in range(0, process_count)))
        for ci_size in ci_sizes:
            hit_rates[ci_size] = {}
            for m in methods:
                hit_rates[ci_size][m] = np.zeros(level_count)
                for r in results:
                    hit_rates[ci_size][m] += r[ci_size][m]
                hit_rates[ci_size][m] /= experiment_count

    print(f'Completed in {time.time() - start_time:.0f}s')
# %%

    # %matplotlib widget

    for ci_size in ci_sizes:
        fig, ax = plt.subplots()
        ax.set_title(f'{ci_size} Confidence Interval Coverage', size=20)
        ax.set_xlabel('Survived Levels')
        ax.set_ylabel('Cover Rate')
        for i in range(len(methods)):
            m = methods[i]
            sns.lineplot(x=np.arange(1, level_count + 1), y=hit_rates[ci_size][m], ax=ax, label=m)
        ax.axhline(ci_size, color='grey', alpha=0.5, label='Target Rate')
        for alpha, opacity, line in [(0.01, 0.3, '--'), (0.0001, 0.15, '-.')]:
            ys = stats.binom.interval(1 - alpha, experiment_count, ci_size)
            ax.axhline(ys[0] / experiment_count, color='grey', alpha=opacity, linestyle=line, label=f'α = {alpha:.2%}')
            ax.axhline(ys[1] / experiment_count, color='grey', alpha=opacity, linestyle=line)
        ax.legend()
        fig.set_size_inches(10, 5)
        plt.tight_layout()
        plt.savefig(f'{resample_size} {experiment_count} {ci_size}.png')
        plt.savefig(f'{resample_size} {experiment_count} {ci_size}_2x.png', dpi=200)

    plt.show()

    with open(f'{resample_size} {experiment_count}.txt', 'a') as f:
        for i in range(len(methods)):
            m = methods[i]
            f.write(m)
            f.write('\n')
            for ci_size in ci_sizes:
                for l in [999, 1999, 2999]:
                    f.write(f'{ci_size:.0%} CI of level {l + 1}: {hit_rates[ci_size][m][l]:.1%}\n')
# %%
