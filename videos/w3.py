import random
from style import *
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from remind.rl.bandits import BernoulliBandit, EpsilonGreedy, UCB1, run
from remind.rl.gridworld import GridWorld, LAYOUT
from remind.rl.qlearning import QLearningAgent

STYLES = ["MCQ", "fill-blank", "explain", "true/false"]
PROBS = [0.35, 0.50, 0.70, 0.55]


class W3Bandit(Lesson):
    KICKER = "Week 3 · Bandits"
    TITLE = "The bandit's dilemma"

    def bars(self, values, counts, origin):
        g = VGroup()
        for i, (v, n) in enumerate(zip(values, counts)):
            x = origin + RIGHT * i * 2.4
            base = Line(x + LEFT * 0.6, x + RIGHT * 0.6, color=SLATE)
            bar = Rectangle(width=1.0, height=max(0.02, v * 3.2), fill_color=COBALT, fill_opacity=0.85, stroke_width=0).next_to(base, UP, buff=0)
            lab = T(STYLES[i], 22, INK).next_to(base, DOWN, buff=0.2)
            cnt = T(f"used {n}", 20, SLATE, font=MONO).next_to(lab, DOWN, buff=0.1)
            est = T(f"{v:.2f}", 22, COBALT, font=MONO).next_to(bar, UP, buff=0.1)
            g.add(VGroup(base, bar, lab, cnt, est))
        return g

    def step_bars(self, cur, new):
        self.play(*[Transform(cur[i][1], new[i][1]) for i in range(4)], run_time=0.6)
        for i in range(4):
            cur[i][3].become(new[i][3]); cur[i][4].become(new[i][4])
        self.wait(0.15)

    def simulate(self, agent, steps, seed=2):
        b = BernoulliBandit(PROBS, seed=seed)
        snaps = []
        for t in range(1, steps + 1):
            a = agent.select(); agent.update(a, b.pull(a))
            if t in (5, 20, 60, 150, 400, 1000):
                snaps.append((t, list(agent.values), list(agent.counts)))
        return snaps

    def construct(self):
        self.title_card()
        h = self.heading("Which quiz style helps you remember?", "Week 3")
        origin = LEFT * 3.6 + DOWN * 1.2
        hidden = VGroup(*[T(f"true p = {p:.2f}", 20, AMBER, font=MONO).move_to(origin + RIGHT * i * 2.4 + UP * 3.0) for i, p in enumerate(PROBS)])
        cur = self.bars([0] * 4, [0] * 4, origin)
        self.say("The tutor can quiz you in four styles. Each one helps you remember with some probability, but the tutor doesn't know which is best.",
                 FadeIn(h), FadeIn(cur))
        self.say("Here are the true values, hidden from the agent. Explain-in-your-own-words is best, at seventy percent.", FadeIn(hidden))
        self.play(FadeOut(hidden))
        greedy = EpsilonGreedy(4, 0.0, seed=1)
        snaps = self.simulate(greedy, 1000)
        tag = T("greedy: always pick the best-looking style", 26, AMBER).to_edge(UP, buff=1.5)
        self.say("A greedy agent always uses whatever looks best so far.", FadeIn(tag))
        for t, v, c in snaps:
            self.step_bars(cur, self.bars(v, c, origin))
        self.say("It locked onto the first style that paid off, and never tried the others again. Early luck became a permanent mistake.",
                 Indicate(cur[0], color=AMBER))
        eps = EpsilonGreedy(4, 0.1, seed=1)
        snaps = self.simulate(eps, 1000)
        self.play(FadeOut(tag), FadeOut(cur))
        tag = T("epsilon-greedy: explore 10% of the time", 26, COBALT).to_edge(UP, buff=1.5)
        cur = self.bars([0] * 4, [0] * 4, origin)
        self.play(FadeIn(tag), FadeIn(cur))
        for t, v, c in snaps:
            self.step_bars(cur, self.bars(v, c, origin))
        self.say("Now the agent tries a random style one time in ten. Its estimates sharpen, and it ends up using explain-it most. Exploration pays.",
                 Indicate(cur[2], color=COBALT))
        self.clear()

        h = self.heading("Regret: reward lost to not knowing", "Week 3")
        ax = axes([0, 2000, 500], [0, 700, 100], x_length=10, y_length=4.6, xnums=[0, 1000, 2000], ynums=[0, 200, 400, 600]).shift(DOWN * 0.4)
        xl = T("quizzes given", 22, SLATE).next_to(ax.x_axis, DOWN, buff=0.4)
        curves = VGroup()
        for name, mk, col in [("greedy", lambda: EpsilonGreedy(4, 0.0, seed=1), AMBER), ("epsilon-greedy", lambda: EpsilonGreedy(4, 0.1, seed=1), SLATE), ("UCB", lambda: UCB1(4, seed=1), COBALT)]:
            avg = [0.0] * 2000
            for r in range(30):
                _, reg = run(BernoulliBandit(PROBS, seed=r), mk(), 2000)
                avg = [a + x / 30 for a, x in zip(avg, reg)]
            c = VMobject(color=col, stroke_width=5).set_points_as_corners([ax.c2p(i, avg[i]) for i in range(0, 2000, 20)])
            l = T(name, 22, col).next_to(c.get_end(), RIGHT, buff=0.15)
            curves.add(VGroup(c, l))
        self.say("Regret counts the reward lost compared with always using the best style. Greedy's regret keeps climbing. With exploration it flattens out.",
                 FadeIn(h), Create(ax), FadeIn(xl), *[Create(c[0]) for c in curves], *[FadeIn(c[1]) for c in curves], run_time=3)
        ucb = M(r"a_t = \arg\max_a \; Q(a) + \sqrt{\frac{c \ln t}{N(a)}}", 40, color=COBALT).move_to(ax.c2p(700, 520))
        self.say("UCB explores smarter: it adds a bonus to styles it has rarely tried, so it explores where it's unsure, not at random.", Write(ucb))
        self.clear()


