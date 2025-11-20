# Repository Guidelines

## Project Structure & Module Organization
- `summarize.py` converts `prompts.yaml` (and timestamped YAML snapshots) into the rendered `index.html` chat history; keep prompts concise and prefixed with `Q`/`A` tokens so the parser stays reliable.
- Static assets (`logo.png`, `microphone.png`) live at the repo root and are referenced by the generated HTML; replace them in place to update the UI.
- `chatgpt_client.py` contains the direct OpenAI integration for live querying, while `justfile` and `requirements.txt` define the tooling surface; the `venv-hackathon-25-11` directory is a local virtualenv and should not be committed elsewhere.

## Build, Test, and Development Commands
- `python -m venv venv-hackathon-25-11 && source venv-hackathon-25-11/bin/activate` to create/enter the local environment.
- `pip install -r requirements.txt` installs OpenAI, PyYAML, and lint dependencies.
- `just serve` (default) regenerates `index.html` and starts `python -m http.server 8000` for local preview; `just restart` runs the same flow in the background.
- `just build` only regenerates the HTML, while `just rebuild`/`just refresh` wrap regeneration plus a clean server restart and browser open.
- `just stop` halts lingering `http.server` processes so ports stay clean.

## Coding Style & Naming Conventions
- Python modules follow standard PEP 8: 4-space indentation, snake_case functions, and docstrings for helpers like `extract_qa_messages`.
- Keep YAML strictly two-space indented with descriptive keys inside the top-level `prompts` array; run `yamllint prompts.yaml` before committing.
- Generated HTML should remain formatted by `summarize.py`; avoid hand-editing `index.html` so diffs stay scriptable.

## Testing Guidelines
- No automated test suite yet; validate changes by running `just build` and manually reviewing the refreshed UI in the browser.
- When adjusting YAML parsing, add temporary prompts that cover each branch (e.g., `Q2:` variant labels) to confirm rendering, then remove any fixtures.
- Lint YAML with `yamllint` and ensure `summarize.py` exits without tracebacks to maintain CI-readiness if automation is added later.

## Commit & Pull Request Guidelines
- Current history (`first commit`) uses short, imperative summaries; continue that convention (`add prompt parser guard`, `update logo asset`).
- Squash unrelated work before opening a PR, link any task IDs in the body, include before/after screenshots for UX changes, and describe how you validated the output (`just serve`, manual browser check, etc.).
- If a change introduces configuration needs (e.g., OpenAI keys via `.env`), document them in the PR description and update repository docs accordingly.

## Security & Configuration Tips
- Load sensitive settings (OpenAI API keys, environment-specific URLs) through `.env` consumed by `python-dotenv`; never hardcode credentials inside scripts or checked-in YAML.
- When sharing prompt files externally, scrub proprietary content and rotate API keys if you needed to log terminal output during debugging.
