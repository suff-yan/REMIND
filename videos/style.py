"""Shared look for Re-Mind animations: same palette and type as the website.
Each scene narrates with self.say(caption, *animations); captions are written to
captions/<SceneName>.vtt with the exact timings, so you can record a voiceover over them later."""
import os
from manim import *

PAPER, STONE, CHARCOAL = "#FAFAF8", "#F2F1ED", "#16181D"
INK, SLATE, RULE = "#141413", "#575651", "#E2E0D8"
COBALT, AMBER, GREEN = "#1D4ED8", "#D97706", "#2F7D4F"
SERIF, SANS, MONO = "RemindSerif", "Inter", "JetBrains Mono"

config.background_color = PAPER
config.pixel_width, config.pixel_height, config.frame_rate = 1920, 1080, 30

tex = TexTemplate()
tex.add_to_preamble(r"\usepackage{amsmath}")


def T(s, size=30, color=INK, font=SANS, weight=NORMAL, **kw):
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def H(s, size=46, color=INK):
    return Text(s, font=SERIF, font_size=size, color=color)


def M(*s, size=40, color=INK):
    if s and isinstance(s[-1], (int, float)):
        *s, size = s
    return MathTex(*s, font_size=size, color=color, tex_template=tex)


def fit(m, w=12.5):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def axes(x_range, y_range, x_length=10.5, y_length=4.6, xnums=None, ynums=None):
    ax = Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
              axis_config={"color": SLATE, "include_tip": False, "font_size": 24},
              x_axis_config={"numbers_to_include": xnums or []}, y_axis_config={"numbers_to_include": ynums or []})
    for a in (ax.x_axis, ax.y_axis):
        if hasattr(a, "numbers"):
            a.numbers.set_color(SLATE)
    return ax


def line_box(row):
    return SurroundingRectangle(row, color=AMBER, buff=0.08, stroke_width=3)


def mono(s, size=24, color=INK):
    return Text(s, font=MONO, font_size=size, color=color)


def code_block(lines, size=22, width=None, highlight=None):
    """Charcoal code panel. highlight: {line_index: color}. Indentation is kept by shifting lines."""
    highlight = highlight or {}
    cw = Text("M" * 10, font=MONO, font_size=size).width / 10
    rows = VGroup(*[Text(l.strip() or "\u00a0", font=MONO, font_size=size, color=highlight.get(i, "#E6E6E1"))
                    for i, l in enumerate(lines)])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    for r, l in zip(rows, lines):
        r.shift(RIGHT * cw * (len(l) - len(l.lstrip(" "))))
    bg = RoundedRectangle(corner_radius=0.08, width=(width or rows.width + 0.7), height=rows.height + 0.55,
                          fill_color=CHARCOAL, fill_opacity=1, stroke_width=0)
    rows.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.35)
    return VGroup(bg, rows)


def box(label, w=2.6, h=1.0, color=COBALT, fill=WHITE, size=26, font=SANS):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2.5,
                         fill_color=fill, fill_opacity=1)
    t = Text(label, font=font, font_size=size, color=INK).move_to(r)
    if t.width > w - 0.3:
        t.scale_to_fit_width(w - 0.3)
    return VGroup(r, t)


def arrow(a, b, color=SLATE, buff=0.1):
    return Arrow(a, b, color=color, buff=buff, stroke_width=3, max_tip_length_to_length_ratio=0.12)


class Lesson(Scene):
    KICKER = ""
    TITLE = ""

    def setup(self):
        self.caps = []

    def say(self, text, *anims, run_time=None, min_rate=2.6, wait_after=0.25):
        start = self.renderer.time
        if anims:
            self.play(*anims, run_time=run_time or 1.2)
        need = len(text.split()) / min_rate
        spent = self.renderer.time - start
        if need > spent:
            self.wait(need - spent)
        if wait_after:
            self.wait(wait_after)
        self.caps.append((start, self.renderer.time, text))

    def heading(self, s, kicker=None):
        h = H(s, 40).to_corner(UL, buff=0.6)
        grp = VGroup(h)
        if kicker:
            k = T(kicker.upper(), 16, SLATE, font=MONO).next_to(h, UP, aligned_edge=LEFT, buff=0.15)
            grp.add(k)
        return grp

    def title_card(self):
        k = T(self.KICKER.upper(), 20, AMBER, font=MONO)
        t = H(self.TITLE, 64)
        if t.width > 12:
            t.scale_to_fit_width(12)
        brand = T("Re-Mind · WiDS 6.0", 20, SLATE, font=MONO)
        g = VGroup(k, t).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=1.2)
        brand.to_corner(DL, buff=0.6)
        rule = Line(LEFT, RIGHT, color=COBALT, stroke_width=4).set_width(1.6).next_to(g, DOWN, aligned_edge=LEFT, buff=0.4)
        self.say(f"{self.TITLE}.", FadeIn(g, shift=UP * 0.2), Create(rule), FadeIn(brand), run_time=1.2, wait_after=0.6)
        self.play(FadeOut(VGroup(g, rule, brand)), run_time=0.6)

    def clear(self, run_time=0.6):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    def tear_down(self):
        def ts(t):
            h, m = int(t // 3600), int(t % 3600 // 60)
            return f"{h:02d}:{m:02d}:{t % 60:06.3f}"
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captions", f"{type(self).__name__}.vtt")
        with open(out, "w") as f:
            f.write("WEBVTT\n\n")
            for i, (a, b, s) in enumerate(self.caps, 1):
                f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{s}\n\n")
        super().tear_down()
