"""A 4x4 'study room' gridworld for learning tabular Q-learning.

  S . . .        S = start, G = exam hall (+10)
  . # . X        # = wall, X = phone distraction (-5, episode ends)
  . . . .        every move costs -0.1 (time is precious)
  X . . G
"""
LAYOUT = ["S...",
          ".#.X",
          "....",
          "X..G"]
ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]          # up, down, left, right
ACTION_NAMES = ["^", "v", "<", ">"]


class GridWorld:
    def __init__(self, layout=LAYOUT, step_cost=-0.1, max_steps=50):
        self.grid = [list(r) for r in layout]
        self.h, self.w = len(self.grid), len(self.grid[0])
        self.step_cost, self.max_steps = step_cost, max_steps
        self.start = next((r, c) for r in range(self.h) for c in range(self.w) if self.grid[r][c] == "S")

    @property
    def n_states(self):
        return self.h * self.w

    n_actions = len(ACTIONS)

    def reset(self):
        self.pos, self.t = self.start, 0
        return self._sid()

    def _sid(self):
        return self.pos[0] * self.w + self.pos[1]

    def step(self, a):
        self.t += 1
        dr, dc = ACTIONS[a]
        r, c = self.pos[0] + dr, self.pos[1] + dc
        if 0 <= r < self.h and 0 <= c < self.w and self.grid[r][c] != "#":
            self.pos = (r, c)
        cell = self.grid[self.pos[0]][self.pos[1]]
        if cell == "G":
            return self._sid(), 10.0, True, {}
        if cell == "X":
            return self._sid(), -5.0, True, {}
        return self._sid(), self.step_cost, self.t >= self.max_steps, {}

    def render_policy(self, q):
        rows = []
        for r in range(self.h):
            row = ""
            for c in range(self.w):
                ch = self.grid[r][c]
                if ch in "#GX":
                    row += ch
                else:
                    s = r * self.w + c
                    row += ACTION_NAMES[max(range(4), key=lambda a: q[s][a])]
            rows.append(row)
        return "\n".join(rows)
