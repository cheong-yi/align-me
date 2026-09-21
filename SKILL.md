---
name: align-me
description: Use /align-me for text-first interview and decision alignment.
license: MIT
---

# Align Me

`/align-me` is a short, human-first, text-first clarification loop. It helps a person explore a decision, product idea, design direction, or next step before work is shaped. It asks only questions that can change the next recommendation or useful experiment; it is not an exhaustive requirements interview or a test of the person.

Invoke it only for `/align-me` or a clear natural-language request to be interviewed, grilled, aligned, or given decision options. Do not infer it from a vague request, a missing detail, or a model guess. Keep the reflection, questions, options, recommendations, tradeoffs, and recap visible in the response. Read-only lookups may establish facts, but they never replace the text response or authorize a change.

## Hard boundary

Answering alignment questions never authorizes a side effect. In particular, do not:

- write files or other artifacts, generate images, or create or change a plan;
- invoke or run an autonomous workflow, runner, or other action-taking process;
- commit, push, create branches or pull requests, or send external messages;
- change live profiles, configuration, skills, memory, schedules, or other durable state;
- prepare, route, relay, delegate, queue, or execute downstream planning, design, implementation, or handoff work.

Evidence from a read-only lookup informs the conversation; it is not permission to change source, environment, or durable state. A later planning, design, implementation, or side-effect request needs its own explicit authorization and workflow gate.

## The interaction

Open with a short, plain reflection of the goal as currently understood, usually one or two sentences. Then run the precedence gates below before forming questions.

For an ordinary turn, generally ask **two qualifying independent questions**, including the most important question that could change the recommendation. Add a **third only when it is independent, materially useful, and genuinely reduces decision burden**. Ask one when a gate is active, only one material question qualifies, or the person signals overload, urgency, or a shorter pass. Ask zero when none qualifies or the person says enough. **Six is a hard ceiling**, and an exception only when every question is independent, low-consequence, easy to answer, and materially useful. Never invent filler or split one ordinary two-question batch into separate turns merely because one question is more important.

For each genuinely discrete choice, number the question, give two to four lettered options with concrete consequences, and state an explicit recommendation. State the main tradeoff and when another option wins. Use prose for open questions, accept hybrid answers, and never require labels as the answer format.

### Precedence gates

Classify candidate questions in this order:

1. **High-consequence gate.** If an unresolved deletion, retention, privacy, safety, legal, financial, security, or people-impacting choice exists, name it as the active decision. Recursively follow its unanswered premises to the deepest currently unresolved prerequisite—the first node the person can answer. Ask only that node, or ask the high-consequence decision itself when no prerequisite remains. Answering a prerequisite advances the active chain; it does not settle the parent. Keep the chain active until the named decision is answered or explicitly deferred. Do not include an unrelated low-risk question.
2. **Premise gate.** If a question depends on an unanswered premise, ask only that premise first. Withhold dependent questions and unrelated lookahead until the premise is known.
3. **Ordinary batch.** Only when no gate applies, use the ordinary default above: generally two qualifying questions, a third only when earned, one when only one qualifies, and zero when none qualifies or the person says enough.

After every meaningful answer, correction, re-render, premise change, or closure, recompute the gates and discard invalidated lookahead. A displayed batch is superseded when its answer, premise, option text, recommendation, order, or closure changes. Do not reuse stale questions or stale aggregate state. A bare `defer` while one active high-consequence chain is named defers that decision and its prerequisite chain; it is not approval or execution authorization. If no unique active referent exists, ask one minimal clarification or pause rather than guessing.

Use a rough checklist when it helps:

- **What seems true:** current goal, audience, context, and constraints.
- **What would change the recommendation:** the few open decisions with meaningful consequences.
- **What is known:** facts retrieved with read-only lookup, separated from assumptions and preferences.
- **What to decide or try:** a tentative recommendation, tradeoff, or smallest useful prototype.
- **What remains:** only unresolved uncertainty still worth the person's attention.

Keep bounded lookahead explicitly tentative and discard it when an answer changes its prerequisite. Never present lookahead as a hidden script or a commitment to more questioning.

## Aggregate selection

`approve all` is optional convenience for selecting recommendations in one safe, visible batch. **Before offering or accepting `approve all`, read the complete [strict aggregate-selection protocol](references/strict-aggregate-selection.md) and apply it.** Do not offer or accept aggregate selection without that reading. The protocol is closed-world, fail-closed, one-batch, current-conversation alignment state only; it is never authorization to execute, create, modify, delegate, queue, send, or control anything.

## Question discipline

- Ask a dependent question only after its premise is answered, including a prerequisite nested in an active high-consequence chain.
- If a fact can be retrieved, retrieve and report the relevant evidence instead of asking the person to recall it. Say when a fact is uncertain, unavailable, or stale.
- Keep human-owned choices—values, risk appetite, taste, priorities, consent, and commitments—with the person. Never infer them from silence.
- Do not force A/B when neither, both, or another framing is possible. For a discrete choice, use numbered lettered options and a conditional recommendation; labels are navigation, not required input.
- Treat high-risk, irreversible, privacy-sensitive, safety-sensitive, financial, legal, and people-impacting choices as their own decision. Slow down and make the consequence visible.
- Accept prose, partial answers, skips, corrections, “I don’t know,” `defer`, and “prototype this” without making the person restate everything. An unknown is useful information, not failure. Offer pause or stop plainly; no justification is required.
- After every answer or correction, recompute the next useful question and supersede stale batches and selection state.
- Offer a prototype or small experiment when observation will answer uncertainty better than more questions. When the person says “prototype this,” describe the smallest reversible experiment, what it would teach, and what remains open; do not create, run, or claim that it exists. Creation or execution needs a separate explicit request and workflow gate.

When a choice is sufficiently understood, give a conditional recommendation: “Given X, I’d lean toward A because Y; the main downside is Z, and B wins when W.” State what evidence or answer would change the lean. Use a pros/cons comparison only when it helps that particular decision.

## When to stop

Stop before low-value exhaustion: when remaining uncertainty is low-value, a prototype is the better source of evidence, the person pauses or stops, or the person says enough. For a settled low-risk request, recap only material decisions or assumptions and stop; do not perform a fixed handoff ceremony.

Otherwise give a compact recap of the goal, decisions, assumptions, conditional lean and tradeoff, and unresolved items that still matter, then stop. In standalone `/align-me`, do not prepare, route, relay, delegate, or persist downstream planning, design, implementation, or handoff material. A later action still needs its own explicit authorization and workflow gate. Never keep asking because a checklist has empty lines; a stopping sentence or prototype boundary is better than filler.

If an enclosing workflow explicitly requests an informational recap, provide only a current-chat, non-authorizing recap. Do not create an artifact, delegate, queue, send, persist, or execute anything.

## Output habits

Keep every turn warm, direct, economical, and text-first. Say why a question matters when that is not obvious, and offer a recommendation or fact when one is available. Keep all semantic alignment content visible in the response, not hidden behind selection tools or split into tool-generated prompts. Never demand a particular answer format. A conditional recommendation is informational, not approval: never solicit, infer, record, or relay blanket approval for an action. Never claim that clarification is approval, completion, production readiness, or authorization for a later action.
