"""Compare schedulers on 2000 fresh simulated students + show reward hacking.

    python scripts/benchmark.py            # prints a table, writes assets/*.png
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from remind.env import N_ACTIONS, N_STATES, SpacedRepetitionEnv
from remind.rl.qlearning import QLearningAgent, train
from remind.schedulers import evaluate, fixed, from_agent, leitner

EPISODES = 40000


def trained(mode, seed=1):
    env = SpacedRepetitionEnv(seed=seed, reward_mode=mode)
    agent = QLearningAgent(N_STATES, N_ACTIONS, seed=seed, epsilon_decay=0.9998)
    curve = train(env, agent, EPISODES)
    return agent, curve


if __name__ == "__main__":
    make_env = lambda seed: SpacedRepetitionEnv(seed=seed)
    results = {}
    for name, pol in [("Every day", fixed(1)), ("Every 2 days", fixed(2)), ("Every 4 days", fixed(4)),
                      ("Every week", fixed(7)), ("Leitner boxes", leitner)]:
        results[name] = evaluate(pol, make_env)
    curves = {}
    for mode, label in [("proven_days", "RL (good reward)"),
                        ("correct_count", "RL (+1 per correct)"),
                        ("long_gaps", "RL (+gap length)")]:
        agent, curves[label] = trained(mode)
        results[label] = evaluate(from_agent(agent), make_env)

    print(f"{'policy':22s} {'reviews':>8} {'retention':>10} {'exam pass':>10}")
    for k, v in results.items():
        print(f"{k:22s} {v['reviews']:8.1f} {v['retention']:10.1%} {v['exam_pass']:10.1%}")
    os.makedirs("assets", exist_ok=True)
    with open("assets/benchmark.json", "w") as f:
        json.dump(results, f, indent=2)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6.4, 4.2))
        for k, v in results.items():
            hacked = "+1" in k or "+gap" in k
            ax.scatter(v["reviews"], v["retention"] * 100, s=70,
                       marker="x" if hacked else ("*" if k.startswith("RL") else "o"),
                       c="#b03030" if hacked else ("#1f4e79" if k.startswith("RL") else "#555555"))
            ax.annotate(k, (v["reviews"], v["retention"] * 100), textcoords="offset points",
                        xytext=(6, -3), fontsize=8)
        ax.set_xlabel("reviews per item over 60 days  (effort)")
        ax.set_ylabel("average recall probability (%)")
        ax.set_title("Retention vs effort on 2000 simulated students")
        ax.grid(alpha=0.3)
        ax.set_xlim(0, 75)
        fig.tight_layout()
        fig.savefig("assets/benchmark.png", dpi=200)
        print("wrote assets/benchmark.png")
    except ImportError:
        pass
