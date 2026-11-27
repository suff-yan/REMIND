"""Review-gap policies. Each policy maps (streak, last_grade) -> action index."""
from .env import GAPS, MAX_STREAK, state_id
from .memory_model import EASY


def fixed(days):
    a = GAPS.index(days)
    return lambda streak, grade: a


def leitner(streak, grade):
    """Classic level/box system: level = streak. Fail -> back to box 0."""
    return min(streak, len(GAPS) - 1)


def leitner_plus(streak, grade):
    """Hand-tuned rule: skip a box when the answer felt easy."""
    bonus = 1 if grade == EASY else 0
    return min(streak + bonus, len(GAPS) - 1)


def from_agent(agent):
    return lambda streak, grade: agent.act(state_id(streak, grade), greedy=True)


def evaluate(policy, env_factory, n=2000, seed=123):
    env = env_factory(seed)
    tot = {"reviews": 0.0, "retention": 0.0, "exam_pass": 0.0}
    for _ in range(n):
        env.reset()
        done = False
        while not done:
            _, _, done, _ = env.step(policy(env.streak, env.grade))
        for k, v in env.metrics().items():
            tot[k] += v
    return {k: v / n for k, v in tot.items()}
