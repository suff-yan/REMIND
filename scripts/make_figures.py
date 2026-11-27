"""Regenerate every teaching figure used in the handbook and slides -> assets/"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from remind.memory_model import SimulatedStudent, recall_probability
from remind.rl.bandits import BernoulliBandit, EpsilonGreedy, UCB1, run
from remind.rl.gridworld import GridWorld
from remind.rl.qlearning import QLearningAgent, train
from remind.env import SpacedRepetitionEnv, N_STATES, N_ACTIONS

os.makedirs("assets", exist_ok=True)
NAVY, GREY, RED = "#1f4e79", "#777777", "#b03030"


def smooth(x, k=200):
    out, s = [], 0.0
    for i, v in enumerate(x):
        s += v
        if i >= k:
            s -= x[i - k]
        out.append(s / min(i + 1, k))
    return out


# 1. forgetting curve with and without reviews
fig, ax = plt.subplots(figsize=(6.4, 3.4))
days = [d / 10 for d in range(0, 301)]
ax.plot(days, [100 * recall_probability(d, 1.5) for d in days], c=GREY, ls="--", label="no review")
st = SimulatedStudent(difficulty=0.4, rng=random.Random(3))
t_last, xs, ys, reviews = 0, [], [], [1, 3, 7, 14, 30]
for d in days:
    if reviews and d >= reviews[0]:
        st.review(reviews.pop(0) - t_last); t_last = d
    xs.append(d); ys.append(100 * st.p_recall(d - t_last))
ax.plot(xs, ys, c=NAVY, label="reviews on day 1, 3, 7, 14, 30")
ax.set_xlabel("days since learning"); ax.set_ylabel("recall probability (%)")
ax.set_title("Each review flattens the forgetting curve"); ax.legend(); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig("assets/forgetting_curve.png", dpi=200); plt.close(fig)

# 2. bandit regret
fig, ax = plt.subplots(figsize=(6.4, 3.4))
probs = [0.35, 0.50, 0.70, 0.55]
for name, mk, c in [("greedy (eps=0)", lambda: EpsilonGreedy(4, 0.0, seed=1), RED),
                    ("eps-greedy (0.1)", lambda: EpsilonGreedy(4, 0.1, seed=1), GREY),
                    ("UCB1", lambda: UCB1(4, seed=1), NAVY)]:
    avg = [0.0] * 2000
    for run_id in range(50):
        _, reg = run(BernoulliBandit(probs, seed=run_id), mk(), 2000)
        avg = [a + r / 50 for a, r in zip(avg, reg)]
    ax.plot(avg, label=name, c=c)
ax.set_xlabel("quizzes given"); ax.set_ylabel("cumulative regret")
ax.set_title("Which quiz style? Exploration pays off"); ax.legend(); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig("assets/bandit_regret.png", dpi=200); plt.close(fig)

# 3. gridworld learning curve
env = GridWorld(); ag = QLearningAgent(env.n_states, env.n_actions, seed=0, epsilon_decay=0.995)
curve = train(env, ag, 1500)
with open("assets/gridworld_policy.txt", "w") as f:
    f.write(env.render_policy(ag.q))
fig, ax = plt.subplots(figsize=(6.4, 3.0))
ax.plot(smooth(curve, 50), c=NAVY); ax.set_xlabel("episode"); ax.set_ylabel("return (smoothed)")
ax.set_title("Q-learning in the study-room gridworld"); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig("assets/gridworld_curve.png", dpi=200); plt.close(fig)

# 4. scheduler learning curve
env = SpacedRepetitionEnv(seed=1)
ag = QLearningAgent(N_STATES, N_ACTIONS, seed=1, epsilon_decay=0.9998)
curve = train(env, ag, 40000)
fig, ax = plt.subplots(figsize=(6.4, 3.0))
ax.plot(smooth(curve, 500), c=NAVY); ax.axhline(0, c=GREY, lw=.8)
ax.set_xlabel("simulated students (episodes)"); ax.set_ylabel("return (smoothed)")
ax.set_title("The RL scheduler learning on simulated students"); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig("assets/scheduler_curve.png", dpi=200); plt.close(fig)
print("figures written to assets/"); print(open("assets/gridworld_policy.txt").read())
