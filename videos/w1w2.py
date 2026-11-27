from style import *


class W1Request(Lesson):
    KICKER = "Week 1 · APIs"
    TITLE = "One request, end to end"

    def construct(self):
        self.title_card()
        h = self.heading("Your code never touches the model", "Week 1")
        app = box("app.py", 2.4, 1.0)
        env = box(".env  (API key)", 2.8, 0.9, color=AMBER, font=MONO, size=22)
        sdk = box("google-genai SDK", 3.0, 1.0)
        cloud = box("Gemini on Google's servers", 3.6, 1.4, color=SLATE, fill=STONE)
        row = VGroup(app, sdk, cloud).arrange(RIGHT, buff=1.2).shift(UP * 0.4)
        env.next_to(app, DOWN, buff=1.0)
        a1, a2 = arrow(app.get_right(), sdk.get_left(), COBALT), arrow(sdk.get_right(), cloud.get_left(), COBALT)
        ak = arrow(env.get_top(), app.get_bottom(), AMBER)
        self.say("Gemini runs on Google's servers. Your app talks to it through an API, using Google's SDK, the waiter between you and the kitchen.",
                 FadeIn(h), FadeIn(app), FadeIn(sdk), FadeIn(cloud), GrowArrow(a1), GrowArrow(a2), run_time=1.8)
        self.say("The API key is read from the .env file at runtime. It never sits in your code, and never goes to GitHub.", FadeIn(env), GrowArrow(ak))
        req = T('"Explain entropy in two lines."', 22, COBALT, font=MONO).next_to(row, UP, buff=0.5)
        dot = Dot(app.get_right(), color=COBALT, radius=0.1)
        self.say("Your prompt travels out as a request, with the key attached so Google knows who is asking.",
                 FadeIn(req), MoveAlongPath(dot, Line(app.get_right(), cloud.get_left())), run_time=2)
        resp = T("response.text", 22, GREEN, font=MONO).next_to(cloud, DOWN, buff=0.4)
        dot2 = Dot(cloud.get_left(), color=GREEN, radius=0.1)
        self.say("A moment later the answer comes back as response dot text.",
                 FadeOut(dot), FadeIn(resp), MoveAlongPath(dot2, Line(cloud.get_left(), app.get_right())), run_time=2)
        js = box("chat_history.json", 3.2, 0.9, color=GREEN, font=MONO, size=22).next_to(sdk, DOWN, buff=1.0)
        aj = arrow(app.get_bottom() + RIGHT * 0.6, js.get_left(), GREEN)
        self.say("Your app shows it, and saves the question, the answer and the time to a JSON file: the tutor's long-term memory.",
                 FadeOut(dot2), FadeIn(js), GrowArrow(aj))
        self.clear()

        h = self.heading("Streamlit re-runs the whole script", "Week 1")
        lines = ['st.title("Gemini clone")', 'chat = []   # reset every run',
                 'if "chat" not in st.session_state:', '    st.session_state.chat = []', 'for m in st.session_state.chat:',
                 '    st.chat_message(m["role"]).markdown(...)', 'if q := st.chat_input():', '    ...']
        code = code_block(lines, 20).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        self.say("Streamlit has one idea to understand. Every click or message re-runs your script from top to bottom.", FadeIn(h), FadeIn(code))
        scan = Rectangle(width=code[0].width, height=0.36, fill_color=COBALT, fill_opacity=0.22, stroke_width=0).move_to(code[1][0]).align_to(code[0], LEFT)
        ss = box("st.session_state.chat", 3.8, 0.8, color=COBALT, font=MONO, size=20).to_edge(RIGHT, buff=0.5).shift(UP * 1.0)
        lv = box("chat", 3.8, 0.8, color=AMBER, font=MONO, size=20).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.2)
        ssn, lvn = T("messages: 0", 22, COBALT, font=MONO).next_to(ss, DOWN, buff=0.15), T("messages: 0", 22, AMBER, font=MONO).next_to(lv, DOWN, buff=0.15)
        self.add(scan)
        self.say("So a normal variable is born again, empty, on every run. Anything that must survive goes in session state.",
                 FadeIn(ss), FadeIn(lv), FadeIn(ssn), FadeIn(lvn))
        for k in range(1, 4):
            self.play(scan.animate.move_to(code[1][-1]).align_to(code[0], LEFT), run_time=1.0, rate_func=linear)
            self.play(Transform(ssn, T(f"messages: {2 * k}", 22, COBALT, font=MONO).move_to(ssn)),
                      Transform(lvn, T("messages: 0", 22, AMBER, font=MONO).move_to(lvn)), Indicate(lv, color=AMBER), run_time=0.6)
            self.play(scan.animate.move_to(code[1][0]).align_to(code[0], LEFT), run_time=0.3)
        self.caps.append((self.renderer.time - 5.7, self.renderer.time, "Three messages, three reruns: session state keeps growing, the plain variable starts empty each time."))
        self.say("Session state lasts as long as the browser tab. The JSON file lasts forever. You need both.")
        self.clear()


