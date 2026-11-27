import random
from style import *


class W0Python(Lesson):
    KICKER = "Week 0 · Python I"
    TITLE = "Python as labels and boxes"

    def construct(self):
        self.title_card()

        # --- names point at values
        h = self.heading("Names point at values", "Week 0")
        self.play(FadeIn(h))
        code = code_block(["x = 5"], size=30).shift(LEFT * 4 + UP * 1)
        lab = box("x", 1.0, 0.8, color=AMBER, font=MONO).shift(RIGHT * 0.5 + UP * 1)
        v5 = box("5", 1.2, 0.9, color=SLATE, font=MONO).shift(RIGHT * 3.5 + UP * 1)
        a1 = arrow(lab.get_right(), v5.get_left(), COBALT)
        self.say("In Python, x equals 5 does not put five inside x. It makes the name x point at a value.",
                 FadeIn(code), FadeIn(lab), FadeIn(v5), GrowArrow(a1))
        code2 = code_block(["x = 5", "x = 7"], size=30).move_to(code, aligned_edge=UL)
        v7 = box("7", 1.2, 0.9, color=SLATE, font=MONO).shift(RIGHT * 3.5 + DOWN * 0.6)
        a2 = arrow(lab.get_right(), v7.get_left(), COBALT)
        self.say("Assigning again just moves the label to a new value.",
                 Transform(code, code2), FadeIn(v7), Transform(a1, a2), v5.animate.set_opacity(0.3))
        self.play(FadeOut(VGroup(code, lab, v5, v7, a1)))

        # --- shared list
        h2 = self.heading("Two names, one list", "Week 0")
        self.play(Transform(h, h2))
        c = code_block(["a = [1, 2]", "b = a", "b.append(3)", "print(a)   # [1, 2, 3]"], size=28).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        cells = VGroup(*[box(str(i), 0.9, 0.9, color=SLATE, font=MONO) for i in (1, 2)]).arrange(RIGHT, buff=0).shift(RIGHT * 3 + DOWN * 0.3)
        la = box("a", 0.8, 0.7, color=AMBER, font=MONO).next_to(cells, UP, buff=1.0).shift(LEFT * 1.0)
        lb = box("b", 0.8, 0.7, color=AMBER, font=MONO).next_to(cells, UP, buff=1.0).shift(RIGHT * 1.0)
        aa = arrow(la.get_bottom(), cells.get_top() + LEFT * 0.3, COBALT)
        ab = arrow(lb.get_bottom(), cells.get_top() + RIGHT * 0.3, COBALT)
        self.say("Here a points at a list. Then b equals a makes b point at the very same list, not a copy.",
                 FadeIn(c), FadeIn(cells), FadeIn(la), GrowArrow(aa), FadeIn(lb), GrowArrow(ab), run_time=2)
        three = box("3", 0.9, 0.9, color=AMBER, font=MONO).next_to(cells, RIGHT, buff=0)
        self.say("So when b appends three, a sees it too. One list, two labels. This catches everyone at least once.",
                 FadeIn(three, shift=LEFT * 0.3), Indicate(la))
        self.play(FadeOut(VGroup(c, cells, la, lb, aa, ab, three)))

        # --- dict
        h3 = self.heading("Dictionaries name each field", "Week 0")
        self.play(Transform(h, h3))
        c = code_block(['item = {"topic": "Q-learning",', '        "streak": 2}', 'item["streak"] += 1'], size=28).to_edge(LEFT, buff=0.8)
        rows = VGroup()
        for k, v in [('"topic"', '"Q-learning"'), ('"streak"', "2")]:
            rows.add(VGroup(box(k, 2.0, 0.8, color=SLATE, font=MONO, size=22), box(v, 2.6, 0.8, color=COBALT, font=MONO, size=22)).arrange(RIGHT, buff=0))
        rows.arrange(DOWN, buff=0).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.2)
        c.scale(0.9).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        self.say("A dictionary maps keys to values. Almost every piece of data in Re-Mind is a dictionary, because dictionaries become JSON almost for free.",
                 FadeIn(c), FadeIn(rows))
        new = box("3", 2.6, 0.8, color=AMBER, font=MONO, size=22).move_to(rows[1][1])
        self.say("Update a field by its name.", Transform(rows[1][1], new))
        self.play(FadeOut(VGroup(c, rows)))

        # --- loop trace
        h4 = self.heading("Tracing a loop", "Week 0")
        self.play(Transform(h, h4))
        lines = ["total = 0", "for s in [2, 0, 1]:", "    total += s", "print(total)"]
        c = code_block(lines, size=30).to_edge(LEFT, buff=0.8)
        rowsT = c[1]
        hl = line_box(rowsT[0])
        tab_lbls = VGroup(T("s", 28, SLATE, font=MONO), T("total", 28, SLATE, font=MONO)).arrange(DOWN, aligned_edge=LEFT, buff=0.6).shift(RIGHT * 2.6)
        vals = VGroup(T("-", 34, INK, font=MONO), T("0", 34, INK, font=MONO))
        for v, l in zip(vals, tab_lbls):
            v.next_to(l, RIGHT, buff=1.0)
        self.say("Let's run a loop by hand. Total starts at zero.", FadeIn(c), Create(hl), FadeIn(tab_lbls), FadeIn(vals))
        total = 0
        for s in [2, 0, 1]:
            self.play(Transform(hl, line_box(rowsT[1])),
                      Transform(vals[0], T(str(s), 34, COBALT, font=MONO).move_to(vals[0])), run_time=0.6)
            total += s
            self.play(Transform(hl, line_box(rowsT[2])),
                      Transform(vals[1], T(str(total), 34, COBALT, font=MONO).move_to(vals[1])), run_time=0.6)
        self.caps.append((self.renderer.time - 3.6, self.renderer.time, "Each pass gives s the next value, and total grows by s."))
        self.say("When the list runs out, the loop ends and total is three. Every RL episode in this course is a loop just like this.",
                 Transform(hl, line_box(rowsT[3])))
        self.clear()


