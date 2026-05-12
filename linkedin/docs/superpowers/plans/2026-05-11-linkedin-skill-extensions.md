# LinkedIn Skill Extensions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three focused LinkedIn writing skills for event promotion, carousel/document-post outlining, and comment/reply strategy, all reusing the existing `linkedin-writing` reference set where practical.

**Architecture:** Keep one shared foundation in `skills/linkedin-writing/` and add three narrow trigger skills beside it. Each extension should have a short `SKILL.md`, minimal `agents/openai.yaml`, and only new references when the guidance is genuinely distinct rather than a duplicate of existing hook, structure, style, or format material.

**Tech Stack:** Markdown skill packages, local skill metadata, shared reference files, manual validation with shell inspection.

---

## File Structure

- Existing: `skills/linkedin-writing/SKILL.md`
- Existing: `skills/linkedin-writing/references/platform.md`
- Existing: `skills/linkedin-writing/references/hooks.md`
- Existing: `skills/linkedin-writing/references/structure.md`
- Existing: `skills/linkedin-writing/references/style.md`
- Existing: `skills/linkedin-writing/references/formats.md`
- Existing: `skills/linkedin-writing/assets/templates.md`
- Create: `skills/linkedin-event-promo/SKILL.md`
- Create: `skills/linkedin-event-promo/agents/openai.yaml`
- Create: `skills/linkedin-event-promo/references/event-promos.md`
- Create: `skills/linkedin-carousel-outline/SKILL.md`
- Create: `skills/linkedin-carousel-outline/agents/openai.yaml`
- Create: `skills/linkedin-carousel-outline/references/carousel-structure.md`
- Create: `skills/linkedin-comment-strategy/SKILL.md`
- Create: `skills/linkedin-comment-strategy/agents/openai.yaml`
- Create: `skills/linkedin-comment-strategy/references/comment-patterns.md`
- Modify: `skills/linkedin-writing/references/formats.md`
- Modify: `skills/linkedin-writing/assets/templates.md`

### Task 1: Extend The Shared Format Guidance

**Files:**
- Modify: `skills/linkedin-writing/references/formats.md`
- Modify: `skills/linkedin-writing/assets/templates.md`

- [ ] **Step 1: Write the failing content checks**

Add these acceptance notes to the working scratchpad before editing:

```text
formats.md must mention when event promotion should stay a post versus become a document post.
templates.md must include a reusable event promotion template and a carousel/document-post outline template.
```

- [ ] **Step 2: Run a baseline read to verify the content is missing**

Run: `rg -n "event|carousel|document post outline|agenda" skills/linkedin-writing/references/formats.md skills/linkedin-writing/assets/templates.md`
Expected: partial or missing matches that confirm the new guidance is not yet fully present.

- [ ] **Step 3: Add minimal shared guidance**

Add to `skills/linkedin-writing/references/formats.md`:

```md
## Event Promotion Heuristic

Use a standard post when the event pitch is simple and the goal is quick registration or awareness.

Use a document post when attendees need agenda detail, speaker context, logistics, or a swipeable framework that justifies multiple frames.

## Carousel / Document Post Heuristic

Use a document post when the idea improves through sequencing, one frame per concept, or visual scanability.

Avoid turning plain text into a carousel unless each frame adds distinct value.
```

Add to `skills/linkedin-writing/assets/templates.md`:

```md
## Template 6: Event Promotion

- Hook around the attendee problem
- Why this event matters now
- What people will learn or experience
- Who should attend
- Clear registration CTA

## Template 7: Carousel / Document Post

- Cover promise
- Problem frame
- 3-7 insight or step frames
- Common mistake frame
- Closing takeaway
- CTA frame
```

- [ ] **Step 4: Run verification reads**

Run: `sed -n '1,260p' skills/linkedin-writing/references/formats.md`
Expected: the new event and carousel heuristics are present and read cleanly.

Run: `sed -n '1,260p' skills/linkedin-writing/assets/templates.md`
Expected: both new templates are present and non-duplicative.

- [ ] **Step 5: Commit**

```bash
git add skills/linkedin-writing/references/formats.md skills/linkedin-writing/assets/templates.md
git commit -m "feat: extend shared linkedin format guidance"
```

### Task 2: Add The Event Promotion Skill

