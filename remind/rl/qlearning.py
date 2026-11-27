"""Tabular Q-learning - the whole algorithm in ~40 lines."""
import json
import random


class QLearningAgent:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.95,
                 epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.9995, seed=None):
        self.q = [[0.0] * n_actions for _ in range(n_states)]
        self.n_actions = n_actions
        self.alpha, self.gamma = alpha, gamma
        self.epsilon, self.epsilon_min, self.epsilon_decay = epsilon, epsilon_min, epsilon_decay
        self.rng = random.Random(seed)

    def act(self, s, greedy=False):
        if not greedy and self.rng.random() < self.epsilon:
            return self.rng.randrange(self.n_actions)          # explore
        row = self.q[s]
        best = max(row)
        return self.rng.choice([a for a, v in enumerate(row) if v == best])  # exploit

    def update(self, s, a, r, s_next, done):
        target = r if done else r + self.gamma * max(self.q[s_next])
        self.q[s][a] += self.alpha * (target - self.q[s][a])

    def decay(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save(self, path):
        with open(path, "w") as f:
            json.dump({"q": self.q, "epsilon": self.epsilon}, f, indent=1)

    @classmethod
    def load(cls, path, **kw):
        with open(path) as f:
            data = json.load(f)
        agent = cls(len(data["q"]), len(data["q"][0]), **kw)
        agent.q, agent.epsilon = data["q"], kw.get("epsilon", data["epsilon"])
        return agent


def train(env, agent, episodes=20000, log_every=0):
    history = []
    for ep in range(episodes):
        s, done, total = env.reset(), False, 0.0
        while not done:
            a = agent.act(s)
            s2, r, done, _ = env.step(a)
            agent.update(s, a, r, s2, done)
            s, total = s2, total + r
        agent.decay()
        history.append(total)
        if log_every and (ep + 1) % log_every == 0:
            avg = sum(history[-log_every:]) / log_every
            print(f"episode {ep+1:>6}  avg return {avg:7.2f}  epsilon {agent.epsilon:.3f}")
    return history
