---
title: Training the scheduler
minutes: 70
video: w4_scheduler
videoTitle: Teaching a scheduler, and watching it cheat
checkpoint:
  kind: browser
  title: Train it in your browser
  prompt: "Write the training loop (the same six lines as in Week 3) and train on 15,000 simulated students. Takes a few seconds. To pass, your agent must beat 93% average recall."
  modules: true
  starter: |
    from remind.env import GAPS, N_STATES, N_ACTIONS, SpacedRepetitionEnv, state_id
    from remind.rl.qlearning import QLearningAgent
    from remind.schedulers import evaluate, from_agent, leitner

    env = SpacedRepetitionEnv(seed=1)
    agent = QLearningAgent(N_STATES, N_ACTIONS, alpha=0.1, gamma=0.95, epsilon_decay=0.9996, seed=1)

    for episode in range(15000):
        s, done = env.reset(), False
        # TODO: while not done -> act, step, update
        agent.decay()

    make_env = lambda seed: SpacedRepetitionEnv(seed=seed)
    for name, pol in [("Leitner", leitner), ("RL agent", from_agent(agent))]:
        m = evaluate(pol, make_env, n=500)
        print(f"{name:9s} reviews {m['reviews']:5.1f}  recall {m['retention']:.1%}  exam {m['exam_pass']:.1%}")
    print("learned gaps (days) for streak 0..5 after an 'easy' answer:",
          [GAPS[agent.act(state_id(k, 2 if k else 0), greedy=True)] for k in range(6)])
  tests: |
    m = evaluate(from_agent(agent), make_env, n=500, seed=77)
    assert m["retention"] > 0.93, f"recall {m['retention']:.1%}: did the loop call agent.update?"
    print(f"passed: {m['retention']:.1%} recall with {m['reviews']:.1f} reviews")
quiz:
  - q: "On 2,000 fresh simulated students the course RL agent got 96.8% recall with 11.8 reviews. Leitner got 93.3% with 10. Which is fair?"
    options: ["RL is strictly better in every way", "RL halves forgotten time for about two extra reviews", "Leitner is better", "They're identical"]
    answer: 1
    explain: "Forgotten time 6.7% → 3.2%, for ~1.8 more reviews. Honest comparisons name the trade-off."
  - q: "RL matches 'review every 2 days' (97.0%) with how much effort?"
    options: ["Same 30 reviews", "About 60% fewer reviews", "Double", "Zero"]
    answer: 1
    explain: "11.8 vs 30 reviews."
  - q: "The learned policy roughly says..."
    options: ["always wait 30 days", "drill a new concept daily until the streak is solid, then jump to long gaps", "random gaps", "always 4 days"]
    answer: 1
    explain: "Different from Leitner's smooth ladder."
  - q: "Some cells of the learned policy look odd. Most likely reason?"
    options: ["A bug in Python", "Rarely visited states get few updates, so their values stay noisy", "The GPU", "Gemini"]
    answer: 1
    explain: "Train with several seeds and compare; that's a Week 4 exercise."
  - q: "Why test on fresh students with a different seed?"
    options: ["It's faster", "To check the agent generalises, not just memorises its training students", "Seeds don't matter", "Python needs it"]
    answer: 1
    explain: "Same reason the Cup uses hidden students."
resources:
  - label: Course notebook 02_rl_scheduler.ipynb
    url: https://github.com/suff-yan/REMIND/blob/main/week4_spaced_repetition_rl/02_rl_scheduler.ipynb
  - label: "Duolingo: A trainable spaced repetition model (Settles & Meeder, 2016)"
    url: https://aclanthology.org/P16-1174/
---
## Training

Tabular Q-learning, exactly as in the gridworld, on 40,000 simulated students: $\alpha = 0.1$, $\gamma = 0.95$, $\varepsilon$ decaying to 0.05. About five seconds on a laptop, no GPU.

```bash
python scripts/train_scheduler.py      # writes data/q_table.json
python scripts/benchmark.py            # the table and plot below
```

## Results on 2,000 fresh students

| Scheduler | Reviews / concept | Avg. recall | Exam pass |
|---|---|---|---|
| every 2 days | 30.0 | 97.0% | 98.8% |
| every 4 days | 15.0 | 83.3% | 81.8% |
| Leitner boxes | 10.0 | 93.3% | 95.3% |
| **RL scheduler** | **11.8** | **96.8%** | **98.4%** |

The RL agent matches "every 2 days" with **60% fewer reviews**, and halves the forgotten time compared with Leitner for about two extra reviews per concept.

## What did it learn?

| streak | after "hard" | after "easy" |
|---|---|---|
| 0 (just forgot / new) | 1 day | 1 day |
| 1–2 | 1 | 1 |
| 3 | 4 | 1 |
| 4 | 1 | 4 |
| 5 | 4 | 14 |

Roughly: *drill a new concept daily until it has a solid streak, then jump to long gaps.* Some cells look odd: rarely visited states get few updates. That's a great discussion for the weekly meet.