**Files:**
- Create: `skills/linkedin-event-promo/SKILL.md`
- Create: `skills/linkedin-event-promo/agents/openai.yaml`
- Create: `skills/linkedin-event-promo/references/event-promos.md`

- [ ] **Step 1: Write the failing content checks**

Add these acceptance notes to the working scratchpad:

```text
The skill must trigger on launch posts, speaker announcements, last-call posts, and event recap promotions.
The skill must distinguish event relevance, attendee value, logistics, and CTA.
The skill must not duplicate the general linkedin-writing workflow in full.
```

- [ ] **Step 2: Verify the skill does not exist yet**

Run: `find skills/linkedin-event-promo -maxdepth 3 -type f`
Expected: no files found or a “No such file or directory” result.

- [ ] **Step 3: Create the skill entry file**

Create `skills/linkedin-event-promo/SKILL.md` with:

```md
---
name: linkedin-event-promo
description: Use when writing or rewriting LinkedIn posts that promote events, announce speakers, drive registrations, handle last-call reminders, or turn event details into clearer attendee-facing messaging.
---

# LinkedIn Event Promo

## Overview

Use this skill when the main job is getting the right people to care about an event.

Lead with attendee relevance, not organizer excitement.

## Workflow

1. Identify the event type, audience, and timing.
2. Define the attendee payoff.
3. Decide whether this should be a standard post or document post.
4. Build the draft around problem, outcome, proof, logistics, and CTA.
5. Check that the CTA matches the event stage.

## Rules

- Lead with why the event matters.
- Name who the event is for.
- Keep logistics secondary to value.
- Avoid generic “excited to announce” openings.
- Match urgency to reality.

## Load References

- Read [references/event-promos.md](references/event-promos.md).
- Read [../linkedin-writing/references/formats.md](../linkedin-writing/references/formats.md).
- Read [../linkedin-writing/references/hooks.md](../linkedin-writing/references/hooks.md) when the opening is weak.
```

- [ ] **Step 4: Create the event-specific reference**

Create `skills/linkedin-event-promo/references/event-promos.md` with:

```md
# Event Promos

## Core Event Angles

- attendee problem
- timely industry shift
- speaker credibility
- concrete outcome
- exclusivity or deadline, only if real

## Common Post Types

### Launch Post

- Why this event exists
- What attendees will get
- Who should attend
- Registration CTA

### Speaker Announcement

- What this speaker adds
- Why their perspective matters now
- Who benefits from attending

### Last-Call Post

- Real deadline
- Fast reminder of value
- Direct CTA

### Recap / Momentum Post

- What happened
- What people learned
- Why future attendees should care
```

- [ ] **Step 5: Create the agent metadata**

Create `skills/linkedin-event-promo/agents/openai.yaml` with:

```yaml
version: 1
display_name: LinkedIn Event Promo
short_description: Write event-focused LinkedIn posts that drive attention and registrations through attendee relevance.
default_prompt: Write or rewrite this LinkedIn event promotion so it is clearer, stronger, and more attendee-focused.
```

- [ ] **Step 6: Run verification reads**

Run: `find skills/linkedin-event-promo -maxdepth 3 -type f | sort`
Expected: exactly `SKILL.md`, `agents/openai.yaml`, and `references/event-promos.md`.

Run: `sed -n '1,240p' skills/linkedin-event-promo/SKILL.md`
Expected: short skill, clear trigger description, and correct cross-links.

- [ ] **Step 7: Commit**

```bash
git add skills/linkedin-event-promo
git commit -m "feat: add linkedin event promo skill"
```

### Task 3: Add The Carousel Outline Skill

**Files:**
- Create: `skills/linkedin-carousel-outline/SKILL.md`
- Create: `skills/linkedin-carousel-outline/agents/openai.yaml`
- Create: `skills/linkedin-carousel-outline/references/carousel-structure.md`

- [ ] **Step 1: Write the failing content checks**

Add these acceptance notes to the working scratchpad:

```text
The skill must help outline document posts and carousels frame-by-frame.
The skill must optimize for one idea per frame and a strong cover promise.
The skill must avoid pretending that all post ideas need slides.
```

- [ ] **Step 2: Verify the skill does not exist yet**

