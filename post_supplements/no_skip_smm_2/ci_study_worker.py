import tqdm
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from archbs import IIDBootstrap
import challenge
from typing import List

def cal_probability(data):
    sample_probabilities = np.zeros(4 - data['Lives'].min())
    
    applicables = data[data['Lives'] < 0]
    rate = 1 / data.shape[0]
    lives, counts = np.unique(applicables['Lives'], return_counts=True)
    for l, c in zip(lives, counts):
        sample_probabilities[l - 4] = c * rate

    remainings = data
    base = 1 - applicables.shape[0] / data.shape[0]
    for i in range(3):
        remainings = remainings[(remainings['Lives'] >= i) & (remainings['Starting Lives'] < 99 - i)]
        if remainings.shape[0] == 0:
            base = 0
            break
        p = base * (remainings['Lives'] == i).sum() / remainings.shape[0]
        sample_probabilities[-4 + i] = p
        base -= p
    sample_probabilities[-1] = base
    return sample_probabilities

def simulation(data: DataFrame, level_count:int, ci_sizes: List[float], methods: List[str], resample_size: int, total_experiment_count: int, process_count: int, process: int):

    def cal_cdf(data):
        sample_probabilities = cal_probability(data)
        return challenge.level_survivial_prob(sample_probabilities, level_count)[1]

    if process == process_count - 1:
        pbar = tqdm.tqdm(total=total_experiment_count)
    try:
        life_sample_size = data.shape[0]
        true_values = cal_cdf(data)

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
        
        true_probabilities = cal_probability(data)
        
        for r in range(experiment_count):
            i = r + start
            rng = np.random.default_rng(i)
            resample = rng.multinomial(life_sample_size, true_probabilities)
            resample = np.repeat(range(4 - true_probabilities.shape[0], 4), resample)
            rng.shuffle(resample)
            
            starting_lives = np.zeros(resample.shape, np.int32)
            starting_lives[0] = 15
            for j in range(life_sample_size - 1):
                lives = min(99, starting_lives[j] + resample[j])
                if lives <= 0:
                    lives = 15
                starting_lives[j + 1] = lives
            resample = np.minimum(99 - starting_lives, resample)
            resample_df = pd.DataFrame({
                'Starting Lives': starting_lives,
                'Lives': resample,
            })
            
            bs = IIDBootstrap(resample_df, seed=i + 1)
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