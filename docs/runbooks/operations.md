# Operations Runbook

**Project:** agentic-pipeline-injection
**Last updated:** 2026-03-27

> Update this runbook whenever setup steps, commands, or environment variables change.

---

## Prerequisites

- — list prerequisites here
- — list prerequisites here

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/BUDDY26/agentic-pipeline-injection.git
cd agentic-pipeline-injection
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Open .env and fill in real values before proceeding
```

### 4. Run the application

```bash
python src/main.py
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Linting and Formatting

```bash
ruff check src/ {{LINT_COMMAND}}{{LINT_COMMAND}} black src/
```

---

## Structure Validation

```bash
bash scripts/validate-structure.sh
```

---

## Environment Variables

See `.env.example` for the full list of required variables.

| Variable | Description | Required |
|----------|-------------|----------|
| *(fill in from `.env.example`)* | | |

---

## Troubleshooting

### Tests fail on first run

1. Confirm all variables in `.env` are set correctly
2. Confirm dependencies are installed: `pip install -r requirements.txt`
3. Check the exact test command: `pytest tests/ -v`

### Structure validation fails

Run `bash scripts/validate-structure.sh` to see a categorized report.
Common causes: missing required files, unfilled `{{PLACEHOLDER}}` tokens.

### CI is failing

Check the Actions tab on GitHub. Review the pipeline jobs defined in `.github/workflows/ci.yml`.

- Lint or test failures indicate source code issues
- validate-structure failures indicate missing required files

---

## Deployment

*(Fill in deployment steps here.)*
