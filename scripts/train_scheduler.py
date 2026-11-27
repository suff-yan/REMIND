"""Pre-train the RL scheduler on simulated students.

    python scripts/train_scheduler.py --episodes 40000 --reward proven_days
Saves data/q_table.json which the Streamlit tutor loads as a warm start.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from remind.env import GAPS, N_ACTIONS, N_STATES, SpacedRepetitionEnv, state_id
from remind.memory_model import GRADE_NAMES
from remind.rl.qlearning import QLearningAgent, train


def print_policy(agent):
    print("\nLearned policy: next gap (days)")
    print("streak | " + " | ".join(f"{GRADE_NAMES[g]:>6}" for g in range(3)))
    for streak in range(6):
        cells = []
        for g in range(3):
            if streak > 0 and g == 0:          # impossible state: streak>0 means last answer was right
                cells.append(f"{'-':>6}")
            elif streak == 0 and g > 0:
                cells.append(f"{'-':>6}")
            else:
                cells.append(f"{GAPS[agent.act(state_id(streak, g), greedy=True)]:>6}")
        print(f"{streak:>6} | " + " | ".join(cells))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", type=int, default=40000)
    ap.add_argument("--reward", default="proven_days", choices=["proven_days", "correct_count", "long_gaps"])
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default="data/q_table.json")
    args = ap.parse_args()

    env = SpacedRepetitionEnv(seed=args.seed, reward_mode=args.reward)
    agent = QLearningAgent(N_STATES, N_ACTIONS, seed=args.seed, epsilon_decay=0.9998)
    train(env, agent, args.episodes, log_every=args.episodes // 8)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    agent.save(args.out)
    print_policy(agent)
    print(f"\nsaved -> {args.out}")
