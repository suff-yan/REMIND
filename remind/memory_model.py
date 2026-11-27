"""A tiny, readable model of human memory used to simulate students.

Idea (forgetting curve):  P(recall after t days) = 0.9 ** (t / S)
  S = "stability" in days = how long until recall drops to 90%.
  Bigger S -> slower forgetting.

Every review changes S:
  * successful recall  -> S grows. It grows MORE when recall was hard
                          (p was low) - the "desirable difficulty" effect.
  * failed recall      -> S shrinks (you have to re-learn).

This is a simplified cousin of the models used by modern schedulers such as
FSRS. It is NOT a scientific model of your brain - it is a sandbox that lets
an RL agent practise millions of reviews in seconds.
"""
import math
import random

# Grades the tutor can observe after a quiz (Gemini gives the same 3 buckets)
FORGOT, HARD, EASY = 0, 1, 2
GRADE_NAMES = {FORGOT: "forgot", HARD: "hard", EASY: "easy"}


def recall_probability(days_since_review: float, stability: float) -> float:
    """Probability of remembering an item `days_since_review` days later."""
    return 0.9 ** (days_since_review / stability)


def retention_area(gap: float, stability: float) -> float:
    """Integral of the recall probability over a gap (in 'remembered days')."""
    k = math.log(1 / 0.9) / stability
    return (1.0 - math.exp(-k * gap)) / k


class SimulatedStudent:
    """One simulated student learning ONE item (fact / concept).

    difficulty in [0, 1]: 0 = trivial, 1 = very hard. Hidden from the agent!
    """

    MIN_S, MAX_S = 0.2, 365.0

    def __init__(self, difficulty=None, rng=None):
        self.rng = rng or random.Random()
        self.difficulty = self.rng.uniform(0.0, 1.0) if difficulty is None else difficulty
        # right after first learning: easy items are already a bit stable
        self.stability = 0.3 + 1.2 * (1.0 - self.difficulty)

    def p_recall(self, days: float) -> float:
        return recall_probability(days, self.stability)

    def review(self, days_since_last: float):
        """Quiz the student. Returns (grade, p_before_review)."""
        p = self.p_recall(days_since_last)
        recalled = self.rng.random() < p
        if recalled:
            growth = 1.0 + (2.0 - 1.8 * self.difficulty) * (1.0 + 2.0 * (1.0 - p))
            self.stability = min(self.MAX_S, self.stability * growth)
            # a noisy self-report: recall felt hard when p was low
            felt_hard = self.rng.random() < (1.0 - p) + 0.1
            grade = HARD if felt_hard else EASY
        else:
            self.stability = max(self.MIN_S, self.stability * 0.5)
            grade = FORGOT
        return grade, p
