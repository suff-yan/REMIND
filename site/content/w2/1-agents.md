---
title: But what even is agentic AI?
minutes: 35
video: w2_agent
videoTitle: From chatbot to agent
quiz:
  - q: "What makes a system 'agentic' rather than a plain chatbot?"
    options: ["It uses a bigger model", "It decides its own next action, such as quizzing you without being asked", "It has a nicer UI", "It answers faster"]
    answer: 1
    explain: "Agency is the ability to choose what to do next, not just respond."
  - q: "Which is NOT one of the four parts of an agent in this course?"
    options: ["A brain (LLM)", "Memory", "Tools it can call", "A GPU on your laptop"]
    answer: 3
    explain: "Brain, memory, tools, decision. The model runs on Google's servers."
  - q: "'Agentic AI' vs 'an AI agent':"
    options: ["Same thing", "Agentic AI is the idea; an AI agent is a program built with it", "An agent is the idea; agentic AI is the program", "Agentic AI needs RL"]
    answer: 1
    explain: "Re-Mind is an AI agent built on agentic principles."
  - q: "In Re-Mind, which decision becomes learned by RL in Week 5?"
    options: ["What font to use", "When to quiz you on each concept", "Which model to call", "How to grade"]
    answer: 1
    explain: "Grading stays with Gemini; the timing is learned."
  - q: "Put the agent loop in order:"
    options: ["act → perceive → remember → decide", "perceive → decide → act → remember", "remember → act → decide → perceive", "decide → remember → perceive → act"]
    answer: 1
    explain: "Notice what's happening, choose, do it, store what happened."
resources:
  - label: Anthropic, building effective agents
    url: https://www.anthropic.com/research/building-effective-agents
  - label: Lilian Weng, LLM-powered autonomous agents
    url: https://lilianweng.github.io/posts/2023-06-23-agent/
---
## Definition

A normal model answers whatever you give it and then waits. An **agentic** system can also take initiative: store information, plan, choose tools, check its own work, and act without being asked at every step. The key idea is **agency**: the system decides its next action.

An agent usually has four parts, running in a loop:

| Part | In Re-Mind |
|---|---|
| **Brain** (an LLM) | Gemini: answers, writes quizzes, grades |
| **Memory** | a JSON file of concepts and their review history |
| **Tools** | quiz writer, JSON grader, concept extractor |
| **Decision** | *when* to quiz you. A fixed rule this week, a learned policy by Week 5 |

The loop: **perceive** (a new message, the clock) → **decide** (is anything due?) → **act** (answer, or interrupt with a quiz) → **remember** (save what happened).

## Agentic AI v/s AI agents

*Agentic AI* is the design idea: autonomy and initiative. An *AI agent* is a concrete program built with that idea, like a research bot, a scheduling assistant, or Re-Mind. The idea versus the thing.

## OK, but how is this related to the project?

Last year Re-Mind's decision was a rule we wrote: quiz every 5 questions, or after 10 minutes. This year that rule becomes the thing that **learns**. Weeks 3 and 4 teach the RL to do it; this week we build the agent's body so there's something for the RL to control.
