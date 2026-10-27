# ADR-0005: Browser backend — wigolo primary, aside optional

**Status:** Accepted
**Date:** 2026-10-27

## Context

Users may have multiple browser tools installed (wigolo, aside browser, etc.).
hawk needs to decide which to use for browser-based operations (JS-rendered
pages, authenticated sessions, browser actions).

aside browser requires a GUI (desktop browser) and cannot be installed on
headless Linux servers. wigolo uses headless Chrome via CDP and works in
both desktop and server environments.

## Decision

wigolo is the primary browser backend for hawk. aside browser may be used as
an optional enhancement on desktop environments where the user has it
installed and wants to leverage their existing login sessions.

## Rationale

- wigolo works everywhere (headless and desktop)
- wigolo is already a required dependency of hawk
- Adding aside as an optional fallback increases complexity
- The user's primary use case (Linux servers) requires headless operation

## Consequences

- hawk requires wigolo to be installed (hard dependency)
- aside browser integration is deferred to a future enhancement
- Users on desktop who want to use their logged-in browser sessions must
  use aside directly, not through hawk (for now)
