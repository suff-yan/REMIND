## Course material

| What | Where |
|---|---|
| Course repository | [github.com/suff-yan/REMIND](https://github.com/suff-yan/REMIND) |
| Handbook (PDF, all weeks) | [docs/remind_handbook.pdf](https://github.com/suff-yan/REMIND/blob/main/docs/remind_handbook.pdf) |
| Weekly plan, hour by hour | [WEEKLY_PLAN.md](https://github.com/suff-yan/REMIND/blob/main/WEEKLY_PLAN.md) |
| Mid-term template | [templates/midterm](https://github.com/suff-yan/REMIND/tree/main/templates/midterm) |
| End-term template | [templates/endterm](https://github.com/suff-yan/REMIND/tree/main/templates/endterm) |

## Setup troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError` for a package you installed | Activate the venv: `source venv/bin/activate` |
| `python: command not found` | Use `python3`, or install Python 3.11+ |
| Gemini `404 model not found` | Run `week1_foundations/examples/hello_gemini.py`, copy a *flash-lite* name into `GEMINI_MODEL` |
| Gemini `429 RESOURCE_EXHAUSTED` | Free-tier rate limit: wait a minute, use a lite model, cache answers while testing |
| Gemini `400 API key not valid` | `.env` must say `GEMINI_API_KEY=...` with no quotes or spaces; restart Streamlit |
| Streamlit page blank or stale | Stop with Ctrl+C and rerun; check the terminal for the real error |
| History vanishes on every message | You stored it in a normal variable; use `st.session_state` |
| Windows path errors | Use WSL and work inside `~/`, not `/mnt/c/...` |
| In-browser checkpoint stuck on "starting Python" | The first run downloads ~13 MB; wait or refresh. Works best in Chrome or Firefox. |

## Glossary

| Term | Meaning |
|---|---|
| **API / API key** | a doorway into someone else's system / the secret that identifies you to it |
| **Agent** | a program that decides its own next action in a loop: perceive, decide, act, remember |
| **Context window** | how much text a model reads in one call |
| **System instruction** | rules and personality that hold for a whole conversation |
| **JSON mode** | asking the model to reply with machine-readable JSON |
| **State, action, reward** | what the agent knows, what it can do, how good that was |
| **Policy** $\pi(s)$ | the agent's rule for choosing actions |
| **Return** $G_t$ | discounted sum of future rewards |
| **Discount** $\gamma$ | how much the future matters (0 to 1) |
| **Q-value** $Q(s,a)$ | expected return after taking $a$ in $s$ |
| **Learning rate** $\alpha$ | how far each estimate moves toward its target |
| **ε-greedy** | explore at random with probability ε |
| **Regret** | reward lost compared with always choosing the best option |
| **Stability** $S$ | days until recall drops to 90% |
| **Leitner boxes** | a rule-based ladder of review gaps |
| **Reward hacking** | an agent maximising the reward in a way you didn't intend |

## Go deeper

**Reinforcement learning**
- Sutton & Barto, [*Reinforcement Learning: An Introduction*](http://incompleteideas.net/book/the-book-2nd.html): free; chapters 1–3 and 6 cover this course
- David Silver, [RL lecture series](https://www.youtube.com/playlist?list=PLqYmG7hTraZDM-OYHWgPebj2MfCFzFObQ) (video)
- Hugging Face, [Deep RL course](https://huggingface.co/learn/deep-rl-course/unit0/introduction): where to go after tabular Q-learning
- OpenAI, [Spinning Up](https://spinningup.openai.com/): deep RL, once you're comfortable

**Spaced repetition and memory**
- Nicky Case, [How to remember anything forever-ish](https://ncase.me/remember/) (interactive)
- Gwern, [Spaced repetition for efficient learning](https://gwern.net/spaced-repetition)
- Open Spaced Repetition, [FSRS algorithm](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)
- Settles & Meeder, [A trainable spaced repetition model](https://aclanthology.org/P16-1174/) (Duolingo)

**LLMs and agents**
- Google, [Gemini API docs](https://ai.google.dev/gemini-api/docs)
- Anthropic, [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- Streamlit, [Chat and LLM app tutorials](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps)

**Python and maths, from zero**
- [Official Python tutorial](https://docs.python.org/3/tutorial/)
- [Python Tutor](https://pythontutor.com/visualize.html): watch your code run step by step
- [Seeing Theory](https://seeing-theory.brown.edu/): visual probability
- [3Blue1Brown](https://www.youtube.com/@3blue1brown): intuition for the maths
