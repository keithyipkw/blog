This folder contains the code and supporting files used for writing the article "How Difficult is 1000 Endless Expert Levels Without Skipping in Super Mario Marker 2".

# Notable Files

* `env.yml` is an export of my Conda environment.

* `labeler.py` processes Panga's videos by labeling the levels with the ordinal and the life change.

* `expert.tsv` contains Panga's life changes in his first few attempts. It only contains entries that his level starting life was between 1 and 96 as explained in the article.

* `ci_study.py` checks the actual coverages of confidence intervals produced by different bootstraps.

* `analysis.py` calculates and draws the sample success rate and confidence intervals.