class W2Agent(Lesson):
    KICKER = "Week 2 · Agents"
    TITLE = "From chatbot to agent"

    def construct(self):
        self.title_card()
        h = self.heading("The agent loop", "Week 2")
        names = ["perceive", "decide", "act", "remember"]
        subs = ["a message, the clock", "is anything due?", "answer, or quiz", "save to JSON"]
        pos = [UP * 1.7, RIGHT * 3.6, DOWN * 1.9, LEFT * 3.6]
        nodes = VGroup(*[VGroup(box(n, 2.6, 0.9, size=28, font=SERIF), T(s, 20, SLATE)).arrange(DOWN, buff=0.12).move_to(p + DOWN * 0.2) for n, s, p in zip(names, subs, pos)])
        arcs = VGroup(*[CurvedArrow(nodes[i][0].get_center() + (pos[(i + 1) % 4] - pos[i]) * 0.28, nodes[(i + 1) % 4][0].get_center() - (pos[(i + 1) % 4] - pos[i]) * 0.28,
                                    color=SLATE, angle=-PI / 4) for i in range(4)])
        self.say("A chatbot answers and waits. An agent runs a loop: it perceives what's happening, decides what to do, acts, and remembers what happened.",
                 FadeIn(h), LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.3), Create(arcs), run_time=2.5)
        brain = T("brain: Gemini   ·   memory: JSON   ·   tools: quiz writer, grader", 24, SLATE).to_edge(DOWN, buff=0.5)
        self.say("Gemini is the brain, a JSON file is the memory, and the quiz writer and grader are its tools.", FadeIn(brain))
        self.say("The interesting part is decide. This week it's a rule we write. By week five, a reinforcement learning agent learns it.",
                 Indicate(nodes[1], color=AMBER, scale_factor=1.15), run_time=1.5)
        self.clear()

        h = self.heading("Two triggers nobody asked for", "Week 2")
        c_title = T("counter", 26, AMBER, font=MONO).shift(LEFT * 3.5 + UP * 1.6)
        bubbles = VGroup(*[box(f"Q{i}", 1.0, 0.6, color=SLATE, font=MONO, size=20) for i in range(1, 6)]).arrange(RIGHT, buff=0.15).next_to(c_title, DOWN, buff=0.5)
        self.say("Trigger one, a counter. After every five questions, the bot picks one of them at random and quizzes you on it.", FadeIn(h), FadeIn(c_title),
                 LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bubbles], lag_ratio=0.4), run_time=2.5)
        pick = SurroundingRectangle(bubbles[2], color=AMBER, buff=0.06, stroke_width=4)
        quiz1 = box("Pop quiz on Q3", 3.0, 0.7, color=AMBER, size=22).next_to(bubbles, DOWN, buff=0.4)
        self.play(Create(pick), FadeIn(quiz1))
        t_title = T("clock", 26, AMBER, font=MONO).shift(RIGHT * 3.0 + UP * 1.6)
        clock = Circle(radius=0.9, color=SLATE).next_to(t_title, DOWN, buff=0.4)
        hand = Line(clock.get_center(), clock.get_center() + UP * 0.75, color=INK, stroke_width=5)
        lbl = T("0 min", 22, SLATE, font=MONO).next_to(clock, RIGHT, buff=0.3)
        self.say("Trigger two, a clock. On every rerun, the bot checks whether a question is ten minutes old and not yet quizzed.", FadeIn(t_title), Create(clock), Create(hand), FadeIn(lbl))
        self.play(Rotate(hand, -2 * PI * 10 / 12, about_point=clock.get_center()), Transform(lbl, T("10 min", 22, AMBER, font=MONO).move_to(lbl)), run_time=2)
        quiz2 = box("Recall check", 2.6, 0.7, color=AMBER, size=22).next_to(clock, DOWN, buff=0.4)
        self.say("If one is, the bot interrupts you, before you've even typed.", FadeIn(quiz2, shift=UP * 0.2))
        self.clear()

        h = self.heading("A grade your code can use", "Week 2")
        txt = T('"Correct! Mostly right, though\nyou missed the discount\nfactor..."', 22, SLATE, font=MONO)
        jsn = code_block(['{', '  "grade": 1,', '  "feedback": "Missed gamma."', '}'], 22)
        vs = T("vs", 26, SLATE)
        VGroup(txt, vs, jsn).arrange(RIGHT, buff=0.7).shift(UP * 0.6)
        self.say("A prose grade is fine for a human but awful for code. Ask Gemini for JSON instead, and you get a number you can store.",
                 FadeIn(h), FadeIn(txt), FadeIn(vs), FadeIn(jsn))
        g = VGroup(*[VGroup(T(n, 80, COBALT, font=SERIF), T(d, 22, SLATE)).arrange(DOWN, buff=0.1) for n, d in
                     [("0", "forgot / wrong"), ("1", "partly right"), ("2", "clearly correct")]]).arrange(RIGHT, buff=1.6).shift(DOWN * 2.0)
        self.say("Three grades: zero, one and two. Remember them. In week five they become what the agent observes, and the reward it learns from.",
                 LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in g], lag_ratio=0.3))
        self.clear()
