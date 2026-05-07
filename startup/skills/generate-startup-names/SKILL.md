---
name: generate-startup-names
description: Generate startup, product, app, and service names from a brief. Use when the user asks to name a startup, generate brand names, suggest product names, or create naming options for a new company, app, product, or service. Do not use this skill for domain availability checks, trademark validation, or legal clearance.
---

# Generate Startup Names

## Overview

Turn a rough startup brief into a structured set of naming options. Generate names across multiple patterns, explain why each works, and finish with a concise shortlist.

## Workflow

1. Extract the brief.
2. Infer only the minimum missing context.
3. Generate names across several naming patterns.
4. Explain each candidate in one short line.
5. Finish with a shortlist of the strongest options.

## Extract The Brief

Identify:

- what is being named
- who it serves
- what problem it solves
- the tone or brand personality
- any explicit constraints such as length, language, or style

If the brief is incomplete, make conservative assumptions and state them briefly. Do not stop the flow unless a missing detail would materially change the naming direction.

## Generate Naming Patterns

Generate names across at least four of these patterns:

- descriptive
- invented or brandable
- compound
- metaphorical or symbolic
- modern or technical
- short and punchy

Avoid producing a flat list with the same rhythm or structure. Vary syllable count, sound, and construction.

## Naming Heuristics

Prefer names that are:

- easy to pronounce
- easy to remember
- distinct enough to feel ownable
- aligned with the product category without being generic
- short enough to be brand-friendly

Avoid names that are:

- hard to spell after hearing once
- overloaded with trendy suffixes unless the brief clearly supports them
- too similar to obvious incumbents
- awkward to say aloud
- dependent on weak puns

## Output Format

Return:

1. A brief restatement of the naming direction.
2. `20-30` candidate names grouped by pattern.
3. One-line rationale for each name.
4. A shortlist of `5-10` strongest options with a short reason each.

Keep explanations compact. The names are the main deliverable.

## Boundaries

Do not claim that domains are available.
Do not claim that trademarks are clear.
Do not present legal or domain-check work unless the user separately asks for it.

## Example Triggers

- "Name my startup."
- "Generate product names for this app."
- "Suggest brand names for my SaaS."
- "I need naming ideas for a new service."
- "Create startup name options from this brief."
