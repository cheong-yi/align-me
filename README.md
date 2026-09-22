# align-me

![A guide compares two paths, asks one careful question, and marks a small reversible test.](docs/assets/readme/align-me.png)

> **Turn a vague request into a clear decision before planning or building.**

`align-me` is a portable Agent Skill that helps people settle important choices before an agent starts work.

## Why it helps

When the goal is known but a few choices still need a human answer, agents often guess or ask too much. `align-me` does neither: it asks only what could change its recommendation, explains the tradeoffs, and stops when the decision is clear.

It does not plan, build, or act; that needs a separate request.

## Use it

```text
/align-me Help me decide what belongs in the first release.
```

If your host has no skill command, ask in plain language:

```text
Use align-me to interview me about this decision before we plan or build it.
```

The agent reflects the goal, usually asks two independent questions, gives concrete options and a recommendation, then adapts and stops. You can answer in prose, skip, correct an assumption, say “I don’t know,” or stop. See [`SKILL.md`](SKILL.md) for the full contract.

Consequential choices, such as privacy or safety, and unanswered prerequisites take precedence over the ordinary two-question batch.

## Example

> **Human:** Help me choose the first version of sharing for my notes app. Do not plan or build it yet.
>
> **Agent:** You want useful sharing without taking on full collaboration.
>
> **1. Who can open a shared note?**
> - **A. Anyone with the link** — faster, with weak access control.
> - **B. Invited accounts** — more work, with explicit access.
>
> I recommend **B** if notes may be private.
>
> **2. Can recipients edit?**
> - **A. Read only** — smaller, with no edit conflicts.
> - **B. Edit** — more collaborative, but adds permissions, history, and conflict handling.
>
> I recommend **A** unless collaboration is the main goal.
>
> **Human:** Invited accounts, read-only.
>
> **Agent:** First release: invite-only, read-only sharing. It gives you clear access control without taking on collaborative editing. We are aligned, so I’ll stop here.

The decision is ready for a separate planning request. No plan or implementation has started.

## Install it

Copy this structure into your host’s supported skill directory:

```text
align-me/
├── SKILL.md
├── LICENSE
└── references/
    └── strict-aggregate-selection.md
```

Keep the relative `references/` path and follow the host’s discovery rules. This repository does not install itself or provide a universal slash command.

## Advanced selection

Most uses do not need `approve all`. Before using it, read [`references/strict-aggregate-selection.md`](references/strict-aggregate-selection.md). It selects recommendations from one visible batch; it never authorizes execution.

## Evidence

```sh
python3 -B eval/check.py
python3 -B -m unittest discover -s tests
```

[`eval/EVIDENCE.md`](eval/EVIDENCE.md) describes the synthetic cases, bounded historical results, and limits. It does not predict every agent or runtime, and the checks are not a complete semantic or privacy review.

## License and lineage

MIT. See [`LICENSE`](LICENSE). The project builds on the MIT-licensed [`swyxio/skills` align-me](https://github.com/swyxio/skills/blob/main/align-me/SKILL.md); its notice is retained for possible adapted portions. [Matt Pocock’s `grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) is conceptual lineage. Neither source endorses this project.