Run: `find skills/linkedin-carousel-outline -maxdepth 3 -type f`
Expected: no files found or a “No such file or directory” result.

- [ ] **Step 3: Create the skill entry file**

Create `skills/linkedin-carousel-outline/SKILL.md` with:

```md
---
name: linkedin-carousel-outline
description: Use when turning a LinkedIn idea into a document post or carousel outline, especially when deciding frame sequence, cover messaging, pacing, or whether the idea deserves slides at all.
---

# LinkedIn Carousel Outline

## Overview

Use this skill when the output should be a swipeable LinkedIn document post rather than a plain text update.

The job is sequencing.

## Workflow

1. Confirm the idea deserves multiple frames.
2. Define the cover promise.
3. Break the concept into distinct frames.
4. Ensure each frame adds one clear unit of value.
5. End with one takeaway and one CTA.

## Rules

- One idea per frame.
- The cover must promise a concrete payoff.
- Cut frames that repeat rather than advance.
- Prefer 5-9 strong frames over bloated decks.
- If the idea works better as text, say so.

## Load References

- Read [references/carousel-structure.md](references/carousel-structure.md).
- Read [../linkedin-writing/references/formats.md](../linkedin-writing/references/formats.md).
- Read [../linkedin-writing/assets/templates.md](../linkedin-writing/assets/templates.md).
```

- [ ] **Step 4: Create the carousel reference**

Create `skills/linkedin-carousel-outline/references/carousel-structure.md` with:

```md
# Carousel Structure

## Default Sequence

1. Cover promise
2. Problem or context
3. Insight or step 1
4. Insight or step 2
5. Insight or step 3
6. Common mistake or contrast
7. Summary takeaway
8. CTA

## Frame Rules

- each frame should stand on its own
- keep text scannable
- avoid burying the best insight after frame 5
- use progression, not repetition

## Good Use Cases

- frameworks
- checklists
- event agendas
- process breakdowns
- before/after thinking
```

- [ ] **Step 5: Create the agent metadata**

Create `skills/linkedin-carousel-outline/agents/openai.yaml` with:

```yaml
version: 1
display_name: LinkedIn Carousel Outline
short_description: Turn LinkedIn ideas into stronger document-post and carousel outlines with clear frame sequencing.
default_prompt: Outline this LinkedIn carousel or document post frame by frame and improve the sequence if needed.
```

- [ ] **Step 6: Run verification reads**

Run: `find skills/linkedin-carousel-outline -maxdepth 3 -type f | sort`
Expected: exactly `SKILL.md`, `agents/openai.yaml`, and `references/carousel-structure.md`.

Run: `sed -n '1,240p' skills/linkedin-carousel-outline/references/carousel-structure.md`
Expected: default sequence and frame rules are present.

- [ ] **Step 7: Commit**

```bash
git add skills/linkedin-carousel-outline
git commit -m "feat: add linkedin carousel outline skill"
```

### Task 4: Add The Comment Strategy Skill

**Files:**
- Create: `skills/linkedin-comment-strategy/SKILL.md`
- Create: `skills/linkedin-comment-strategy/agents/openai.yaml`
- Create: `skills/linkedin-comment-strategy/references/comment-patterns.md`

- [ ] **Step 1: Write the failing content checks**

Add these acceptance notes to the working scratchpad:

```text
The skill must cover replying to comments on the user's own posts and leaving comments on others' posts.
The skill must distinguish conversation-building from spammy visibility tactics.
The skill must give concrete comment patterns rather than generic “add value” advice.
```

- [ ] **Step 2: Verify the skill does not exist yet**

Run: `find skills/linkedin-comment-strategy -maxdepth 3 -type f`
Expected: no files found or a “No such file or directory” result.

- [ ] **Step 3: Create the skill entry file**

Create `skills/linkedin-comment-strategy/SKILL.md` with:

