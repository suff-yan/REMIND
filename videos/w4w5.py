import json, os, random, sys
from style import *
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from remind.memory_model import SimulatedStudent, recall_probability
from remind.env import GAPS, N_ACTIONS, N_STATES, SpacedRepetitionEnv, state_id
from remind.rl.qlearning import QLearningAgent, train

BENCH = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "benchmark.json")))


class W4Forgetting(Lesson):
    KICKER = "Week 4 · Memory"
    TITLE = "Forgetting and Leitner boxes"

    def construct(self):
        self.title_card()
        h = self.heading("The forgetting curve", "Week 4")
        ax = axes([0, 30, 5], [0, 1, 0.25], x_length=9.5, y_length=4.4, xnums=[0, 10, 20, 30], ynums=[0, 0.5, 1]).shift(DOWN * 0.6 + LEFT * 1.2)
        xl = T("days since learning", 22, SLATE).next_to(ax.x_axis, DOWN, buff=0.4)
        eq = M(r"P(\text{recall}) = 0.9^{\,t/S}", 46).to_corner(UR, buff=0.8).shift(DOWN * 0.8)
        S = ValueTracker(1.5)
        curve = always_redraw(lambda: ax.plot(lambda t: recall_probability(t, S.get_value()), x_range=[0, 30], color=COBALT, stroke_width=5))
        sl = always_redraw(lambda: T(f"S = {S.get_value():.1f} days", 26, COBALT, font=MONO).next_to(eq, DOWN, buff=0.4))
        self.say("Memory fades by the same fraction each stretch of days. Stability S is how many days until recall drops to ninety percent.",
                 FadeIn(h), Create(ax), FadeIn(xl), Write(eq), Create(curve), FadeIn(sl), run_time=2)
        self.say("Bigger stability, slower forgetting.", S.animate.set_value(12), run_time=2.5)
        self.play(S.animate.set_value(1.5), run_time=1)
        self.remove(curve)
        st = SimulatedStudent(difficulty=0.4, rng=random.Random(3))
        pts, last, todo, marks = [], 0.0, [1, 3, 7, 14], []
        for k in range(0, 301):
            d = k / 10
            if todo and d >= todo[0]:
                st.review(todo.pop(0) - last); last = d; marks.append(d)
            pts.append(ax.c2p(d, st.p_recall(d - last)))
        nor = DashedVMobject(ax.plot(lambda t: recall_probability(t, 1.5), x_range=[0, 30], color=SLATE), num_dashes=40)
        saw = VMobject(color=COBALT, stroke_width=5).set_points_as_corners(pts)
        ticks = VGroup(*[Line(ax.c2p(m, 0), ax.c2p(m, 0.08), color=AMBER, stroke_width=5) for m in marks])
        tl = T("reviews", 22, AMBER).next_to(ticks, DOWN, buff=0.1).align_to(ticks, LEFT)
        self.say("Now review on days one, three, seven and fourteen. Each review resets recall to the top, and boosts stability, so the next dip is shallower.",
                 FadeOut(sl), Create(nor), Create(saw), FadeIn(ticks), run_time=3.5)
        self.say("Without reviews, the grey curve: most of it is gone in a month.")
        self.clear()

        h = self.heading("Leitner boxes: one ladder for everyone", "Week 4")
        boxes = VGroup(*[box(f"{g} d", 1.7, 1.0, color=SLATE, font=MONO, size=24) for g in GAPS]).arrange(RIGHT, buff=0.35).shift(UP * 0.5)
        nums = VGroup(*[T(f"box {i}", 18, SLATE, font=MONO).next_to(b, UP, buff=0.15) for i, b in enumerate(boxes)])
        self.say("The classic rule: six boxes with growing gaps. A correct answer moves the card up a box. A wrong answer sends it back to box zero.",
                 FadeIn(h), FadeIn(boxes), FadeIn(nums))
        card = RoundedRectangle(corner_radius=0.05, width=0.9, height=0.55, fill_color=COBALT, fill_opacity=1, stroke_width=0)
        card.move_to(boxes[0])
        self.play(FadeIn(card))
        for i in range(1, 4):
            self.play(card.animate.move_to(boxes[i]), run_time=0.5)
        self.play(card.animate.set_fill(AMBER), run_time=0.3)
        self.play(card.animate.move_to(boxes[0]), run_time=0.7)
        self.caps.append((self.renderer.time - 2.5, self.renderer.time, "Right, right, right, then one slip, and it falls all the way back."))
        self.play(card.animate.set_fill(COBALT), run_time=0.2)
        stats = VGroup(*[VGroup(T(lbl, 24, SLATE), T(v, 54, col, font=SERIF)).arrange(DOWN, buff=0.1) for lbl, v, col in
                         [("easy concepts", "99%", COBALT), ("medium", "97%", COBALT), ("hard concepts", "81%", AMBER)]]).arrange(RIGHT, buff=1.6).shift(DOWN * 2.1)
        self.say("Leitner is strong. But on our simulated students it keeps ninety-nine percent of easy concepts, and only eighty-one percent of hard ones.",
                 FadeOut(card), LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in stats], lag_ratio=0.3))
        self.say("One fixed ladder can't fit every concept. A policy that adapts could do better, and that's what we'll train.", Indicate(stats[2], color=AMBER))
        self.clear()


