from typing import Tuple
import numpy as np

def level_survivial(samples: np.ndarray, level_count: int) -> Tuple[np.ndarray, np.ndarray]:
    lives, counts = np.unique(samples, return_counts=True)

    # for life change [min, min - 1, ... 0, 1, 2, 3]
    life_pmf = np.zeros(4 - min(0, min(lives)))
    for l, c in zip(lives, counts):
        life_pmf[life_pmf.shape[0] - 4 + l] = c
    life_pmf /= life_pmf.sum()
    
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
