# PolyLens Docs

This directory now acts as a lightweight navigation layer, not a second full product README.

For the full product overview, installation, usage, architecture, lens model, and extension guidance, start with [../README.md](../README.md).

## What Lives Here

- [../README.md](../README.md): canonical project documentation
- [polylens/README.md](polylens/README.md): canonical markdown artifact storage rules
- [polylens/reviews/](polylens/reviews/): saved executive review briefs
- [polylens/pre-fight/](polylens/pre-fight/): saved pre-fight reports
- [polylens/plans/](polylens/plans/): plans and proposals
- [polylens/memory/](polylens/memory/): generic markdown memos and working notes
- [polylens/notes/](polylens/notes/): supporting notes

## Reading Order

1. Read [../README.md](../README.md) for the full PolyLens model and runtime structure.
2. Read [polylens/README.md](polylens/README.md) for save-path and filename conventions.
3. Use the subdirectories under [polylens/](polylens/) for generated artifacts only.

## Notes

- The source docs remain at the repo root under `README.md`, `prompts/`, `engines/`, `lenses/`, and `orchestrators/`.
- The runtime bundle remains under `skills/shared/`; those mirrored files are intentional and should stay in sync with the source docs.
- Do not create loose markdown artifacts at the repo root when a `docs/polylens/` category fits.

## Contributing

Contributions are welcome in these areas:

- **New lenses** — Add perspectives we haven't covered (COO, CFO, and more)
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

MIT License

Copyright (c) 2026 PolyLens Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
