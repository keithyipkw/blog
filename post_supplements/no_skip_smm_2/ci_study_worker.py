import tqdm
import numpy as np
from pandas.core.frame import DataFrame
from archbs import IIDBootstrap
import challenge
from typing import List

def simulation(data: DataFrame, level_count:int, ci_sizes: List[float], methods: List[str], resample_size: int, total_experiment_count: int, process_count: int, process: int):

    def cal_cdf(samples):
        return challenge.level_survivial(samples, level_count)[1]

    if process == process_count - 1:
        pbar = tqdm.tqdm(total=total_experiment_count)
    try:
        life_sample_size = len(data['Lives'])
        true_values = cal_cdf(data['Lives'])

        experiment_count = total_experiment_count // process_count
        remaining = total_experiment_count - experiment_count * process_count
        if process_count - remaining > process:
            start = experiment_count * process
        else:
            start = experiment_count * (process_count - remaining) + (experiment_count + 1) * (process - process_count + remaining)
            experiment_count += 1

        hits = {}
        for ci_size in ci_sizes:
            hits[ci_size] = {}
            for m in methods:
                hits[ci_size][m] = np.zeros(level_count)
        
        for r in range(experiment_count):
            i = r + start
            np.random.seed(i)
            samples = np.random.choice(data['Lives'], size=life_sample_size)
            bs = IIDBootstrap(samples, seed=i + 1)
            reuse = False
            for m in methods:
                for ci_size in ci_sizes:
                    ci = bs.conf_int(cal_cdf, method=m, size=ci_size, reuse=reuse, reps=resample_size)
                    reuse = True
                    hits[ci_size][m] += np.logical_and(ci[0] <= true_values, true_values <= ci[1])
            if process == process_count - 1:
                pbar.update(process_count)

        return hits
    except KeyboardInterrupt:
        return {}
    finally:
        if process == process_count - 1:
            pbar.close()

def formatted_time(second: int) -> str:
    return f'{second // 3600:02}:{second % 3600 // 60:02}:{second % 60:02}'