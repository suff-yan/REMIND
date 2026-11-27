---
title: "Maths II: exponential decay and geometric sums"
minutes: 70
checkpoint:
  kind: browser
  title: Forgetting and discounting
  prompt: "Fill in three small functions. They are, almost word for word, the maths inside Re-Mind's simulator (Week 4) and RL agent (Week 3)."
  starter: |
    import math

    def recall(t, S):
        """Probability of remembering after t days, with stability S (days until 90%)."""
        return 0.0  # TODO: 0.9 ** (t / S)

    def days_until(p, S):
        """How many days until recall drops to probability p? Solve 0.9 ** (t / S) = p for t."""
        return 0.0  # TODO: use math.log

    def discounted_return(rewards, gamma):
        """r0 + gamma*r1 + gamma**2*r2 + ..."""
        total = 0.0
        # TODO
        return total

    print(recall(7, 7), days_until(0.5, 10), discounted_return([1, 1, 1], 0.5))
  tests: |
    assert abs(recall(7, 7) - 0.9) < 1e-9
    assert abs(recall(0, 3) - 1.0) < 1e-9
    assert abs(days_until(0.9, 5) - 5) < 1e-9
    assert abs(days_until(0.5, 10) - 65.788) < 0.01, days_until(0.5, 10)
    assert abs(discounted_return([1, 1, 1], 0.5) - 1.75) < 1e-9
    assert abs(discounted_return([1] * 500, 0.9) - 10) < 1e-6
    print("all three work")
quiz:
  - q: "Recall follows $P = 0.9^{t/S}$. With $S = 10$, what is recall at $t = 10$ days?"
    options: ["0.1", "0.5", "0.9", "1.0"]
    answer: 2
    explain: "At t = S the exponent is 1, so P = 0.9. That's what stability means."
  - q: "If stability S doubles, the memory..."
    options: ["fades twice as fast", "fades half as fast", "is forgotten immediately", "doesn't change"]
    answer: 1
    explain: "t/S halves, so it takes twice as long to reach any given recall level."
  - q: "What is $1 + \\frac{1}{2} + \\frac{1}{4} + \\frac{1}{8} + \\dots$ forever?"
    options: ["1.5", "2", "Infinity", "4"]
    answer: 1
    explain: "Geometric series: 1 / (1 − ½) = 2."
  - q: "With discount $\\gamma = 0.9$, a reward of 1 every step forever is worth..."
    options: ["0.9", "1", "10", "Infinity"]
    answer: 2
    explain: "1 / (1 − 0.9) = 10. Discounting keeps endless futures finite."
  - q: "Which gamma makes an agent care most about the far future?"
    options: ["0", "0.5", "0.9", "0.99"]
    answer: 3
    explain: "Closer to 1 means future rewards shrink slowly, so they still matter."
  - q: "To solve $0.9^{x} = 0.5$ for $x$ you use..."
    options: ["a square root", "a logarithm: x = log(0.5) / log(0.9)", "division: 0.5 / 0.9", "it can't be solved"]
    answer: 1
    explain: "Logs turn exponents into multiplication: x·log(0.9) = log(0.5)."
resources:
  - label: 3Blue1Brown, what's so special about Euler's number e?
    url: https://www.youtube.com/watch?v=m2MIpDrF7Es
  - label: Khan Academy, geometric series
    url: https://www.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:poly-factor/x2ec2f6f830c9fb89:geo-series/v/geometric-series-sum
  - label: Desmos (plot 0.9^(x/S) and drag S)
    url: https://www.desmos.com/calculator
---
## Exponential decay: the shape of forgetting

Some things shrink by the same **fraction** every day: radioactivity, the value of money, and memory. If you keep 90% of what's left after each stretch of $S$ days:

$$P(\text{recall after } t \text{ days}) = 0.9^{\,t/S}$$

$S$ is **stability**: the number of days until recall drops to 90%. Big $S$, slow forgetting. Plot it in Desmos with a slider for $S$ and you'll see the whole of Week 4 in one picture: reviews make $S$ jump, which flattens the curve.

## Logarithms undo exponents

"When will recall hit 50%?" means solving $0.9^{t/S} = 0.5$. Take logs of both sides:

$$t = S \cdot \frac{\log 0.5}{\log 0.9}$$

With $S = 10$, that's about 66 days. A scheduler that wants you to review "just before you'd forget" is doing exactly this calculation.

## Geometric sums: why the future is finite

In RL an agent adds up future rewards, but a reward tomorrow is worth a little less than one today. Multiply each step by a **discount** $\gamma$ (gamma) between 0 and 1:

$$G = r_0 + \gamma r_1 + \gamma^2 r_2 + \gamma^3 r_3 + \dots$$

If every reward is 1, this is a geometric series:

$$1 + \gamma + \gamma^2 + \dots = \frac{1}{1-\gamma}$$

With $\gamma = 0.9$, an endless stream of 1s is worth exactly 10. That's how an agent can compare futures that never end. $\gamma$ near 1 is a patient agent; near 0, an impatient one.
