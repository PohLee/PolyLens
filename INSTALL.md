# PolyLens Install Instructions For Agents

Use these instructions when a user asks you to install PolyLens.

## Goal

Install PolyLens so the target agent can discover these three sibling skill directories:

- `polylens/`
- `polylens-lens-review/`
- `shared/`

Do **not** symlink the whole repository root. Do **not** expose only one of the public skill directories without `shared/`.

## Repository Source

Use this repository as the source:

- GitHub: `https://github.com/PohLee/PolyLens`
- Raw instructions: `https://raw.githubusercontent.com/PohLee/PolyLens/main/INSTALL.md`

If the repository is not already present locally, clone it first.

```bash
git clone https://github.com/PohLee/PolyLens.git polylens
cd polylens
```

If the repository is already open in the current workspace, use that local copy instead of cloning again.

## Detect The Target Environment

Detect which agent the user wants PolyLens installed into.

Known personal skill directories:

- Claude Code: `~/.claude/skills`
- OpenCode: `~/.config/opencode/skills`
- Codex: `~/.codex/skills`
- RooCode: `~/.roo/skills`

For GitHub Copilot in VS Code, prefer workspace installation instead of a user-global symlink unless the user explicitly asks for a global install.

## Install Rules

### Rule 0: OpenCode Uses A Dedicated Installer

OpenCode does not reliably resolve PolyLens runtime reads through sibling traversal such as `../shared/...`. A direct install of `skills/polylens`, `skills/polylens-lens-review`, and `skills/shared` into `~/.config/opencode/skills` can leave the public skills unable to find their orchestrators.

If the target agent is OpenCode, do this instead:

```bash
bash tools/install_opencode.sh
```

Optional explicit target path:

```bash
bash tools/install_opencode.sh ~/.config/opencode/skills
```

The installer builds `dist/opencode-polylens/` and installs self-contained `polylens/` and `polylens-lens-review/` skill directories with nested `shared/` runtime assets, so OpenCode never needs to traverse outside the active skill directory.

### Rule 0.5: Common Agent Installers

PolyLens also ships explicit installers for the common sibling-layout agents:

- Claude Code: `bash tools/install_claude_code.sh`
- Codex: `bash tools/install_codex.sh`
- GitHub Copilot workspace install: `bash tools/install_copilot_workspace.sh /path/to/workspace`

These scripts build `dist/standard-polylens/` and install the standard sibling bundle:

- `polylens/`
- `polylens-lens-review/`
- `shared/`

If you need a custom target path, pass it as the first argument:

```bash
bash tools/install_claude_code.sh ~/.claude/skills
bash tools/install_codex.sh ~/.codex/skills
bash tools/install_copilot_workspace.sh /path/to/workspace
```

### Rule 1: Preserve Sibling Layout

For Claude Code, Codex, RooCode, Copilot workspace installs, and other agents that correctly resolve sibling-relative paths, the final target skills location must contain these sibling directories:

The final target skills location must contain these sibling directories:

- `<skills-root>/polylens`
- `<skills-root>/polylens-lens-review`
- `<skills-root>/shared`

The public skills rely on sibling-relative runtime paths such as `../shared/prompts/...`.

### Rule 2: Prefer Symlinks Or Junctions

When possible, create symlinks or junctions from the local repository's `skills/` subdirectories into the target skills location.

macOS / Linux pattern:

```bash
mkdir -p <skills-root>
ln -s "<repo>/skills/polylens" <skills-root>/polylens
ln -s "<repo>/skills/polylens-lens-review" <skills-root>/polylens-lens-review
ln -s "<repo>/skills/shared" <skills-root>/shared
```

Windows PowerShell pattern:

```powershell
New-Item -ItemType Directory -Force -Path "<skills-root>" | Out-Null
New-Item -ItemType Junction -Path "<skills-root>\polylens" -Target "<repo>\skills\polylens" | Out-Null
New-Item -ItemType Junction -Path "<skills-root>\polylens-lens-review" -Target "<repo>\skills\polylens-lens-review" | Out-Null
New-Item -ItemType Junction -Path "<skills-root>\shared" -Target "<repo>\skills\shared" | Out-Null
```

If symlinks are blocked, copy the three directories instead.

Do not use this direct-sibling install method for OpenCode. Use `bash tools/install_opencode.sh` instead.

If you want a deterministic copied bundle instead of manual symlinks for Claude Code, Codex, RooCode, or Copilot workspace installs, prefer the installer scripts above.

### Rule 3: Copilot Workspace Install

For GitHub Copilot in VS Code, use one of these approaches:

1. Run `bash tools/install_copilot_workspace.sh /path/to/workspace` to copy the bundle into `.github/skills/`.
2. Or add `./skills` to the workspace `chat.skillsLocations` setting.
3. Or place the three sibling directories into `.github/skills/` or `.claude/skills/` inside the target workspace.

Do not treat the whole repository root as a skills directory.

## Verification

After installation:

1. For OpenCode installs, confirm the target location contains `polylens/shared/` and `polylens-lens-review/shared/`.
2. For other agents, confirm the target location contains `polylens`, `polylens-lens-review`, and `shared` as siblings.
3. Confirm the public skills can resolve their runtime markdown dependencies.
4. Ask the agent or user-facing environment what skills are available, if that environment supports it.

## Suggested Completion Message

Report:

- which repo copy was used
- which agent skills location was targeted
- whether symlinks/junctions or copies were created
- how verification was performed