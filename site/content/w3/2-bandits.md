---
title: "Bandits: exploration vs exploitation"
minutes: 70
video: w3_bandit
videoTitle: The bandit's dilemma
checkpoint:
  kind: browser
  title: Build an epsilon-greedy agent
  prompt: "Four quiz styles help with unknown probabilities. Implement `select` (explore with probability epsilon, else pick the best estimate) and `update` (incremental mean). The check runs 3,000 quizzes and expects you to find the best style."
  modules: true
  starter: |
    import random
    from remind.rl.bandits import BernoulliBandit

    class EpsGreedy:
        def __init__(self, k, epsilon=0.1, seed=0):
            self.counts = [0] * k
            self.values = [0.0] * k
            self.epsilon = epsilon
            self.rng = random.Random(seed)

        def select(self):
            # TODO: with probability epsilon return a random arm, else the arm with the highest value
            return 0

        def update(self, arm, reward):
            # TODO: counts[arm] += 1, then move values[arm] toward reward by 1/counts[arm]
            pass

    styles = ["MCQ", "fill-blank", "explain", "true/false"]
    bandit = BernoulliBandit([0.35, 0.50, 0.70, 0.55], seed=1)
    agent = EpsGreedy(4)
    for _ in range(3000):
        a = agent.select()
        agent.update(a, bandit.pull(a))
    for s, n, v in zip(styles, agent.counts, agent.values):
        print(f"{s:10s} used {n:5d}  estimate {v:.2f}")
  tests: |
    best = max(range(4), key=lambda a: agent.counts[a])
    assert best == 2, f"expected 'explain' to be used most, got {styles[best]}"
    assert abs(agent.values[2] - 0.70) < 0.05, agent.values
    greedy = EpsGreedy(4, epsilon=0.0)
    assert greedy.select() == 0
    print("epsilon-greedy works")
quiz:
  - q: "A greedy agent (ε = 0) can get stuck forever on a bad arm. Why?"
    options: ["It forgets", "If the best arm is unlucky early, it never tries it again", "It always picks randomly", "It can't compute averages"]
    answer: 1
    explain: "Without exploration, early bad luck becomes permanent."
  - q: "With ε = 0.1, how often does the agent pick a random arm?"
    options: ["Never", "10% of the time", "90% of the time", "Every 10th step exactly"]
    answer: 1
    explain: "Each step, with probability 0.1."
  - q: "UCB adds $\\sqrt{c \\ln t / N(a)}$ to each estimate. What happens to an arm tried only a few times?"
    options: ["It gets a big bonus, so it's tried again", "It's ignored", "Its estimate is reset", "Nothing"]
    answer: 0
    explain: "Optimism in the face of uncertainty: explore where you're unsure, not at random."
  - q: "Regret measures..."
    options: ["how sad the agent is", "reward lost compared with always using the best arm", "the number of arms", "the learning rate"]
    answer: 1
    explain: "Flat regret = the agent has found the best arm."
  - q: "Why is a bandit 'RL with one state'?"
    options: ["It has one arm", "Actions don't change the situation; there's only 'which arm now?'", "It runs once", "It has one reward"]
    answer: 1
    explain: "No consequences carry over, which isolates exploration vs exploitation."
  - q: "The incremental update $Q \\leftarrow Q + \\frac{1}{n}(r - Q)$ after rewards 1, 0, 1 gives..."
    options: ["0.33", "0.5", "0.67", "1"]
    answer: 2
    explain: "It's just the average: 2/3."
resources:
  - label: Sutton & Barto, chapter 2 (bandits)
    url: http://incompleteideas.net/book/the-book-2nd.html
  - label: Lilian Weng, the multi-armed bandit problem
    url: https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/
  - label: Course notebook 01_bandits.ipynb
    url: https://github.com/suff-yan/REMIND/blob/main/week3_rl_foundations/01_bandits.ipynb
---
## The story

Re-Mind can quiz you in four styles: MCQ, fill-in-the-blank, true/false, explain-in-your-own-words. Each helps you remember with an unknown probability. Every quiz is one pull of a slot-machine arm. Over 1,000 quizzes, which style should the tutor use?

This is the **multi-armed bandit**: RL with one state. Nothing you do changes the situation; you just keep choosing. It isolates the most important tension in RL.

## Exploration vs exploitation

- **Exploit:** use the arm that looks best so far.
- **Explore:** try another arm in case it's actually better.

Only exploiting is a trap: if the best arm is unlucky in its first few pulls, a greedy agent never touches it again.

## Estimating an arm's value

The running mean from Week 0, again:

$$Q_{n+1}(a) = Q_n(a) + \frac{1}{n}\big(r - Q_n(a)\big)$$

## Three strategies

| Strategy | Rule |
|---|---|
| **Greedy** | always $\arg\max_a Q(a)$ |
| **ε-greedy** | random arm with probability ε, else greedy |
| **UCB** | $\arg\max_a\; Q(a) + \sqrt{\frac{c \ln t}{N(a)}}$: a bonus for arms you've rarely tried |

**Regret** is how much reward you lost compared with always using the best arm. Greedy's regret grows forever; ε-greedy and UCB flatten out once they've found the best arm.