class W4Scheduler(Lesson):
    KICKER = "Week 4 · RL scheduler"
    TITLE = "Teaching a scheduler, and watching it cheat"

    def construct(self):
        self.title_card()
        h = self.heading("When to quiz, as an RL problem", "Week 4")
        rows = [("state", "streak (0–5) × last grade  →  18 states"), ("action", "wait 1, 2, 4, 7, 14 or 30 days"),
                ("reward", "+gap − 1 if recalled,   −2·gap − 1 if forgot"), ("environment", "a simulated student, day 0 to exam on day 60")]
        tbl = VGroup(*[VGroup(T(a, 28, COBALT, font=MONO), T(b, 28, INK)).arrange(RIGHT, buff=0.6) for a, b in rows])
        for r in tbl:
            r[1].shift(RIGHT * (3.2 - r[0].width - 0.6))
        tbl.arrange(DOWN, aligned_edge=LEFT, buff=0.55).shift(DOWN * 0.2)
        self.say("The agent only sees what a real tutor could: the streak of correct answers and the last grade. Its action is how long to wait.",
                 FadeIn(h), FadeIn(tbl[0]), FadeIn(tbl[1]), FadeIn(tbl[3]))
        self.say("The reward: waited fourteen days and still remembered? You proved fourteen days of memory. Forgetting costs double, and every review costs effort.",
                 FadeIn(tbl[2]))
        self.play(Indicate(tbl[2][1], color=AMBER))
        self.clear()

        h = self.heading("Training on 40,000 simulated students", "Week 4")
        env = SpacedRepetitionEnv(seed=1)
        ag = QLearningAgent(N_STATES, N_ACTIONS, seed=1, epsilon_decay=0.9998)
        curve = train(env, ag, 40000)
        k = 500
        sm = [sum(curve[max(0, i - k):i + 1]) / len(curve[max(0, i - k):i + 1]) for i in range(0, 40000, 200)]
        ax = axes([0, 40000, 10000], [-80, 40, 20], x_length=10, y_length=4.4, xnums=[0, 20000, 40000], ynums=[-80, -40, 0, 40]).shift(DOWN * 0.5)
        xl = T("simulated students (episodes)", 22, SLATE).next_to(ax.x_axis, DOWN, buff=0.4)
        line = VMobject(color=COBALT, stroke_width=5).set_points_as_corners([ax.c2p(i * 200, v) for i, v in enumerate(sm)])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(40000, 0), color=RULE)
        self.say("Same Q-learning as the gridworld. At first it guesses badly and students forget. Within about fifteen thousand students, the return climbs and settles. Five seconds on a laptop.",
                 FadeIn(h), Create(ax), FadeIn(xl), Create(zero), Create(line), run_time=4)
        self.clear()

        h = self.heading("Recall vs effort on 2,000 new students", "Week 4")
        ax = axes([0, 65, 10], [0, 100, 20], x_length=10.5, y_length=4.8, xnums=[0, 20, 40, 60], ynums=[0, 50, 100]).shift(DOWN * 0.4)
        xl = T("reviews per concept (effort)", 22, SLATE).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = T("avg recall %", 22, SLATE).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.35)
        self.play(FadeIn(h), Create(ax), FadeIn(xl), FadeIn(yl))
        pts = {}
        for name, col in [("Every day", SLATE), ("Every 2 days", SLATE), ("Every 4 days", SLATE), ("Every week", SLATE), ("Leitner boxes", SLATE)]:
            v = BENCH[name]
            d = Dot(ax.c2p(v["reviews"], 100 * v["retention"]), radius=0.1, color=col)
            l = T(name, 20, SLATE).next_to(d, DOWN if name == "Leitner boxes" else RIGHT, buff=0.12)
            pts[name] = VGroup(d, l)
        self.say("Fixed schedules trade effort for recall along a curve. Every day is near perfect, but costs sixty reviews. Leitner sits at ninety-three percent with ten.",
                 LaggedStart(*[FadeIn(p) for p in pts.values()], lag_ratio=0.25), run_time=2)
        v = BENCH["RL (good reward)"]
        star = Star(5, outer_radius=0.22, color=COBALT, fill_opacity=1).move_to(ax.c2p(v["reviews"], 100 * v["retention"]))
        sl = T("RL scheduler: 96.8% recall, 11.8 reviews", 24, COBALT).move_to(ax.c2p(36, 74))
        sl_ar = arrow(sl.get_left() + LEFT * 0.05, star.get_center() + RIGHT * 0.15 + DOWN * 0.1, COBALT)
        self.say("The learned scheduler lands top-left: ninety-seven percent recall with under twelve reviews. Same recall as every two days, with sixty percent less effort.",
                 GrowFromCenter(star), FadeIn(sl), GrowArrow(sl_ar))
        self.wait(0.5)
        h2 = self.heading("Reward hacking", "Week 4")
        bad = []
        for name, label in [("RL (+1 per correct)", "+1 per correct answer: quizzes almost daily"), ("RL (+gap length)", "+gap length: never quizzes")]:
            v = BENCH[name]
            x = Cross(scale_factor=0.18, stroke_color=AMBER, stroke_width=6).move_to(ax.c2p(v["reviews"], 100 * v["retention"]))
            l = T(label, 22, AMBER)
            if v["reviews"] > 30:
                l.move_to(ax.c2p(45, 52))
            else:
                l.next_to(x, RIGHT, buff=0.15)
            grp = VGroup(x, l)
            if v["reviews"] > 30:
                grp.add(arrow(l.get_top() + RIGHT * 1.2, x.get_bottom(), AMBER))
            bad.append(grp)
        self.say("Now change the reward. Plus one per correct answer sounds right, but the agent quizzes you almost every day: easy points, huge workload.",
                 Transform(h, h2), FadeIn(bad[0]))
        self.say("Reward long gaps instead, and it simply never quizzes you. Recall collapses to twenty-two percent.", FadeIn(bad[1]))
        msg = fit(T("RL optimises exactly what you reward, not what you meant.", 30, INK, font=SERIF)).move_to(xl)
        self.say("Reinforcement learning optimises exactly what you reward, not what you meant. Designing the reward is the real work.", FadeOut(xl), FadeIn(msg))
        self.clear()


