"""Multi-armed bandits: the simplest RL problem (one state, many actions).

Story for Re-Mind: the tutor can quiz you in K styles (MCQ, fill-in-the-blank,
explain-in-your-own-words, ...). Each style has an unknown chance of actually
helping you learn. Which one should the tutor use?
"""
import math
import random


class BernoulliBandit:
    def __init__(self, probs, seed=None):
        self.probs = list(probs)
        self.rng = random.Random(seed)

    @property
    def k(self):
        return len(self.probs)

    def pull(self, arm):
        return 1.0 if self.rng.random() < self.probs[arm] else 0.0


class EpsilonGreedy:
    def __init__(self, k, epsilon=0.1, seed=None):
        self.counts, self.values = [0] * k, [0.0] * k
        self.epsilon, self.rng = epsilon, random.Random(seed)

    def select(self):
        if self.rng.random() < self.epsilon:
            return self.rng.randrange(len(self.values))
        return max(range(len(self.values)), key=lambda a: self.values[a])

    def update(self, arm, r):
        self.counts[arm] += 1
        self.values[arm] += (r - self.values[arm]) / self.counts[arm]   # running mean


class UCB1(EpsilonGreedy):
    def __init__(self, k, c=2.0, seed=None):
        super().__init__(k, 0.0, seed)
        self.c, self.t = c, 0

    def select(self):
        self.t += 1
        for a, n in enumerate(self.counts):
            if n == 0:
                return a
        return max(range(len(self.values)),
                   key=lambda a: self.values[a] + math.sqrt(self.c * math.log(self.t) / self.counts[a]))


def run(bandit, agent, steps=1000):
    best = max(bandit.probs)
    rewards, regret = [], []
    total_regret = 0.0
    for _ in range(steps):
        a = agent.select()
        r = bandit.pull(a)
        agent.update(a, r)
        total_regret += best - bandit.probs[a]
        rewards.append(r)
        regret.append(total_regret)
    return rewards, regret
