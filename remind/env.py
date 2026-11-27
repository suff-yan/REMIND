"""Spaced repetition as a Reinforcement Learning problem (gym-style API).

Episode   : one item, from the day it is learned (day 0) to the exam (HORIZON).
State     : (streak, last_grade)
              streak     = successful reviews in a row, capped at 5  -> 0..5
              last_grade = 0 forgot / 1 hard / 2 easy                -> 0..2
            => 6 * 3 = 18 discrete states
Action    : index into GAPS = how many days to wait before the next quiz
Reward    : see `reward()`; three modes so mentees can watch reward hacking.
The final quiz is always on exam day (a gap that overshoots is truncated).
"""
import random
from .memory_model import SimulatedStudent, retention_area, FORGOT

GAPS = [1, 2, 4, 7, 14, 30]          # days
N_ACTIONS = len(GAPS)
MAX_STREAK = 5
N_STATES = (MAX_STREAK + 1) * 3


def state_id(streak: int, grade: int) -> int:
    return min(streak, MAX_STREAK) * 3 + grade


def reward(mode: str, gap: int, grade: int, review_cost: float = 1.0, fail_weight: float = 2.0) -> float:
    recalled = grade != FORGOT
    if mode == "proven_days":     # GOOD: days of memory you proved, minus effort
        return (gap if recalled else -fail_weight * gap) - review_cost
    if mode == "correct_count":   # BAD: +1 per correct answer -> agent quizzes daily
        return 1.0 if recalled else 0.0
    if mode == "long_gaps":       # BAD: rewards waiting, ignores forgetting
        return float(gap)
    raise ValueError(f"unknown reward mode {mode!r}")


class SpacedRepetitionEnv:
    def __init__(self, horizon=60, reward_mode="proven_days", seed=None, **reward_kwargs):
        self.horizon = horizon
        self.reward_mode = reward_mode
        self.reward_kwargs = reward_kwargs
        self.rng = random.Random(seed)

    def reset(self, difficulty=None):
        self.student = SimulatedStudent(difficulty, rng=self.rng)
        self.day, self.streak, self.grade = 0, 0, FORGOT
        self.n_reviews, self.remembered_days = 0, 0.0
        self.exam_passed = None
        return state_id(self.streak, self.grade)

    def step(self, action: int):
        gap = min(GAPS[action], self.horizon - self.day)
        self.remembered_days += retention_area(gap, self.student.stability)
        grade, p = self.student.review(gap)
        self.day += gap
        self.n_reviews += 1
        self.streak = self.streak + 1 if grade != FORGOT else 0
        self.grade = grade
        r = reward(self.reward_mode, gap, grade, **self.reward_kwargs)
        done = self.day >= self.horizon
        if done:
            self.exam_passed = grade != FORGOT
        info = {"gap": gap, "grade": grade, "p": p, "day": self.day}
        return state_id(self.streak, self.grade), r, done, info

    def metrics(self):
        return {
            "reviews": self.n_reviews,
            "retention": self.remembered_days / self.horizon,
            "exam_pass": float(self.exam_passed),
        }
