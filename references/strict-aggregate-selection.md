# Strict aggregate selection

`approve all` is an optional convenience for selecting the recommendations in one safe, visible batch. It is not approval to execute, create, modify, delegate, queue, send, or control anything. Use this protocol before offering or accepting it. The following rules are closed-world and fail closed:

- Every covered item must be ordinary, low-consequence, reversible, homogeneous, visible, independent, and current. Recording its value must have no external, durable, operational, or live effect; before separate authorization it must remain replaceable ephemeral chat state. Unknown, ambiguous, stale, potentially consequential, security-sensitive, conditional, premise-dependent, protected, or coupled items are ineligible.
- This skill text does not claim a runtime parser, authoritative database, durable batch store, or user-identity service. Offer or accept aggregate selection only when the assistant can bind it to exactly one current visible batch in the same conversation, thread, and requesting-user scope, and verify the visible wording, options, recommendations, premises, gates, provenance, and currentness. If that binding cannot be established, suppress or reject aggregate selection.
- The current batch has one-use conversational scope. It is superseded or expired after an answer, correction, re-render, premise change, closure, or newer batch. Never replay it across chats or threads, and reject when multiple active batches could match.
- Normalize only by trimming leading/trailing ASCII spaces or tabs, collapsing internal ASCII space/tab runs to one, and applying ASCII case-folding. Accept aggregate syntax only when the whole normalized message is exactly `approve all`. Reject newlines, Unicode whitespace, zero-width or confusable characters, punctuation, quotes, extra words, aliases, names, exceptions, and overrides. Forms such as `approve all, but 2B → 2A` are explicit non-aggregate responses; restate exact individual choices or reject them.
- Before acceptance, preview the recommendations against the current dependency closure. Traverse hidden and tentative dependencies for validation only; never approve or inherit them. If a required hidden or tentative, unknown, protected, consequential, coupled, cyclic, or unresolved item appears, reject zero, invalidate the batch, surface the gate or dependency, and recapture. Newly exposed items always require fresh exact selection.
- Use a bounded, deterministic fixed-point check with no unbounded retry. If closure cannot converge or current state changes during validation, suppress or reject the whole aggregate rather than looping or partially accepting it.
- Acceptance is atomic: apply zero selections on any rejection. Retain selected values only as ephemeral state after every visible recommendation passes current eligibility and closure checks, and then only for a recap in the current chat. Discard that state on rejection, supersession, expiry, correction, or conversation boundary. It is never durable state, downstream input, or authority.

## Operational checklist

1. Confirm that the request is the whole normalized message `approve all`, with no disallowed variation.
2. Bind it to exactly one current, visible, one-use batch in the same conversation, thread, and requesting-user scope.
3. Verify every visible recommendation's wording, options, recommendation, premises, gates, provenance, independence, eligibility, and currentness.
4. Compute the dependency closure for validation only with a bounded deterministic fixed-point check; reject on any hidden, tentative, unknown, protected, consequential, coupled, cyclic, or unresolved item, or on a state change.
5. Apply zero or all selections atomically. Retain eligible values only as replaceable ephemeral chat state for the current recap, and discard it on any invalidation or boundary.

Aggregate selection is never execution, authorization, durable storage, downstream input, or a substitute for a separate explicit request and workflow gate.
