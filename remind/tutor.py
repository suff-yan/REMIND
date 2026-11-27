"""The Re-Mind agent: memory + scheduler + (optional) online RL.

Each concept the student learns becomes an item:
  {"topic", "fact", "streak", "last_grade", "last_review", "next_due", "gap_action"}
On every turn the agent checks which items are due and decides by itself to quiz.
When the student answers, Gemini grades it (0/1/2) -> reward -> Q-learning update.
"""
import json
import os
import time

from .env import GAPS, N_ACTIONS, N_STATES, reward, state_id
from .rl.qlearning import QLearningAgent
from . import prompts

DAY_SECONDS = float(os.getenv("REMIND_DAY_SECONDS", 86400))  # set to 60 for demos!


class Tutor:
    def __init__(self, llm, store_path="memory.json", q_path=None, scheduler="rl", learn_online=True):
        self.llm, self.store_path, self.q_path = llm, store_path, q_path
        self.scheduler, self.learn_online = scheduler, learn_online
        self.items = self._load()
        if q_path and os.path.exists(q_path):
            self.agent = QLearningAgent.load(q_path, epsilon=0.05)
        else:
            self.agent = QLearningAgent(N_STATES, N_ACTIONS, epsilon=0.1)

    # ---------- persistence ----------
    def _load(self):
        if not os.path.exists(self.store_path):
            return []
        try:
            with open(self.store_path) as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save(self):
        with open(self.store_path, "w") as f:
            json.dump(self.items, f, indent=2)
        if self.q_path:
            self.agent.save(self.q_path)

    # ---------- scheduling ----------
    def choose_gap(self, item):
        s = state_id(item["streak"], item["last_grade"])
        if self.scheduler == "leitner":
            a = min(item["streak"], len(GAPS) - 1)
        else:
            a = self.agent.act(s, greedy=not self.learn_online)
        item["gap_action"] = a
        item["next_due"] = time.time() + GAPS[a] * DAY_SECONDS
        return GAPS[a]

    def due_items(self, now=None):
        now = now or time.time()
        return sorted([i for i in self.items if i["next_due"] <= now], key=lambda i: i["next_due"])

    # ---------- learning new concepts ----------
    def remember(self, question, answer):
        info = self.llm.json(prompts.EXTRACT.format(question=question, answer=answer),
                             fallback={"topic": question[:40], "fact": answer[:200]})
        item = {"topic": info.get("topic", question[:40]), "fact": info.get("fact", answer[:200]),
                "streak": 0, "last_grade": 0, "last_review": time.time(), "history": []}
        self.choose_gap(item)
        self.items.append(item)
        self.save()
        return item

    # ---------- quizzing ----------
    def make_quiz(self, item):
        if self.llm.offline:
            return f"What do you remember about: {item['topic']}?"
        return self.llm.chat([{"role": "user", "content": prompts.QUIZ.format(**item)}])

    def grade_and_learn(self, item, question, answer, now=None):
        now = now or time.time()
        res = self.llm.json(prompts.GRADE.format(fact=item["fact"], question=question, answer=answer),
                            fallback={"grade": 1, "feedback": "(offline) graded as 'hard'."})
        grade = int(res.get("grade", 1))
        elapsed_days = (now - item["last_review"]) / DAY_SECONDS
        s = state_id(item["streak"], item["last_grade"])
        a = item.get("gap_action", 0)
        r = reward("proven_days", elapsed_days, grade)
        item["streak"] = item["streak"] + 1 if grade > 0 else 0
        item["last_grade"], item["last_review"] = grade, now
        item["history"].append({"t": now, "grade": grade, "reward": round(r, 2), "gap_days": round(elapsed_days, 2)})
        if self.learn_online and self.scheduler == "rl":
            self.agent.update(s, a, r, state_id(item["streak"], grade), done=False)
        gap = self.choose_gap(item)
        self.save()
        return grade, res.get("feedback", ""), r, gap
