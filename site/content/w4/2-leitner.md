---
title: Rules first, Leitner boxes
minutes: 50
checkpoint:
  kind: browser
  title: Design your own rule
  prompt: "A policy maps (streak, last grade) to an action index into GAPS = [1, 2, 4, 7, 14, 30] days. Write `my_rule`. To pass, it must keep average recall above 90% with at most 16 reviews per concept over 60 days. Can you beat Leitner (93.3%, 10 reviews)?"
  modules: true
  starter: |
    from remind.env import GAPS, SpacedRepetitionEnv
    from remind.schedulers import evaluate, leitner, fixed

    FORGOT, HARD, EASY = 0, 1, 2

    def my_rule(streak, grade):
        return 2   # TODO: always 4 days for now. Make it depend on streak and grade.

    make_env = lambda seed: SpacedRepetitionEnv(seed=seed)
    for name, pol in [("every 4 days", fixed(4)), ("Leitner", leitner), ("my rule", my_rule)]:
        m = evaluate(pol, make_env, n=400)
        print(f"{name:13s} reviews {m['reviews']:5.1f}  recall {m['retention']:.1%}  exam {m['exam_pass']:.1%}")
  tests: |
    m = evaluate(my_rule, make_env, n=400, seed=99)
    assert m["retention"] > 0.90, f"recall {m['retention']:.1%} is below 90%"
    assert m["reviews"] <= 16, f"{m['reviews']:.1f} reviews per concept is above 16"
    print(f"passed: {m['retention']:.1%} recall with {m['reviews']:.1f} reviews")
quiz:
  - q: "In Leitner boxes, what happens after a wrong answer?"
    options: ["Move up a box", "Back to box 0 (shortest gap)", "Stay in the same box", "Remove the card"]
    answer: 1
    explain: "Failure resets the ladder."
  - q: "On our simulator Leitner keeps ~99% recall on easy concepts but ~81% on hard ones. Why?"
    options: ["Bug in Leitner", "One fixed ladder can't suit concepts that are forgotten at very different speeds", "Hard concepts are reviewed less", "The simulator is unfair"]
    answer: 1
    explain: "That gap is the opportunity for a learned policy."
  - q: "'Reviews per concept' measures..."
    options: ["recall", "effort", "difficulty", "reward"]
    answer: 1
    explain: "Good schedulers trade a little effort for a lot of recall."
  - q: "Reviewing every day gives 99.5% recall. Why isn't it the best scheduler?"
    options: ["It is", "It costs 60 reviews per concept: huge effort for a small gain", "It forgets more", "It can't be implemented"]
    answer: 1
    explain: "Recall without counting effort is a misleading goal. Remember this for reward hacking."
  - q: "Last year's 'level' metric in the handbook is..."
    options: ["unrelated", "essentially a Leitner box number", "a Q-value", "the API key"]
    answer: 1
    explain: "Level = consecutive correct answers = Leitner box."
resources:
  - label: Leitner system (Wikipedia)
    url: https://en.wikipedia.org/wiki/Leitner_system
  - label: SuperMemo SM-2 algorithm
    url: https://super-memory.com/english/ol/sm2.htm
  - label: Course notebook 01_forgetting_and_leitner.ipynb
    url: https://github.com/suff-yan/REMIND/blob/main/week4_spaced_repetition_rl/01_forgetting_and_leitner.ipynb
---
Before letting an agent learn, build the thing it has to beat.

## Leitner boxes

Picture index cards in six boxes. Box $k$ is reviewed after a fixed gap: **1, 2, 4, 7, 14, 30 days**. Get a card right and it moves up a box; get it wrong and it goes back to box 0. Last year's "level" metric was exactly this.

In code, a scheduler is just a **policy**: a function from what the tutor can see to an action.

```python
GAPS = [1, 2, 4, 7, 14, 30]

def leitner(streak, grade):
    return min(streak, len(GAPS) - 1)     # index into GAPS
```

## How to judge a scheduler

We simulate 2,000 students, each learning one concept on day 0 with an exam on day 60, and measure:

| Metric | Meaning |
|---|---|
| **Avg. recall** | average probability of remembering, over all 60 days |
| **Reviews / concept** | effort |
| **Exam pass** | remembered on day 60 |

| Scheduler | Reviews | Recall | Exam |
|---|---|---|---|
| every day | 60.0 | 99.5% | 100% |
| every 2 days | 30.0 | 97.0% | 98.8% |
| every 4 days | 15.0 | 83.3% | 81.8% |
| every week | 9.0 | 61.3% | 54.0% |
| **Leitner** | **10.0** | **93.3%** | **95.3%** |

Leitner is strong. Its weakness only shows when you split by difficulty: about 99% recall on easy concepts, 81% on hard ones. One ladder can't fit every concept, and a policy that adapts could do better.
