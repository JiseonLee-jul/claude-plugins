**[emojis exclusion]** Never use **emojis** — in text, comments, commits, or documentation.

## General

### Tidy First Approach

* Separate all changes into two distinct types:
  - STRUCTURAL CHANGES: Rearranging code without changing behavior (renaming, extracting methods, moving code)
  - BEHAVIORAL CHANGES: Adding or modifying actual functionality
* Never mix structural and behavioral changes in the same commit
* Always make structural changes first when both are needed
* Validate structural changes do not alter behavior by running tests before and after

### Code Quality

* Maintain high code quality throughout development
* Eliminate duplication ruthlessly
* Keep methods small and focused on a single responsibility
* Minimize state and side effects
* Use the simplest solution that could possibly work
* Make dependencies explicit
* Express intent clearly through naming and structure
* Name things with meaningful, predictable, and explicit but concise tones
  - When reading codes, variable names should align with what intermediate-level developers could expect from them.
  - The words in names should follow adjectives/descriptives and nouns in a meaningful order.
    - Example: `container_user_info` vs. `user_container_info` means completely different things.
      The former represents container-specific "user" information,
      while the latter represents user-specific "container" information.
  - Legacy stuffs should have distinguishable names
  - Be cautious when naming similar but different stuffs to avoid reader's confusion
* Avoid replicating legacy patterns when writing new codes
  - Stick to the user prompts about the new code patterns