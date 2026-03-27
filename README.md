# Skills Hub

A collection of Claude Code skills by [@kohliarpit](https://github.com/kohliarpit).

---

## Skills

| Skill | Description |
|-------|-------------|
| [youtube-to-steps](./youtube-to-steps) | Convert any YouTube video into structured, actionable steps |

---

## Installation

### Install a single skill

```bash
curl -L https://github.com/kohliarpit/Skills-hub/archive/refs/heads/main.tar.gz \
  | tar xz -C /tmp && \
  cp -r /tmp/Skills-hub-main/youtube-to-steps ~/.claude/skills/
```

### Clone the full repo

```bash
git clone https://github.com/kohliarpit/Skills-hub.git /tmp/skills-hub
cp -r /tmp/skills-hub/youtube-to-steps ~/.claude/skills/
```

No restart needed — Claude Code auto-detects skills in `~/.claude/skills/`.

---

## youtube-to-steps

Converts any YouTube video into clean, numbered markdown steps using a Gemini → Claude → Codex pipeline.

**Triggers:**
- `/youtube-to-steps <url>`
- `/youtube-to-steps <url> <N>` — request exactly N steps
- "turn this video into steps"
- "extract steps from this video"
- Any YouTube URL + "steps" or "how to follow"

**Output:** Saves a markdown file to `~/documents/youtube-steps/<video-id>-steps.md`

**Requirements:**
- Python 3
- Gemini API key (set `GEMINI_API_KEY` env var)
- [Codex CLI](https://github.com/openai/codex) (optional, for code review step)
