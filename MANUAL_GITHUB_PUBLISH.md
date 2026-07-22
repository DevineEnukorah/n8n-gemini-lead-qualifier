# Manual GitHub Publishing Guide

Target repository:

`DevineEnukorah/n8n-gemini-lead-qualifier`

Target branch:

`refactor/production-ready-lead-qualifier`

Do not upload these files directly to `main`.

## Recommended method: Git command line

### 1. Clone the repository

```powershell
git clone https://github.com/DevineEnukorah/n8n-gemini-lead-qualifier.git
cd n8n-gemini-lead-qualifier
```

### 2. Switch to the refactor branch

```powershell
git fetch origin
git checkout refactor/production-ready-lead-qualifier
git pull origin refactor/production-ready-lead-qualifier
```

### 3. Extract the production ZIP

Extract the contents of:

`n8n-gemini-lead-qualifier-production-v1.1.0.zip`

Copy everything inside the extracted `n8n-gemini-lead-qualifier-production-v1.1.0` folder into the repository root. Allow the new files to replace the old `README.md`, `system-prompt.md`, and `workflow.json`.

Do not copy the enclosing folder itself into the repository. The repository root should contain `workflow.json`, `README.md`, `VERSION`, and the other project files directly.

### 4. Run the tests locally

```powershell
python tests/run_all.py
```

The last line must be:

```text
ALL LOCAL TESTS PASSED.
```

### 5. Review the changes

```powershell
git status
git diff --stat
git diff -- workflow.json
```

Confirm that no credential, API key, or `.env` file is present.

### 6. Commit and push

```powershell
git add -A
git commit -m "Refactor lead qualifier for production readiness v1.1.0"
git push origin refactor/production-ready-lead-qualifier
```

### 7. Verify GitHub Actions

Open the repository's **Actions** tab and confirm that **Validate package** completes successfully.

Do not merge the branch into `main` yet. First import `workflow.json` into n8n and complete `tests/LIVE_TEST_PLAN.md`.

## GitHub website method

The command-line method is safer because it preserves nested folders and hidden files.

When using the GitHub website:

1. Select `refactor/production-ready-lead-qualifier`.
2. Extract the ZIP locally.
3. Use **Add file**, then **Upload files**.
4. Upload the contents of the extracted folder into the repository root.
5. Preserve `.github/workflows/validate.yml`, `schemas/`, `tests/`, and `marketplace/`.
6. Commit directly to the refactor branch.
7. Confirm `VERSION` displays `1.1.0`.
8. Confirm the Actions workflow passes.

## Expected root files

```text
.github/
marketplace/
schemas/
tests/
.gitignore
CHANGELOG.md
LICENSE
PRIVACY.md
README.md
SECURITY.md
TEST_REPORT.md
VERSION
system-prompt.md
workflow.json
```