```md
---
name: linkedin-comment-strategy
description: Use when writing LinkedIn comments or replies, especially when the goal is to deepen conversation, add useful perspective, respond to engagement on a post, or avoid low-value visibility tactics.
---

# LinkedIn Comment Strategy

## Overview

Use this skill when the unit of writing is a comment, not a full post.

Optimize for contribution and conversation quality.

## Workflow

1. Identify whether this is an outbound comment or a reply on your own post.
2. Identify the goal: clarify, extend, appreciate, challenge, or move to DM.
3. Write a comment that adds one clear unit of value.
4. Keep it proportional to the thread.
5. Avoid sounding transactional.

## Rules

- Say something specific.
- Build on the post or comment you are answering.
- Use praise sparingly unless it adds context.
- Ask questions only when they are real.
- Do not fake intimacy or agreement.

## Load References

- Read [references/comment-patterns.md](references/comment-patterns.md).
- Read [../linkedin-writing/references/style.md](../linkedin-writing/references/style.md).
```

- [ ] **Step 4: Create the comment reference**

Create `skills/linkedin-comment-strategy/references/comment-patterns.md` with:

```md
# Comment Patterns

## Strong Comment Types

- add a concrete example
- extend the idea with a sharper implication
- respectfully challenge a premise
- summarize the key takeaway
- answer a question in the thread

## Reply Patterns On Your Own Posts

- acknowledge and expand
- clarify a point
- redirect to the main takeaway
- move a qualified lead toward DM only when appropriate

## Avoid

- “Great post”
- generic agreement
- forced controversy
- obvious networking bait
- comments that exist only to be seen
```

- [ ] **Step 5: Create the agent metadata**

Create `skills/linkedin-comment-strategy/agents/openai.yaml` with:

```yaml
version: 1
display_name: LinkedIn Comment Strategy
short_description: Write stronger LinkedIn comments and replies that add value instead of chasing empty visibility.
default_prompt: Improve this LinkedIn comment or reply so it adds clearer value and drives a better conversation.
```

- [ ] **Step 6: Run verification reads**

Run: `find skills/linkedin-comment-strategy -maxdepth 3 -type f | sort`
Expected: exactly `SKILL.md`, `agents/openai.yaml`, and `references/comment-patterns.md`.

Run: `sed -n '1,240p' skills/linkedin-comment-strategy/references/comment-patterns.md`
Expected: strong comment types, reply patterns, and avoid-list are present.

- [ ] **Step 7: Commit**

```bash
git add skills/linkedin-comment-strategy
git commit -m "feat: add linkedin comment strategy skill"
```

### Task 5: Validate Cross-Skill Consistency

**Files:**
- Modify if needed: `skills/linkedin-event-promo/SKILL.md`
- Modify if needed: `skills/linkedin-carousel-outline/SKILL.md`
- Modify if needed: `skills/linkedin-comment-strategy/SKILL.md`
- Modify if needed: `skills/linkedin-writing/references/formats.md`
- Modify if needed: `skills/linkedin-writing/assets/templates.md`

- [ ] **Step 1: Run a cross-link check**

Run: `rg -n "\.\./linkedin-writing|references/" skills/linkedin-event-promo skills/linkedin-carousel-outline skills/linkedin-comment-strategy`
Expected: all relative links point at real shared files.

- [ ] **Step 2: Run a trigger-description review**

Run: `sed -n '1,80p' skills/linkedin-event-promo/SKILL.md && sed -n '1,80p' skills/linkedin-carousel-outline/SKILL.md && sed -n '1,80p' skills/linkedin-comment-strategy/SKILL.md`
Expected: each description starts with “Use when” and describes trigger conditions rather than workflow steps.

- [ ] **Step 3: Run a package inventory**

Run: `find skills -maxdepth 3 -type f | sort`
Expected: the three new skills appear beside `linkedin-writing`, `linkedin-hooks`, and `linkedin-post-rewrite`.

- [ ] **Step 4: Fix any drift inline**

If any file duplicates shared guidance instead of linking to it, reduce the duplication and point back to the shared reference file.

- [ ] **Step 5: Commit**

```bash
git add skills
git commit -m "chore: validate linkedin skill package consistency"
```

## Self-Review

- Spec coverage:
  - `linkedin-event-promo` planned with event-specific workflow and reference file.
  - `linkedin-carousel-outline` planned with frame-sequencing logic and reference file.
  - `linkedin-comment-strategy` planned with comment/reply patterns and reference file.
  - Shared `formats` and `templates` updates planned so the new skills do not become isolated islands.
- Placeholder scan: no `TODO`, `TBD`, or unresolved file paths remain.
- Type consistency: all skill paths and metadata names match the planned directory structure.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-11-linkedin-skill-extensions.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