class W5System(Lesson):
    KICKER = "Week 5 · The live tutor"
    TITLE = "One concept's life"

    def construct(self):
        self.title_card()
        h = self.heading("From a question to an updated Q-table", "Week 5")
        steps = [("ask", "“What is a Q-table?”"), ("extract", "{topic, fact} as JSON"), ("schedule", "agent picks a gap"),
                 ("interrupt", "due → recall check"), ("grade", "Gemini: 0, 1 or 2"), ("learn", "reward → Q update")]
        nodes = VGroup(*[VGroup(box(a, 2.6, 0.85, size=26, font=SERIF), T(b, 20, SLATE)).arrange(DOWN, buff=0.15) for a, b in steps])
        top, bot = VGroup(*nodes[:3]).arrange(RIGHT, buff=1.2), VGroup(*nodes[3:]).arrange(RIGHT, buff=1.2)
        VGroup(top, bot).arrange(DOWN, buff=1.3).shift(DOWN * 0.3)
        bot_order = [nodes[3], nodes[4], nodes[5]]
        arrows = VGroup(arrow(nodes[0][0].get_right(), nodes[1][0].get_left(), COBALT), arrow(nodes[1][0].get_right(), nodes[2][0].get_left(), COBALT),
                        arrow(nodes[2][0].get_bottom(), nodes[5][0].get_top() + RIGHT * 0, COBALT))
        # bottom row runs right-to-left visually: place in reverse
        bot_pos = [n.get_center() for n in nodes[3:]]
        nodes[3].move_to(bot_pos[2]); nodes[5].move_to(bot_pos[0])
        arrows = VGroup(arrow(nodes[0][0].get_right(), nodes[1][0].get_left(), COBALT), arrow(nodes[1][0].get_right(), nodes[2][0].get_left(), COBALT),
                        arrow(nodes[2][0].get_bottom(), nodes[3][0].get_top(), COBALT), arrow(nodes[3][0].get_left(), nodes[4][0].get_right(), COBALT),
                        arrow(nodes[4][0].get_left(), nodes[5][0].get_right(), COBALT))
        back = T("↻  the next gap comes from the updated Q-table", 24, AMBER).next_to(VGroup(*nodes), DOWN, buff=0.5)
        caps = ["You ask a question, and Gemini answers it, directly or Socratically.",
                "Gemini also extracts the concept you learned, as JSON, and the tutor stores it with a streak and a last grade.",
                "The reinforcement learning agent looks at that state and picks how long to wait.",
                "When the concept is due, the tutor interrupts you with a recall check. Nobody asked it to.",
                "Gemini grades your answer zero, one or two.",
                "The grade and the days you actually waited become the reward. One Q update, and a new gap."]
        self.play(FadeIn(h))
        for i in range(6):
            anims = [FadeIn(nodes[i], shift=UP * 0.15)]
            if i:
                anims.append(GrowArrow(arrows[i - 1]))
            self.say(caps[i], *anims, run_time=0.9)
        self.say("Then the loop repeats, and each time the agent knows you a little better.", FadeIn(back))
        self.play(Indicate(nodes[2][0], color=AMBER), Indicate(nodes[5][0], color=AMBER))
        self.clear()

        h = self.heading("Pre-train in simulation, fine-tune on you", "Week 5")
        sim = box("40,000 simulated students", 3.7, 1.0, color=SLATE, fill=STONE, size=22)
        qt = box("Q-table  (18 × 6)", 2.9, 1.0, color=COBALT, font=MONO, size=22)
        you = box("your real grades", 3.2, 1.0, color=AMBER, size=22)
        VGroup(sim, qt, you).arrange(RIGHT, buff=1.4).shift(UP * 0.4)
        a1, a2 = arrow(sim.get_right(), qt.get_left(), COBALT), arrow(you.get_left(), qt.get_right(), AMBER)
        l1 = T("pre-train", 20, SLATE).next_to(a1, UP, buff=0.2)
        l2 = T("fine-tune", 20, AMBER).next_to(a2, UP, buff=0.2)
        self.say("Learning from scratch on one person would take months. So the agent pre-trains on simulated students, then keeps learning from your real grades.",
                 FadeIn(h), FadeIn(sim), FadeIn(qt), GrowArrow(a1), FadeIn(l1))
        self.say("It works because the live tutor uses the same eighteen states and the same reward as the simulator.", FadeIn(you), GrowArrow(a2), FadeIn(l2))
        demo = code_block(["# .env", "REMIND_DAY_SECONDS=60   # one tutor-day = one minute"], 24).shift(DOWN * 2.0)
        self.say("And for demos, one line in the env file makes a tutor day last one minute. Now go build yours.", FadeIn(demo))
        self.clear()
