---
title: MDPs, returns and discounting
minutes: 50
checkpoint:
  kind: browser
  title: Returns from every step
  prompt: "Given one episode's rewards, compute the return $G_t$ from every step $t$. Do it in one backwards pass using $G_t = r_t + \\gamma G_{t+1}$."
  starter: |
    def returns(rewards, gamma):
        G = [0.0] * len(rewards)
        # TODO: loop backwards; running = r + gamma * running
        return G

    print(returns([0, 0, 1], 0.9))
  tests: |
    r = returns([0, 0, 1], 0.9)
    assert [round(x, 4) for x in r] == [0.81, 0.9, 1.0], r
    assert returns([], 0.5) == []
    r = returns([-0.1] * 5 + [10], 0.95)
    assert abs(r[0] - (sum(-0.1 * 0.95 ** i for i in range(5)) + 10 * 0.95 ** 5)) < 1e-9
    print("returns works")
quiz:
  - q: "What makes an MDP different from a bandit?"
    options: ["It has rewards", "Actions change the state, so choices have consequences later", "It uses neural networks", "It has more arms"]
    answer: 1
    explain: "Walking right now changes where you are next."
  - q: "$G_t = r_t + \\gamma G_{t+1}$. With $\\gamma = 0$, the agent cares about..."
    options: ["only the immediate reward", "only the final reward", "all rewards equally", "nothing"]
    answer: 0
    explain: "Every future term is multiplied by 0."
  - q: "$Q(s, a)$ is..."
    options: ["the reward for (s, a)", "the expected return after taking a in s and acting well afterwards", "the probability of a", "the number of visits"]
    answer: 1
    explain: "It includes everything that follows, not just the next reward."
  - q: "If you knew the true Q-values, the best policy would be..."
    options: ["random", "$\\pi(s) = \\arg\\max_a Q(s, a)$", "always the first action", "the action with most visits"]
    answer: 1
    explain: "Just pick the best-valued action in each state."
  - q: "Why does a −0.1 per-step cost make the gridworld agent find short paths?"
    options: ["It doesn't", "Every extra step lowers the return, so shorter routes are worth more", "The map changes", "Walls get removed"]
    answer: 1
    explain: "Reward design shapes behaviour. Week 4 is all about this."
resources:
  - label: Sutton & Barto, chapter 3 (MDPs)
    url: http://incompleteideas.net/book/the-book-2nd.html
  - label: David Silver, lecture 2 (MDPs)
    url: https://www.youtube.com/watch?v=lfHX2hHRMVQ
---
## When actions have consequences

In a bandit, pulling an arm doesn't change anything. In most problems it does: walk right and you're somewhere new; quiz a student today and their memory is different tomorrow. That's a **Markov Decision Process (MDP)**: states, actions, rewards, transitions between states, and a discount $\gamma$.

## Return

The agent doesn't maximise the next reward; it maximises the **return**, the discounted sum of everything that follows:

$$G_t = r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + \dots = r_t + \gamma\, G_{t+1}$$

That last form is the trick: you can compute every return in one backwards pass.

## Values

$Q(s, a)$ is the expected return if you take action $a$ in state $s$ and act well afterwards. If you knew $Q$, acting would be trivial:

$$\pi(s) = \arg\max_a Q(s, a)$$

The rest of the week is about learning $Q$ from experience, without being told it.
