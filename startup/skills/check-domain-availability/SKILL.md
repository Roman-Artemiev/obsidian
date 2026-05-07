---
name: check-domain-availability
description: Check startup, product, or brand name domain availability. Use when the user wants to validate candidate names, prioritize globally useful domains, and treat a free .cz domain as a strong bonus rather than a strict requirement. Do not use this skill for trademark clearance or legal advice.
---

# Check Domain Availability

## Overview

Validate a shortlist of names against priority global TLDs and treat a free `.cz` domain as a strong bonus.

Default global priority:

1. `.com`
2. `.io`
3. `.ai`
4. `.app`
5. `.dev`

Keep a candidate when:

- at least one priority global domain is free

Upgrade a candidate when:

- the matching `.cz` domain is also free

## Workflow

1. Gather candidate names from the user or from a naming shortlist.
2. Normalize names to lowercase ASCII slugs without spaces.
3. Check `.cz` plus the priority global TLDs.
4. Prefer the strongest global result by the priority order above.
5. Keep candidates with a free priority global TLD even if `.cz` is taken.
6. Rank candidates with free `.cz` above otherwise equal options.
7. If live verification fails or is blocked, state that clearly and mark the result as `unknown` or `manual verification needed`.

## Tooling

Use `scripts/check_domains.py` for live checks when network access is available.

Example:

```bash
python3 startup/skills/check-domain-availability/scripts/check_domains.py \
  --names "lumo,verigo,fluxora"
```

Override the global priority when needed:

```bash
python3 startup/skills/check-domain-availability/scripts/check_domains.py \
  --names "lumo,verigo,fluxora" \
  --global-tlds "com,io,ai,app,dev"
```

## Output Format

Return:

1. One short sentence describing the filter used.
2. A compact table with:
   - `name`
   - `best global`
   - `.cz`
   - `status`
   - `notes`
3. A shortlist of recommended names ordered by domain quality, with free `.cz` treated as a bonus.

Status values:

- `bonus` when a priority global domain is free and `.cz` is also free
- `keep` when a priority global domain is free but `.cz` is taken
- `reject` when all priority global domains are taken
- `unknown` when live verification did not produce a reliable answer

## Boundaries

Do not claim trademark clearance.
Do not claim legal exclusivity.
Do not hide uncertainty when WHOIS or network checks fail.
Prefer explicit wording such as `appears free`, `taken`, or `manual verification needed`.
