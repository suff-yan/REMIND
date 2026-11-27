import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from remind.memory_model import SimulatedStudent, recall_probability, retention_area
from remind.env import SpacedRepetitionEnv, N_STATES, N_ACTIONS, reward
from remind.rl.qlearning import QLearningAgent, train
from remind.rl.bandits import BernoulliBandit, UCB1, run
from remind.rl.gridworld import GridWorld
from remind.schedulers import evaluate, fixed, leitner, from_agent


def test_forgetting_curve():
    assert recall_probability(0, 5) == 1.0
    assert abs(recall_probability(5, 5) - 0.9) < 1e-9          # S = days to 90 %
    assert 0 < retention_area(10, 5) < 10


def test_review_updates_stability():
    import random
    s = SimulatedStudent(difficulty=0.2, rng=random.Random(0))
    before = s.stability
    grade, p = s.review(0.0)                                   # p = 1 -> always recalled
    assert grade > 0 and s.stability > before


def test_env_episode_ends_on_exam_day():
    env = SpacedRepetitionEnv(seed=0, horizon=60)
    env.reset(); done = False
    while not done:
        _, _, done, info = env.step(5)
    assert info["day"] == 60


def test_reward_modes():
    assert reward("correct_count", 30, 2) == 1.0
    assert reward("long_gaps", 30, 0) == 30
    assert reward("proven_days", 7, 2) == 6 and reward("proven_days", 7, 0) == -15


def test_q_learning_beats_weekly():
    env = SpacedRepetitionEnv(seed=1)
    agent = QLearningAgent(N_STATES, N_ACTIONS, seed=1, epsilon_decay=0.999)
    train(env, agent, 4000)
    mk = lambda s: SpacedRepetitionEnv(seed=s)
    assert evaluate(from_agent(agent), mk, n=300)["retention"] > evaluate(fixed(7), mk, n=300)["retention"]


def test_ucb_finds_best_arm():
    b = BernoulliBandit([0.2, 0.5, 0.8], seed=0)
    agent = UCB1(3, seed=0)
    run(b, agent, 2000)
    assert max(range(3), key=lambda a: agent.counts[a]) == 2


def test_gridworld_q_learning_reaches_goal():
    env = GridWorld()
    agent = QLearningAgent(env.n_states, env.n_actions, seed=0, epsilon_decay=0.995)
    train(env, agent, 1500)
    s, done, total = env.reset(), False, 0
    while not done:
        s, r, done, _ = env.step(agent.act(s, greedy=True)); total += r
    assert total > 9


def test_tutor_offline_roundtrip():
    from remind.llm import LLM
    from remind.tutor import Tutor
    with tempfile.TemporaryDirectory() as d:
        llm = LLM(api_key=None); llm.offline = True
        t = Tutor(llm, store_path=os.path.join(d, "m.json"))
        item = t.remember("What is entropy?", "A measure of disorder.")
        grade, fb, r, gap = t.grade_and_learn(item, "q?", "disorder", now=item["last_review"] + 86400)
        assert grade == 1 and gap >= 1 and os.path.exists(os.path.join(d, "m.json"))