class W3QLearning(Lesson):
    KICKER = "Week 3 · Q-learning"
    TITLE = "Q-learning, cell by cell"

    def grid_view(self, Q, env, origin, size=1.25):
        g = VGroup()
        vmax = 10.0
        for r in range(4):
            for c in range(4):
                s = r * 4 + c
                ch = LAYOUT[r][c]
                center = origin + RIGHT * c * size + DOWN * r * size
                if ch == "#":
                    sq = Square(size, fill_color=SLATE, fill_opacity=1, stroke_color=PAPER, stroke_width=3).move_to(center)
                    g.add(sq); continue
                v = max(Q[s]) if Q is not None else 0.0
                if ch == "G":
                    fill, op = GREEN, 0.85
                elif ch == "X":
                    fill, op = AMBER, 0.85
                else:
                    fill, op = COBALT, max(0.0, min(1.0, v / vmax)) * 0.75
                sq = Square(size, fill_color=fill, fill_opacity=op, stroke_color=RULE, stroke_width=2).move_to(center)
                cell = VGroup(sq)
                if ch in "GX":
                    cell.add(T("exam" if ch == "G" else "phone", 18, WHITE).move_to(center))
                elif Q is not None and max(Q[s]) != 0:
                    a = max(range(4), key=lambda k: Q[s][k])
                    d = [UP, DOWN, LEFT, RIGHT][a]
                    cell.add(Arrow(center - d * 0.28, center + d * 0.28, color=INK, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.35))
                    cell.add(T(f"{v:.1f}", 14, INK, font=MONO).move_to(center + DOWN * 0.42 + RIGHT * 0.35))
                if ch == "S":
                    cell.add(T("start", 14, SLATE, font=MONO).move_to(center + UP * 0.42 + LEFT * 0.3))
                g.add(cell)
        return g

    def construct(self):
        self.title_card()
        h = self.heading("The update", "Week 3")
        eq = M(r"Q(s,a) \leftarrow", r"Q(s,a)", r"+ \alpha \big[", r"r + \gamma \max_{a'} Q(s',a')", r"- Q(s,a)", r"\big]", 52).shift(UP * 0.8)
        self.say("Q-learning keeps a table: for every state and action, how good it expects things to be from there.", FadeIn(h), Write(eq))
        b = SurroundingRectangle(eq[3], color=COBALT, buff=0.1)
        bl = T("target: reward now, plus the best value one step ahead", 24, COBALT).next_to(b, DOWN, buff=0.35)
        self.say("After every step it nudges one entry toward a target: the reward it just got, plus the best value it currently expects from the next state.", Create(b), FadeIn(bl))
        same = T("Same shape as the running mean: new = old + step × error", 26, INK).to_edge(DOWN, buff=0.8)
        self.say("It's the running average from week zero again, except the target looks one step into the future.", FadeIn(same))
        self.clear()

        h = self.heading("The study room", "Week 3")
        env = GridWorld()
        origin = LEFT * 1.9 + UP * 1.6
        legend = VGroup(T("+10 at the exam", 22, GREEN), T("−5 for the phone", 22, AMBER), T("−0.1 per step", 22, SLATE),
                        T("colour = best value", 22, COBALT), T("arrow = best action", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.9)
        view = self.grid_view(None, env, origin)
        self.say("Reach the exam hall for plus ten. Picking up your phone costs five and ends the episode. Every step costs a little time.", FadeIn(h), FadeIn(view), FadeIn(legend))
        agent = QLearningAgent(16, 4, alpha=0.1, gamma=0.95, epsilon_decay=0.995, seed=0)
        snaps, marks = {}, [1, 10, 40, 100, 250, 600, 1500]
        for ep in range(1, 1501):
            s, done = env.reset(), False
            while not done:
                a = agent.act(s); s2, r, done, _ = env.step(a); agent.update(s, a, r, s2, done); s = s2
            agent.decay()
            if ep in marks:
                snaps[ep] = [row[:] for row in agent.q]
        ep_lbl = T("episode 0", 26, SLATE, font=MONO).next_to(view, DOWN, buff=0.4)
        self.play(FadeIn(ep_lbl))
        start = self.renderer.time
        for ep in marks:
            self.play(Transform(view, self.grid_view(snaps[ep], env, origin)),
                      Transform(ep_lbl, T(f"episode {ep}", 26, SLATE, font=MONO).move_to(ep_lbl)), run_time=1.2)
            self.wait(0.6)
        self.caps.append((start, self.renderer.time, "Watch value spread backwards from the exam, one update at a time, until arrows form a path."))
        s, path = env.reset(), [env.start]
        for _ in range(10):
            s, r, done, _ = env.step(max(range(4), key=lambda k: agent.q[s][k])); path.append((s // 4, s % 4))
            if done:
                break
        pts = [origin + RIGHT * c * 1.25 + DOWN * r * 1.25 for r, c in path]
        trail = VMobject(color=AMBER, stroke_width=8).set_points_as_corners(pts)
        self.say("Follow the arrows from the start: a shortest path to the exam that avoids both phones. Nobody told it the route. It learned from reward alone.", Create(trail), run_time=2)
        nxt = T("Week 4: the same 40 lines learn when to quiz a student.", 26, INK).move_to(ep_lbl)
        self.say("Next week, the exact same algorithm learns when to quiz a student.", FadeOut(ep_lbl), FadeIn(nxt))
        self.clear()
