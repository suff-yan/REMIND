---
title: Reward hacking
minutes: 45
checkpoint:
  kind: browser
  title: Make the agent cheat
  prompt: "Write a reward that sounds reasonable but makes the trained agent do something absurd: review more than 25 times per concept, or fewer than 8. The check trains on your reward and looks at what the agent does."
  modules: true
  starter: |
    from remind.env import N_STATES, N_ACTIONS, SpacedRepetitionEnv
    from remind.rl.qlearning import QLearningAgent, train
    from remind.schedulers import evaluate, from_agent

    FORGOT, HARD, EASY = 0, 1, 2

    def my_reward(gap, grade):
        # TODO: something tempting, e.g. "+1 for every correct answer" or "longer gaps are better"
        return (gap if grade != FORGOT else -2 * gap) - 1   # (this is the GOOD reward; replace it)

    def train_with(reward_fn, episodes=10000):
        env = SpacedRepetitionEnv(seed=3, reward_mode=reward_fn)
        agent = QLearningAgent(N_STATES, N_ACTIONS, epsilon_decay=0.9995, seed=3)
        train(env, agent, episodes)
        return evaluate(from_agent(agent), lambda s: SpacedRepetitionEnv(seed=s), n=300)

    m = train_with(my_reward)
    print(f"reviews {m['reviews']:.1f}  recall {m['retention']:.1%}")
  tests: |
    m = train_with(my_reward)
    assert m["reviews"] > 25 or m["reviews"] < 8, f"{m['reviews']:.1f} reviews looks sensible; make the agent cheat"
    print(f"hacked! {m['reviews']:.1f} reviews, {m['retention']:.1%} recall. Explain why in your Week 4 write-up.")
quiz:
  - q: "Reward = +1 per correct answer. What does the agent learn?"
    options: ["The best schedule", "Quiz almost every day: easy points, huge workload", "Never quiz", "Random gaps"]
    answer: 1
    explain: "It maximises correct answers, not learning: 52.5 reviews per concept."
  - q: "Reward = the gap length. What does it learn?"
    options: ["Never quiz: waiting is free", "Quiz daily", "The Leitner ladder", "It can't learn"]
    answer: 0
    explain: "2.1 reviews per concept and 21.7% recall."
  - q: "Why do both hacks fail with the course's real reward?"
    options: ["They don't", "Forgetting costs −2·gap and every review costs −1, so neither extreme pays", "The reward is random", "Q-learning was changed"]
    answer: 1
    explain: "Each term closes one loophole."
  - q: "Which real-world system is a classic case of reward hacking?"
    options: ["A calculator", "A feed optimised for clicks that learns clickbait", "A thermostat", "A sorting algorithm"]
    answer: 1
    explain: "Optimise a proxy hard enough and it stops tracking what you meant."
  - q: "The Re-Mind Cup scores recall % minus reviews. Why that formula?"
    options: ["It's easy to compute", "Both hacks score badly under it, so winning requires genuinely good scheduling", "It's what Anki uses", "Random choice"]
    answer: 1
    explain: "Daily review scores ~40, never-review ~20, a good scheduler ~85."
resources:
  - label: DeepMind, specification gaming examples
    url: https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/
  - label: OpenAI, faulty reward functions in the wild (CoastRunners)
    url: https://openai.com/index/faulty-reward-functions/
  - label: The Re-Mind Cup
    url: /cup
---
RL optimises **exactly** what you reward, not what you meant. Two tempting rewards show it.

## "+1 for every correct answer"

Sounds right: we want correct answers! The agent learns to quiz you almost **every day** (52.5 reviews per concept). Quizzing tomorrow almost guarantees a correct answer, so it farms easy points. Recall is high; your evenings are gone.

## "Reward long gaps, they mean strong memory"

The agent finds the loophole immediately: **never quiz**. Waiting is free. 2.1 reviews per concept, and recall collapses to 21.7%.

## Why the course reward works

$$r = \begin{cases} +\,\text{gap} - 1 & \text{recalled} \\ -\,2\cdot\text{gap} - 1 & \text{forgot}\end{cases}$$

- **−1 per review** closes the daily-quiz loophole.
- **−2·gap on forgetting** closes the never-quiz loophole.
- **+gap on success** rewards long gaps only when they survive.

This isn't a toy problem. A feed that rewards clicks learns clickbait; a boat-racing agent learns to spin in circles collecting points. **Designing the reward is the most important decision you'll make in RL.** It's also why the [Re-Mind Cup](/cup) scores *recall minus reviews*: both hacks lose.
