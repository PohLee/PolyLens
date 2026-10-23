---
{
  "reasoning": {
    "depth": "standard",
    "min_lenses": 2,
    "max_lenses": 4,
    "constraints": [],
    "output": {"format": "full", "include_sections": ["all"], "custom_template": null}
  }
}
---

## Reasoning Controls

Use JSON frontmatter. Invalid keys/types fail rather than reverting silently.

- `surface`: minimal research; respect any user prohibition on tools.
- `standard`: normal review.
- `deep`: additional research only when permitted and materially useful.
- `constraints`: nonempty strings all lenses must respect.
- Lens range must satisfy `2 <= min_lenses <= max_lenses <= 4`.
- Output `format`: `full`, `concise`, or `dashboard-only`.
- `include_sections`: list of section labels; `all` is the default.
- `custom_template`: optional template path for the host agent, relative to this file.

Presentation preferences never suppress blocking decisions, dissent, or material unknowns.
Only `full` output is covered by the standard brief format validator; concise/custom reports
need their own format contract and must not claim to have passed that validator.
