from typing import Tuple
import numpy as np
import pandas as pd

def life_change_prob(data: pd.DataFrame) -> np.ndarray:
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

def level_survivial_prob(probabilities: np.ndarray, level_count: int) -> Tuple[np.ndarray, np.ndarray]:
    # for life change [min, min - 1, ... 0, 1, 2, 3]
    life_pmf = probabilities
    
    # calculate the transition matrix
    transition = np.zeros((100, 100))
    zero_life_index = life_pmf.shape[0] - 4
    transition[0, 0] = 1
    for i in range(1, 100):
        life_start = zero_life_index - i
        if life_start < 0:
            transition_start = -life_start
            life_start = 0
        else:
            transition_start = 0
        transition_end = i + 4
        if transition_end <= 100:
            life_end = life_pmf.shape[0]
        else:
            life_end = life_pmf.shape[0] - transition_end + 100
            transition_end = 100
        transition[i, transition_start:transition_end] = life_pmf[life_start:life_end]
        if life_start > 0:
            transition[i, 0] += life_pmf[0:life_start].sum()
        if life_end < life_pmf.shape[0]:
            transition[i, -1] += life_pmf[life_end:life_pmf.shape[0]].sum()
    states = np.zeros(100)
    states[15] = 1
    level_pmf = np.zeros(level_count)

    for level in range(level_count):
        states = states.dot(transition)
        level_pmf[level] = states[0]
        states[0] = 0
    
    level_survival = np.zeros((level_count))
    for i in range(level_survival.shape[0]):
        level_survival[i] = 1 - level_pmf[0:i + 1].sum()
    return level_pmf, level_survival

def transition(probabilities: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    # for life change [min, min - 1, ... 0, 1, 2, 3]
    life_pmf = probabilities
    
    # calculate the transition matrix
    transition = np.zeros((100, 100))
    zero_life_index = life_pmf.shape[0] - 4
    transition[0, 0] = 1
    for i in range(1, 100):
        life_start = zero_life_index - i
        if life_start < 0:
            transition_start = -life_start
            life_start = 0
        else:
            transition_start = 0
        transition_end = i + 4
        if transition_end <= 100:
            life_end = life_pmf.shape[0]
        else:
            life_end = life_pmf.shape[0] - transition_end + 100
            transition_end = 100
        transition[i, transition_start:transition_end] = life_pmf[life_start:life_end]
        if life_start > 0:
            transition[i, 0] += life_pmf[0:life_start].sum()
        if life_end < life_pmf.shape[0]:
            transition[i, -1] += life_pmf[life_end:life_pmf.shape[0]].sum()
    return transition