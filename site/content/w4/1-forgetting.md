---
title: Forgetting curves and a simulated student
minutes: 60
video: w4_forgetting
videoTitle: Forgetting and Leitner boxes
checkpoint:
  kind: browser
  title: Write the memory model
  prompt: "Implement one review of the simulated student. Recall probability after waiting `t` days is `0.9 ** (t / S)`. If recalled, stability grows by `1 + (2 - 1.8*d) * (1 + 2*(1 - p))` (capped at 365); if forgotten it halves (floor 0.2). The check compares you with `remind/memory_model.py`."
  modules: true
  starter: |
    def p_recall(t, S):
        return 0.0  # TODO

    def new_stability(S, d, t, recalled):
        p = p_recall(t, S)
        # TODO
        return S

    S = 1.0
    for gap, ok in [(1, True), (3, True), (7, False), (2, True)]:
        S = new_stability(S, d=0.4, t=gap, recalled=ok)
        print(f"after waiting {gap} d, {'recalled' if ok else 'forgot'}: S = {S:.2f}")
  tests: |
    import random
    from remind.memory_model import SimulatedStudent, recall_probability
    assert abs(p_recall(5, 5) - recall_probability(5, 5)) < 1e-12
    rng = random.Random(7)
    for _ in range(300):
        d, S, t = rng.random(), rng.uniform(0.2, 50), rng.choice([1, 2, 4, 7, 14, 30])
        st = SimulatedStudent(difficulty=d, rng=random.Random(1)); st.stability = S
        grade, p = st.review(t)
        assert abs(new_stability(S, d, t, grade > 0) - st.stability) < 1e-9, (S, d, t)
    print("your model matches the simulator")
quiz:
  - q: "With $P = 0.9^{t/S}$, what does a stability of S = 14 mean?"
    options: ["The item is forgotten after 14 days", "Recall drops to 90% after 14 days", "It needs 14 reviews", "Recall is 14%"]
    answer: 1
    explain: "S is the number of days until recall falls to 90%."
  - q: "In the simulator, when does a successful review grow stability the most?"
    options: ["When recall was easy (p near 1)", "When recall was hard (p low) but still succeeded", "When the item is difficult", "Never"]
    answer: 1
    explain: "The (1 + 2(1 − p)) factor: desirable difficulty. Reviewing too early teaches little."
  - q: "Why can't the scheduler use the student's difficulty d directly?"
    options: ["It's hidden: a real tutor can't observe it", "It's always 0.5", "Python can't store it", "It changes every second"]
    answer: 0
    explain: "The agent only sees what a real tutor could: streak and grade."
  - q: "Why build a simulated student at all?"
    options: ["Real students are boring", "The agent needs thousands of practice episodes, which no human could provide", "It's required by Streamlit", "To avoid using Gemini"]
    answer: 1
    explain: "40,000 simulated students train in seconds; then the agent fine-tunes on you."
  - q: "Which statement about this simulator is honest?"
    options: ["It's an exact model of the brain", "It's a simplified cousin of FSRS: a sandbox, not science", "It was fitted to IITB students", "It never forgets"]
    answer: 1
    explain: "Good enough to learn from; your report should discuss its limits."
resources:
  - label: Open Spaced Repetition (FSRS), the algorithm behind modern Anki
    url: https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm
  - label: Gwern, Spaced repetition for efficient learning
    url: https://gwern.net/spaced-repetition
  - label: Nicky Case, How to remember anything forever-ish (interactive)
    url: https://ncase.me/remember/
    note: the best interactive explainer on the topic
---
## yapping about why you should try out this method

Imagine your brain is a leaky bucket. You pour knowledge in and some immediately starts dripping out. Spaced repetition is pouring water back in right before it empties, again and again, until the bucket stops leaking so much. Review too soon and you learn almost nothing; wait too long and you relearn from scratch. The sweet spot is when recall feels *slightly uncomfortable*. Forgetting is not the enemy; forgetting is the teacher.

## The forgetting curve

$$P(\text{recall after } t \text{ days}) = 0.9^{\,t/S}$$

**Stability** $S$ is the number of days until recall drops to 90%. Each successful review makes $S$ jump, which flattens the curve so the next gap can be longer.

## The simulated student

`remind/memory_model.py` simulates one student learning one concept with hidden difficulty $d \in [0, 1]$:

- quizzed after waiting $t$ days, they recall with probability $p = 0.9^{t/S}$;
- **recalled:** $S \leftarrow S \cdot \big(1 + (2 - 1.8d)(1 + 2(1-p))\big)$. Memory grows, and grows **more** when recall was hard (low $p$). That's the uncomfortable sweet spot, in maths;
- **forgot:** $S \leftarrow 0.5\,S$;
- they report *forgot / hard / easy*: the same three grades Gemini gives in Week 5.

It's a simplified cousin of FSRS, the algorithm in modern Anki: a sandbox for an agent to practise in, not a scientific model of your brain.

## A short history of schedulers

Fixed calendars (1, 3, 7 days) → Leitner boxes (next box on success) → SM-2 ease factors (Anki, 1987) → forgetting-curve models → FSRS, which learns its parameters from your data. This project takes one more step: **let an RL agent learn the rule itself**.
