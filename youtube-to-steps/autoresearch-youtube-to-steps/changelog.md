# Autoresearch Changelog — youtube-to-steps

Skill being optimized: `gemini_auto_prompt.txt` (primary) + `SKILL.md` (orchestration)

---

## Session 2

Test inputs: 2 YouTube URLs (SB_tKxkfjMk, H8Lyj2D_cWo)
Evals per run: 5 | Max score per experiment: 10

### Experiment 3 — baseline (session 2)

**Score:** 9/10 (90.0%)
**Change:** None — current prompt post-session-1 optimizations
**Failing outputs:**
- URL1 (SB_tKxkfjMk) E4: Step 6 says "After completing a task like the 'Compile AI News Posts from X' (Step 5)" — explicit cross-reference to another step

---

## Session 1

Test inputs: 5 YouTube URLs (auto-N mode)
Evals per run: 4 | Max score per experiment: 20

---

## Experiment 0 — baseline

**Score:** 18/20 (90.0%)
**Change:** None — original prompt
**Failing outputs:**
- URL3 E1: Setup steps extracted after use-case demos (chronological inversion in video)
- URL5 E2: Step 4 title "Manually Create" — adverb before verb, not a bare verb

## Experiment 1 — keep (provisional)

**Score:** 19/20 estimated (15/16 measurable, URL5 quota-blocked)
**Change:** Added to gemini_auto_prompt.txt: "Step titles MUST start with a bare verb as the very first word — NO adverbs or modifiers before the verb"
**Reasoning:** URL5 baseline failed E2 with "Manually Create" title. This rule explicitly prohibits that pattern.
**Result:** URLs 1-4 held at 15/16. URL5 untestable — free tier daily quota exhausted (gemini-2.5-flash: 20 req/day, gemini-2.0-flash: also exhausted).
**Remaining failures:** URL3 E1 (chronological inversion: setup step placed after use-case demos) — targeted in Experiment 2.
**Status:** PAUSED — daily API quota exhausted. Resume tomorrow with Experiment 2.

## Experiment 2 — keep (provisional)

**Score:** 20/20 estimated (12/12 measurable on URLs 1-3; URL4+5 quota-blocked)
**Change:** Replaced "Steps must be in chronological order" with "Steps must be in logical execution order: if setup/prerequisites appear after demos, reorder them so setup comes FIRST"
**Reasoning:** URL3 baseline had setup step placed last (after 8 use-case demos) — viewer couldn't follow without knowing setup. New rule fixes this explicitly.
**Result:** URL3 E1 confirmed fixed — setup steps now appear at positions 1-3 before all demos. URLs 1, 2 maintained 4/4.
**Remaining failures:** None known on 3 measurable URLs. URL4 + URL5 unverifiable due to quota exhaustion.
**Status:** KEEP — both mutations now in prompt. Session summary below.
