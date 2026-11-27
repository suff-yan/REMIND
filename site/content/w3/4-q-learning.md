---
title: Q-learning
minutes: 80
video: w3_qlearning
videoTitle: Q-learning, cell by cell
checkpoint:
  kind: browser
  title: Teach the agent the study room
  prompt: "Implement the Q-learning update, then train for 1,500 episodes. The check runs your greedy policy and expects it to reach the exam without touching the phone."
  modules: true
  starter: |
    import random
    from remind.rl.gridworld import GridWorld

    env = GridWorld()
    Q = [[0.0] * 4 for _ in range(env.n_states)]
    alpha, gamma, epsilon = 0.1, 0.95, 1.0
    rng = random.Random(0)

    def act(s):
        if rng.random() < epsilon:
            return rng.randrange(4)
        return max(range(4), key=lambda a: Q[s][a])

    def update(s, a, r, s2, done):
        # TODO: target = r if done else r + gamma * max(Q[s2])
        # TODO: Q[s][a] += alpha * (target - Q[s][a])
        pass

    for ep in range(1500):
        s, done = env.reset(), False
        while not done:
            a = act(s)
            s2, r, done, _ = env.step(a)
            update(s, a, r, s2, done)
            s = s2
        epsilon = max(0.05, epsilon * 0.995)

    print(env.render_policy(Q))
  tests: |
    s, done, total = env.reset(), False, 0.0
    while not done:
        s, r, done, _ = env.step(max(range(4), key=lambda a: Q[s][a]))
        total += r
    assert total > 9, f"greedy return {total:.1f}; expected > 9 (reach G in a few steps)"
    print(f"greedy return {total:.1f}: the agent learned the path")
quiz:
  - q: "In the Q-learning target $r + \\gamma \\max_{a'} Q(s', a')$, what does the max do?"
    options: ["Picks the reward", "Assumes the agent will act as well as it currently can from the next state", "Explores randomly", "Ends the episode"]
    answer: 1
    explain: "It looks one step ahead and assumes the best known action afterwards."
  - q: "What's the target when the episode just ended (done = True)?"
    options: ["0", "just r", "r + γ max Q(s')", "max Q(s')"]
    answer: 1
    explain: "There is no future after the terminal step."
  - q: "What does α (alpha) control?"
    options: ["Exploration", "How far each estimate moves toward its target", "The discount", "The number of actions"]
    answer: 1
    explain: "Same role as 1/n in the running mean, but fixed."
  - q: "Why decay ε over episodes?"
    options: ["To save memory", "Explore a lot early, exploit what you've learned later", "Required by the gridworld", "To slow learning"]
    answer: 1
    explain: "Early on you know nothing; later, random moves mostly waste reward."
  - q: "Q-learning vs SARSA: Q-learning's target uses..."
    options: ["the action actually taken next", "the best action in the next state, whatever you do next", "a random action", "no next state"]
    answer: 1
    explain: "That makes Q-learning 'off-policy'. SARSA uses the action it actually took."
  - q: "The Q-table for the gridworld has how many numbers?"
    options: ["4", "16", "64", "256"]
    answer: 2
    explain: "16 states × 4 actions. Re-Mind's scheduler will have 18 × 6 = 108."
resources:
  - label: Sutton & Barto, chapter 6.5 (Q-learning)
    url: http://incompleteideas.net/book/the-book-2nd.html
  - label: Hugging Face Deep RL course, unit 2 (Q-learning)
    url: https://huggingface.co/learn/deep-rl-course/unit2/introduction
  - label: Course notebook 02_q_learning_gridworld.ipynb
    url: https://github.com/suff-yan/REMIND/blob/main/week3_rl_foundations/02_q_learning_gridworld.ipynb
---
## The update

Q-learning keeps a table of $Q(s, a)$ and, after every step, nudges one entry toward a better guess:

$$Q(s,a) \leftarrow Q(s,a) + \alpha\Big[\underbrace{r + \gamma \max_{a'} Q(s',a')}_{\text{target}} - Q(s,a)\Big]$$

It's the running mean from Week 0 again: *new = old + step × error*. Two differences: the step $\alpha$ is fixed, and the **target looks one step ahead**, using the agent's own current estimate of what comes next. Good values spread backwards from the goal, one update at a time. The animation shows exactly that.

## The whole algorithm

```python
def update(self, s, a, r, s_next, done):
    target = r if done else r + self.gamma * max(self.q[s_next])
    self.q[s][a] += self.alpha * (target - self.q[s][a])
```

Plus ε-greedy to choose actions, with ε decaying from 1 (pure exploration) to 0.05.

## Knobs

| Symbol | Meaning | Typical |
|---|---|---|
| $\alpha$ | how far each estimate moves | 0.1 |
| $\gamma$ | how much the future matters | 0.95 |
| $\varepsilon$ | how often to explore | 1 → 0.05 |

After about 400 episodes in the study room, the arrows settle into a shortest path that avoids both phones. Next week, the same 40 lines learn when to quiz a student.
