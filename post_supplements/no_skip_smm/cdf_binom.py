# %%
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import statsmodels.stats.proportion as proportion

%matplotlib widget

sns.set_theme()

fig, ax = plt.subplots()
ax.set_title('Cumulative Distribution Function of Success Rate', size=20)
ax.set_ylabel('Cumulative Probability')
ax.set_xlabel('Probability of Success')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.yaxis.set_major_locator(mtick.MultipleLocator(0.1))
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.xaxis.set_major_locator(mtick.MultipleLocator(0.1))

ax.hlines(0.025, 0, 1, color=sns.color_palette()[2], label=f'95% CI')
ax.hlines(0.975, 0, 1, color=sns.color_palette()[2])

for win, loss, label in [(1, 1, '1 win, 1 loss'), (2, 2, '2 wins, 2 loss')]:
    total = win + loss
    cis = {0.5: win / total}
    cis[0] = 0
    cis[1] = 1
    for alpha in np.linspace(0.01, 100-0.01, 200):
        ci = proportion.proportion_confint(win, total, alpha / 100, method='wilson')
        cis[1 - alpha / 200] = ci[1]
        cis[alpha / 200] = ci[0]

    for alpha in [0.05, 0.01]:
        print(f"{alpha}: {proportion.proportion_confint(win, total, alpha, method='wilson')}")

    ys = sorted(cis.keys())
    xs = [cis[i] for i in ys]
    sns.lineplot(x=xs, y=ys, ax=ax, label=label)

ax.legend()

fig.set_size_inches(10, 5)
plt.tight_layout()
plt.show()