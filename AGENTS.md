# AGENTS.md — hawk-search Development Workflow

## Core Principle: Design Review Before Implementation

Before starting implementation on any issue or feature:

1. **Present the design** — Show the user the design document or specific
   design decision that needs agreement.
2. **Grill session** — Let the user question, challenge, and stress-test the
   design. Use the `grill` skill if available, or ask pointed questions
   yourself to probe for weaknesses.
3. **Get explicit agreement** — Do not start coding until the user has
   confirmed the design is acceptable.
4. **Record decisions as ADRs** — Once agreed, write an Architecture Decision
   Record in `docs/adr/` capturing the decision, rationale, and alternatives
   considered.

## What "Grill" Means

The grill session should cover:
- Is the approach the simplest that could possibly work?
- What are the failure modes?
- What assumptions are we making about dependencies?
- What could go wrong that we haven't considered?
- Are we solving the right problem?

## When to Ask vs. When to Decide

**Ask the user:**
- Architecture-level decisions (tool choice, project structure)
- Feature scope (what's in/out of a release)
- Trade-offs between competing values (speed vs. safety, simplicity vs. power)
- Any decision that would be expensive to reverse

**Decide autonomously (but record as ADR):**
- Implementation details within an agreed design
- Standard patterns and conventions
- Minor API design choices
- Testing strategy

## Issue Workflow

1. Read the issue and its dependencies
2. If the issue has design implications, present the design first
3. Get user agreement
4. Implement
5. Record any new decisions as ADRs
6. Report completion with a demo
