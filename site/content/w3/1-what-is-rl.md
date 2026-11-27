---
title: What is reinforcement learning?
minutes: 40
checkpoint:
  kind: browser
  title: Your first agent-environment loop
  prompt: "`GridWorld` is the study room from this week: reach the exam (+10), avoid your phone (−5), −0.1 per step. Write `run_episode` that plays one episode with a given policy and returns the total reward. Then compare a random policy with a hand-written one."
  modules: true
  starter: |
    import random
    from remind.rl.gridworld import GridWorld, LAYOUT
    print("\n".join(LAYOUT))

    def run_episode(env, policy):
        total = 0.0
        state = env.reset()
        done = False
        # TODO: while not done: pick action = policy(state), step, add reward
        return total

    rng = random.Random(0)
    random_policy = lambda s: rng.randrange(4)          # 0 up, 1 down, 2 left, 3 right
    env = GridWorld()
    print("random:", sum(run_episode(env, random_policy) for _ in range(200)) / 200)
  tests: |
    path = {0: 3, 1: 3, 2: 1, 6: 1, 10: 1, 14: 3}       # right, right, down x3, right
    assert abs(run_episode(GridWorld(), lambda s: path.get(s, 1)) - 9.5) < 1e-9
    assert abs(run_episode(GridWorld(), lambda s: 1) - (-5.2)) < 1e-9   # two steps down, then the phone
    print("run_episode works")
quiz:
  - q: "What does an RL agent get told after each action?"
    options: ["The correct action", "A reward: how good that was", "The full map", "Nothing"]
    answer: 1
    explain: "Unlike supervised learning, RL never sees the right answer, only a reward."
  - q: "In Re-Mind, the environment is..."
    options: ["Gemini", "the student (real or simulated)", "Streamlit", "the JSON file"]
    answer: 1
    explain: "The scheduler (agent) acts on the student (environment) by choosing when to quiz."
  - q: "A policy is..."
    options: ["the reward function", "the agent's rule for choosing an action in each state", "the environment's map", "a learning rate"]
    answer: 1
    explain: "π(s) → a."
  - q: "Why must an RL agent explore?"
    options: ["To waste time", "Because it's never told the best action, so it has to try things to find out", "To use more memory", "It doesn't need to"]
    answer: 1
    explain: "No exploration, no discovery of better actions."
  - q: "`env.step(action)` returns..."
    options: ["only the reward", "next_state, reward, done, info", "a new policy", "the Q-table"]
    answer: 1
    explain: "The gym-style interface used everywhere in this course."
resources:
  - label: Sutton & Barto, RL An Introduction, chapter 1 (free)
    url: http://incompleteideas.net/book/the-book-2nd.html
  - label: David Silver, RL lecture 1 (video)
    url: https://www.youtube.com/watch?v=2pWv7GOvuf0
  - label: Hugging Face Deep RL course, unit 1
    url: https://huggingface.co/learn/deep-rl-course/unit1/introduction
---
## The one idea

Supervised learning is told the right answer. **Reinforcement learning is never told the right answer**, only how good its choice was, and often much later. So it has to try things, and the way you score its tries (the reward) decides what it learns.

## Five words

| Term | Meaning | In Re-Mind |
|---|---|---|
| **Agent** | the decision maker | the scheduler |
| **Environment** | everything else | the student |
| **State** $s$ | what the agent knows now | streak + last grade |
| **Action** $a$ | what it can do | wait 1, 2, 4, 7, 14 or 30 days |
| **Reward** $r$ | how good that was | days of memory proved |

A **policy** $\pi(s)$ is the agent's strategy: which action in each state. Learning means improving the policy.

## The loop

Every RL program has this shape. It's in `remind/rl/qlearning.py`, and you'll write it yourself in the checkpoint:

```python
state = env.reset()
while not done:
    action = agent.act(state)
    next_state, reward, done, info = env.step(action)
    agent.update(state, action, reward, next_state, done)
    state = next_state
```

## The study-room gridworld

```
S . . .     S = start, G = exam hall (+10)
. # . X     # = wall, X = phone (-5, episode ends)
. . . .     every step costs -0.1
X . . G
```

A random policy scores badly: it wanders, and often picks up the phone. By the end of this week you'll have an agent that learns the shortest safe path by itself.
