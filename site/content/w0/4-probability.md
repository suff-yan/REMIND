---
title: "Maths I: probability, averages and expected value"
minutes: 70
video: w0_averages
videoTitle: Averages that learn
checkpoint:
  kind: browser
  title: A running mean
  prompt: "Write `running_means(xs)` that returns the average after each new value, using the incremental update (no re-summing the whole list each time). Then watch a simulated die converge to 3.5."
  starter: |
    import random

    def running_means(xs):
        means = []
        q, n = 0.0, 0
        for x in xs:
            # TODO: update n, then update q with q + (x - q) / n
            means.append(q)
        return means

    rng = random.Random(0)
    rolls = [rng.randint(1, 6) for _ in range(2000)]
    m = running_means(rolls)
    print("after 10 rolls:", round(m[9], 3), " after 2000:", round(m[-1], 3))
  tests: |
    assert running_means([2, 4, 6]) == [2.0, 3.0, 4.0], running_means([2, 4, 6])
    assert abs(running_means(rolls)[-1] - 3.5) < 0.1
    print("running mean works")
quiz:
  - q: "A fair die is rolled. What is the expected value?"
    options: ["3", "3.5", "4", "6"]
    answer: 1
    explain: "(1+2+3+4+5+6)/6 = 3.5."
  - q: "A quiz style helps you remember 70% of the time. Over 200 quizzes, about how many help?"
    options: ["70", "100", "140", "200"]
    answer: 2
    explain: "Expected count = 0.7 × 200 = 140."
  - q: "In $Q_{n+1} = Q_n + \\frac{1}{n}(r - Q_n)$, what is $(r - Q_n)$?"
    options: ["The learning rate", "The error: how surprised we were", "The number of samples", "The final answer"]
    answer: 1
    explain: "New estimate = old estimate + step size × error. This exact shape is the Q-learning update in Week 3."
  - q: "Why does the running average of die rolls get closer to 3.5 as you roll more?"
    options: ["The die learns", "Random fluctuations cancel out over many samples (law of large numbers)", "Later rolls are worth more", "It doesn't"]
    answer: 1
    explain: "The law of large numbers: sample averages approach the expected value."
  - q: "If P(recall) = 0.8, what is P(forget)?"
    options: ["0.8", "0.2", "1.8", "0"]
    answer: 1
    explain: "Probabilities of all outcomes sum to 1."
  - q: "A game pays +10 with probability 0.2 and −1 otherwise. Expected payoff?"
    options: ["+1.2", "+2.0", "−0.8", "+10"]
    answer: 0
    explain: "0.2 × 10 + 0.8 × (−1) = 2 − 0.8 = 1.2."
resources:
  - label: Seeing Theory, chapter 1 (interactive probability)
    url: https://seeing-theory.brown.edu/basic-probability/index.html
  - label: 3Blue1Brown, binomial distributions
    url: https://www.youtube.com/watch?v=8idr1WZ1A7Q
  - label: Khan Academy, expected value
    url: https://www.khanacademy.org/math/statistics-probability/random-variables-stats-library
---
Reinforcement learning is, at heart, about estimating averages of uncertain things. Three ideas carry the whole project.

## Probability

A probability is a number between 0 and 1 for how likely something is. If a student remembers a fact with probability $p = 0.8$, they forget it with probability $1 - p = 0.2$. The probabilities of all possible outcomes add up to 1.

## Expected value

The **expected value** is the long-run average of a random quantity: each outcome times its probability, summed.

$$\mathbb{E}[X] = \sum_x x \cdot P(X = x)$$

For a fair die: $\frac{1+2+3+4+5+6}{6} = 3.5$. You never roll a 3.5, but the average of many rolls approaches it. That's the **law of large numbers**, and it's why an agent can learn from noisy experience.

## Averages that update themselves

You don't need to store every number to keep an average. After the $n$-th value $r$:

$$Q_n = Q_{n-1} + \frac{1}{n}\big(r - Q_{n-1}\big)$$

Read it as *new estimate = old estimate + step size × error*. When a reward is higher than expected, the estimate moves up a little; when lower, down a little. In Week 3 the bandit uses exactly this, and Q-learning swaps $\frac{1}{n}$ for a fixed step size $\alpha$.

## Simulation

When maths gets messy, simulate. `random.random() < p` is True with probability $p$. Re-Mind's whole Week 4 experiment is a simulation: thousands of fake students, each forgetting at random, so an agent can practise.
