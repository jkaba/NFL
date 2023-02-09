# Learning the NFL Draft

Using Machine Learning to perform a mock 2016 draft to compare against actual results.

## Scraping the data
Pro Football Reference has data on historical drafts and combine results. They also link to college statistics of a large number of the players who were drafted or appeared at the combine.

The following data was gathered:
- 6264 players in total.
- 4079 players that were drafted.
- 5556 that appeared at the NFL combine.
- 4488 players with at least some basic college stats available.

## Goal
The goal is to build a model to answer the following question:
- What is the probability that the player will be picked in the first round? (Assume players with high first round probabilities are drafted higher)