class W0Averages(Lesson):
    KICKER = "Week 0 · Maths I"
    TITLE = "Averages that learn"

    def construct(self):
        self.title_card()
        h = self.heading("Rolling a fair die", "Week 0")
        rng = random.Random(4)
        rolls = [rng.randint(1, 6) for _ in range(300)]
        means, q = [], 0.0
        for n, r in enumerate(rolls, 1):
            q += (r - q) / n
            means.append(q)
        ax = axes([0, 300, 50], [1, 6, 1], xnums=[0, 100, 200, 300], ynums=[1, 2, 3, 4, 5, 6]).shift(DOWN * 0.5)
        xl = T("rolls", 22, SLATE).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = T("value", 22, SLATE).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.4)
        ev = DashedLine(ax.c2p(0, 3.5), ax.c2p(300, 3.5), color=AMBER, stroke_width=3)
        evl = T("expected value 3.5", 22, AMBER).next_to(ev, UP, buff=0.1).align_to(ev, RIGHT)
        self.say("Roll a fair die. Each roll is random, but the average of many rolls heads to three and a half: the expected value.",
                 FadeIn(h), Create(ax), FadeIn(xl), FadeIn(yl), Create(ev), FadeIn(evl), run_time=1.6)
        dots = VGroup(*[Dot(ax.c2p(i + 1, r), radius=0.035, color=SLATE).set_opacity(0.45) for i, r in enumerate(rolls)])
        t = ValueTracker(1)
        curve = always_redraw(lambda: VMobject(color=COBALT, stroke_width=5).set_points_as_corners(
            [ax.c2p(i + 1, m) for i, m in enumerate(means[: max(2, int(t.get_value()))])]))
        self.add(curve)
        self.say("Grey dots are single rolls. The blue line is the running average. Early on it swings wildly; with more rolls the noise cancels out.",
                 LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.02), t.animate.set_value(300), run_time=6)
        self.say("That's the law of large numbers, and it's why an agent can learn from noisy experience.")
        self.clear()

        h = self.heading("An average that updates itself", "Week 0")
        eq = M(r"Q_n =", r"Q_{n-1}", r"+", r"\frac{1}{n}", r"\big(r - Q_{n-1}\big)", 60).shift(UP * 1.2)
        self.say("You don't need to store every roll to keep the average. After each new value r, nudge the old estimate.", FadeIn(h), Write(eq))
        b1 = SurroundingRectangle(eq[1], color=SLATE, buff=0.1)
        b2 = SurroundingRectangle(eq[3], color=COBALT, buff=0.1)
        b3 = SurroundingRectangle(eq[4], color=AMBER, buff=0.1)
        l1 = T("old estimate", 24, SLATE).next_to(b1, DOWN, buff=0.3)
        l2 = T("step size", 24, COBALT).next_to(b2, DOWN, buff=0.3)
        l3 = T("error", 24, AMBER).next_to(b3, DOWN, buff=0.3)
        self.say("New estimate equals old estimate, plus a step size, times the error: how surprised we were.",
                 Create(b1), FadeIn(l1), Create(b2), FadeIn(l2), Create(b3), FadeIn(l3), run_time=2)
        ex = M(r"3.2 + \tfrac{1}{5}(6 - 3.2) = 3.76", 48, color=COBALT).shift(DOWN * 1.6)
        self.say("Say the average was 3.2 after four rolls and the fifth roll is a six. The estimate moves a fifth of the way up, to 3.76.", Write(ex))
        nxt = fit(T("Week 3: the same update picks the best quiz style. Q-learning swaps 1/n for a fixed step α.", 26, INK)).to_edge(DOWN, buff=0.7)
        self.say("Remember this shape. In week three it picks the best quiz style, and Q-learning uses it with a fixed step size alpha.", FadeIn(nxt))
        self.clear()
