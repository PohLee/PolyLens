# PolyLens Docs

This directory now acts as a lightweight navigation layer, not a second full product README.

For the full product overview, installation, usage, architecture, lens model, and extension guidance, start with [../Readme.md](../Readme.md).

## What Lives Here

- [../Readme.md](../Readme.md): canonical project documentation
- [evaluation.md](evaluation.md): deterministic checks versus real model behavior evaluation
- [project-memory-model.md](project-memory-model.md): project-specific memory schema for durable context, preferences, and decision history
- [polylens/README.md](polylens/README.md): canonical markdown artifact storage rules
- [polylens/reviews/](polylens/reviews/): saved executive review briefs
- [polylens/pre-fight/](polylens/pre-fight/): saved pre-fight reports
- [polylens/plans/](polylens/plans/): plans and proposals
- [polylens/memory/](polylens/memory/): generic markdown memos and working notes
- [polylens/notes/](polylens/notes/): supporting notes

## Reading Order

1. Read [../Readme.md](../Readme.md) for the full PolyLens model and runtime structure.
2. Read [project-memory-model.md](project-memory-model.md) for project-specific memory classes and update rules.
3. Read [polylens/README.md](polylens/README.md) for save-path and filename conventions.
4. Use the subdirectories under [polylens/](polylens/) for generated artifacts only.

## Notes

- The source docs remain at the repo root under `README.md`, `prompts/`, `engines/`, `lenses/`, and `orchestrators/`.
- The runtime bundle remains under `skills/shared/`; those mirrored files are intentional and should stay in sync with the source docs.
- Do not create loose markdown artifacts at the repo root when a `docs/polylens/` category fits.
- Project-scoped memory should be split into context, preferences, and decision history rather than mixed into a single undifferentiated memo.

## Contributing

Contributions are welcome in these areas:

- **Lenses** — Improve existing perspectives or add a clearly distinct decision owner
- **Improved frameworks** — Better analytical frameworks for lenses to use
- **Conflict resolution models** — New strategies for resolving disagreements
- **Engine improvements** — Better collision detection or synthesis logic
- **Documentation** — Clearer examples, better explanations

To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test by invoking the skill in OpenCode
5. Submit a pull request

---

## License

GNU GPL v3.0 or later, as stated in the root project documentation. See [LICENSE](../LICENSE)
for the authoritative license text; this navigation page does not define a separate license.
