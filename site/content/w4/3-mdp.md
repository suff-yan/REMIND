---
title: Spaced repetition as an RL problem
minutes: 50
checkpoint:
  kind: browser
  title: State and reward
  prompt: "Implement the two functions that turn the problem into RL. State: streak (capped at 5) times 3 plus the last grade, giving 18 states. Reward: +gap − 1 if recalled, −2·gap − 1 if forgotten."
  starter: |
    FORGOT, HARD, EASY = 0, 1, 2

    def state_id(streak, grade):
        return 0  # TODO: min(streak, 5) * 3 + grade

    def reward(gap, grade, review_cost=1.0, fail_weight=2.0):
        return 0.0  # TODO

    print(state_id(2, EASY), reward(7, EASY), reward(7, FORGOT))
  tests: |
    from remind import env as E
    for s in range(8):
        for g in range(3):
            assert state_id(s, g) == E.state_id(s, g), (s, g)
    assert len({state_id(s, g) for s in range(6) for g in range(3)}) == 18
    for gap in [1, 2, 4, 7, 14, 30]:
        for g in range(3):
            assert reward(gap, g) == E.reward("proven_days", gap, g), (gap, g)
    print("state and reward match the environment")
quiz:
  - q: "In Re-Mind's MDP, an episode is..."
    options: ["one chat message", "one concept, from the day it's learned to an exam on day 60", "one student's whole degree", "one Gemini call"]
    answer: 1
    explain: "Each concept is scheduled independently."
  - q: "Why is the state (streak, last grade) and not the true stability S?"
    options: ["S is hidden; a real tutor only observes answers", "S is too big", "It's faster", "Q-learning can't use numbers"]
    answer: 0
    explain: "Design the agent around what you can actually observe."
  - q: "Waited 14 days and still remembered. Reward?"
    options: ["+1", "+13", "+14", "−29"]
    answer: 1
    explain: "+gap − 1 = 14 − 1."
  - q: "Waited 14 days and forgot. Reward?"
    options: ["−1", "−14", "−29", "0"]
    answer: 2
    explain: "−2·14 − 1 = −29. Forgetting costs double."
  - q: "What does the −1 per review represent?"
    options: ["A bug", "Effort: every quiz costs the student time", "The discount", "The learning rate"]
    answer: 1
    explain: "Without it, more reviews are always better."
  - q: "How many numbers are in the scheduler's Q-table?"
    options: ["18", "36", "108", "360"]
    answer: 2
    explain: "18 states × 6 actions."
resources:
  - label: Reddy et al., Unbounded human learning (RL for spaced repetition)
    url: https://arxiv.org/abs/1602.07032
  - label: remind/env.py in the repo
    url: https://github.com/suff-yan/REMIND/blob/main/remind/env.py
---
## The MDP

| Piece | Re-Mind |
|---|---|
| **Episode** | one concept, from the day it's learned (day 0) to an exam on day 60 |
| **State** | (correct-in-a-row streak 0–5, last grade forgot/hard/easy): 18 states |
| **Action** | wait 1, 2, 4, 7, 14 or 30 days before the next quiz |
| **Environment** | the simulated student (`remind/env.py`, gym-style `reset` / `step`) |

The state contains only what a real tutor can observe: never the hidden difficulty or stability. A policy that peeks at hidden variables would be useless in the live app.

## Designing the reward

$$r = \begin{cases} +\,\text{gap} - c & \text{recalled} \\ -\,2\cdot\text{gap} - c & \text{forgot}\end{cases} \qquad c = 1$$

*If you waited 14 days and still remembered, you proved 14 days of memory.* Forgetting costs double, and every review costs a little effort. The agent wants gaps that are as long as possible **and** still survive. Every part of this formula is there to stop a specific kind of cheating, which you'll see in section 5.
