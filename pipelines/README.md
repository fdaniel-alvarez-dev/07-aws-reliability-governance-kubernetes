# Pipelines

This folder documents how CI/CD and quality gates are structured in this repository.

CI goals:
- consistent formatting (Markdown, scripts, IaC)
- early detection of secrets
- fast feedback for contributors

Test policy:
- CI runs `TEST_MODE=demo` to avoid external dependencies.
- Production-mode tests are available locally via `make test-production` and are explicitly guarded.
