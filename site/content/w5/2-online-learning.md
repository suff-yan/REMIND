---
title: From simulation to a real student
minutes: 60
checkpoint:
  kind: browser
  title: One live update
  prompt: "Write the heart of `Tutor.grade_and_learn`: given an item, a grade and the current time, compute the days actually waited, the reward, update the Q-table, update the item, and choose the next gap. One tutor 'day' lasts `day_seconds` seconds (60 in demo mode)."
  modules: true
  starter: |
    from remind.env import GAPS, N_STATES, N_ACTIONS, reward, state_id
    from remind.rl.qlearning import QLearningAgent

    def live_update(agent, item, grade, now, day_seconds=60):
        s = state_id(item["streak"], item["last_grade"])
        a = item["gap_action"]
        elapsed_days = 0.0                     # TODO: from item["last_review"] and now
        r = 0.0                                # TODO: reward("proven_days", elapsed_days, grade)
        # TODO: update item["streak"] (reset to 0 if grade == 0), item["last_grade"], item["last_review"]
        # TODO: agent.update(s, a, r, next_state, done=False)
        # TODO: choose the next action greedily, store it in item["gap_action"], set item["next_due"]
        return r

    agent = QLearningAgent(N_STATES, N_ACTIONS, epsilon=0.0, seed=0)
    item = {"streak": 0, "last_grade": 0, "last_review": 1000.0, "gap_action": 0, "next_due": 1060.0}
    print(live_update(agent, item, grade=2, now=1090.0), item)
  tests: |
    agent = QLearningAgent(N_STATES, N_ACTIONS, epsilon=0.0, alpha=0.5, seed=0)
    item = {"streak": 0, "last_grade": 0, "last_review": 1000.0, "gap_action": 0, "next_due": 1060.0}
    r = live_update(agent, item, grade=2, now=1090.0)
    assert abs(r - 0.5) < 1e-9, f"waited 1.5 days and recalled: reward should be 1.5 - 1 = 0.5, got {r}"
    assert item["streak"] == 1 and item["last_grade"] == 2 and item["last_review"] == 1090.0, item
    assert abs(agent.q[0][0] - 0.25) < 1e-9, agent.q[0]
    assert item["next_due"] == 1090.0 + GAPS[item["gap_action"]] * 60
    r2 = live_update(agent, item, grade=0, now=1090.0 + 3 * 60)
    assert abs(r2 - (-7.0)) < 1e-9 and item["streak"] == 0, (r2, item)
    print("live update works: this is the line that keeps the agent learning from you")
quiz:
  - q: "Why pre-train on simulated students before using the agent on a real one?"
    options: ["Real students are banned", "Learning from scratch on one human would take months of quizzes", "Simulation is more accurate", "Gemini requires it"]
    answer: 1
    explain: "Warm start in simulation, then fine-tune on the real student."
  - q: "Live, ε is set to about 0.05. Why not 0?"
    options: ["It's a bug", "A little exploration lets the agent discover this student differs from the simulated ones", "To slow it down", "To save tokens"]
    answer: 1
    explain: "Pure exploitation would never correct the simulator's biases."
  - q: "In demo mode, REMIND_DAY_SECONDS=60 means..."
    options: ["one tutor-day lasts one minute", "the app restarts every minute", "quizzes take 60 seconds", "nothing"]
    answer: 0
    explain: "Time travel for demos; set it back to 86400 for real use."
  - q: "The live reward uses the days actually waited, not the planned gap. Why?"
    options: ["The student may come back late or early; reward what really happened", "It's simpler", "The planned gap is secret", "No reason"]
    answer: 0
    explain: "If you open the app 3 days late and still remember, you proved 3 more days."
  - q: "Which is a real risk of online learning in Re-Mind?"
    options: ["None", "Gemini's grade is noisy, so a bad grade teaches the agent the wrong lesson", "The Q-table gets too big", "Streamlit forgets the agent"]
    answer: 1
    explain: "Discuss it in your report: it's one of the best failure cases to analyse."
resources:
  - label: Sim-to-real transfer (overview)
    url: https://lilianweng.github.io/posts/2019-05-05-domain-randomization/
  - label: remind/tutor.py, grade_and_learn
    url: https://github.com/suff-yan/REMIND/blob/main/remind/tutor.py
---
## Pre-train, then fine-tune on you

A Q-table learned from scratch on one human would need months of quizzes. So we **pre-train** on simulated students (`python scripts/train_scheduler.py`) and **fine-tune online** with a small ε of 0.05: the same idea as pre-training and fine-tuning an LLM.

That only works because the live tutor uses **the same 18 states and the same reward** as the simulator, built from what it can observe: the streak, Gemini's grade, and the real time elapsed.

## Time travel

Nobody waits 14 days for a demo. In `.env`:

```bash
REMIND_DAY_SECONDS=60     # one tutor-day = one minute
```

Set it back to 86400 to use Re-Mind for real.

## What could go wrong

- **Noisy rewards.** Gemini's grade is a measurement, not the truth. A harsh grade teaches the agent the wrong lesson.
- **The simulator is a cartoon.** A real student may forget faster or slower than any simulated one.
- **Few updates.** One student produces a handful of quizzes a day; the table changes slowly.

These are exactly the honest limitations your end-term report should discuss.
