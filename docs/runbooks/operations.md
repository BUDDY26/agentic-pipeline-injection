# Operations Runbook

**Project:** {{PROJECT_NAME}}
**Last updated:** {{LAST_UPDATED}}

> Update this runbook whenever setup steps, commands, or environment variables change.

---

## Prerequisites

- {{PREREQ_1}}
- {{PREREQ_2}}

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/{{GITHUB_USERNAME}}/{{REPO_NAME}}.git
cd {{REPO_NAME}}
```

### 2. Install dependencies

```bash
{{INSTALL_COMMAND}}
```

### 3. Configure environment

```bash
cp .env.example .env
# Open .env and fill in real values before proceeding
```

### 4. Run the application

```bash
{{RUN_COMMAND}}
```

---

## Running Tests

```bash
{{TEST_COMMAND}}
```

---

## Linting and Formatting

```bash
{{LINT_COMMAND}}
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
2. Confirm dependencies are installed: `{{INSTALL_COMMAND}}`
3. Check the exact test command: `{{TEST_COMMAND}}`

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
