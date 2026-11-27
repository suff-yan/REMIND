---
title: Your toolkit
minutes: 45
checkpoint:
  kind: local
  title: Set up your machine
  prompt: Tick each step as you finish it. Stuck? Paste the exact error into the group; someone has seen it before.
  steps:
    - "Install Python 3.11 or newer from python.org (Windows: install WSL first and use Ubuntu's Python). Check with `python3 --version`."
    - "Install VS Code and its Python extension."
    - "Open a terminal and try `pwd`, `ls`, `mkdir remind-play`, `cd remind-play`."
    - "Create a virtual environment with `python3 -m venv venv` and activate it with `source venv/bin/activate`. You should see `(venv)` in the prompt."
    - "Run `pip install numpy`, then `python -c \"import numpy; print(numpy.__version__)\"`."
    - "Install git, then run `git clone https://github.com/suff-yan/REMIND.git` and open the folder in VS Code with `code REMIND`."
quiz:
  - q: "You open a new terminal and `python` can't find a package you installed yesterday. What is the most likely cause?"
    options: ["The package was deleted overnight", "Your virtual environment isn't activated in this terminal", "pip only works on Mondays", "VS Code needs to be reinstalled"]
    answer: 1
    explain: "Packages live inside the venv. A new terminal starts outside it; run `source venv/bin/activate` again."
  - q: "What does `cd ..` do?"
    options: ["Deletes the current folder", "Moves you to the parent folder", "Lists hidden files", "Creates a folder named .."]
    answer: 1
    explain: "`..` always means 'the folder one level up'."
  - q: "Why do we create one virtual environment per project?"
    options: ["It makes Python run faster", "So each project gets its own package versions without clashing", "Git requires it", "It hides your code from others"]
    answer: 1
    explain: "Two projects may need different versions of the same library. A venv keeps them separate."
  - q: "Which command copies a GitHub repository to your laptop?"
    options: ["git push", "git commit", "git clone <url>", "git status"]
    answer: 2
    explain: "`clone` downloads the repo with its full history. `push` sends your commits up; `commit` saves a snapshot locally."
  - q: "On Windows, the handbook recommends WSL. Why?"
    options: ["It's required by Gemini", "It gives you a Linux terminal, so every command in the course works as written", "It's faster than a Mac", "Streamlit only runs on Linux"]
    answer: 1
    explain: "All instructions in the course are Linux/macOS shell commands. WSL lets Windows users follow them exactly."
resources:
  - label: The Missing Semester (MIT), lecture 1 on the shell
    url: https://missing.csail.mit.edu/2020/course-shell/
    note: the best 1-hour intro to the terminal
  - label: Install WSL (Microsoft)
    url: https://learn.microsoft.com/windows/wsl/install
  - label: Python venv tutorial
    url: https://docs.python.org/3/tutorial/venv.html
  - label: Git in 15 minutes (GitHub Skills)
    url: https://skills.github.com/
---
This project assumes nothing except a laptop and some patience. This first section gets the boring part out of the way: by the end you will have a terminal you're not scared of, an editor, Python, a private box of packages for the project, and a copy of the course repository.

## The terminal

A terminal is a text interface to your computer. Instead of clicking a folder, you type `cd folder`. It feels slower for a day and then becomes much faster. You only need a handful of commands for this whole project:

| Command | Meaning |
|---|---|
| `pwd` | print working directory: where am I? |
| `ls` | list what's here |
| `cd name` / `cd ..` | go into a folder / go up one level |
| `mkdir name` | make a folder |
| `python3 file.py` | run a Python file |

On Windows, install **WSL** (Windows Subsystem for Linux) and use its Ubuntu terminal. Every command in this course is written for Linux and macOS, and WSL makes them work unchanged.

## Python and VS Code

Install Python 3.11 or newer. Check it with `python3 --version`. Install **VS Code** with its Python extension. You will write code in VS Code and run it in the terminal, either the system one or VS Code's built-in terminal (View → Terminal).

## Virtual environments

Every project needs libraries: Gemini's SDK, Streamlit, NumPy. Installing them globally causes trouble the day two projects need different versions. A **virtual environment** is a private folder of packages for one project:

```bash
python3 -m venv venv          # create it once
source venv/bin/activate      # enter it, in every new terminal
pip install -r requirements.txt
```

The prompt shows `(venv)` while it's active. The most common bug of the whole course is "it worked yesterday": the fix is almost always to activate the venv again.

## Git, just enough

Git records snapshots of your code; GitHub hosts them. In this project you need three things: `git clone` to get the course repo, and later `git add`, `git commit` and `git push` to submit your own work. We'll walk through submitting in Week 2.

> Everything in Weeks 0, 3 and 4 also runs right here in the browser, so if setup is fighting you, keep learning and fix it in parallel.
