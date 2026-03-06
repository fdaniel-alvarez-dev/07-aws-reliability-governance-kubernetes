# Repository governance and protection notes

This repository is designed to be safe-by-default and easy to contribute to, while being realistic about what GitHub can and cannot enforce.

## Forking restriction (platform limitation)

GitHub does **not** allow disabling forks for **user-owned** repositories via the GitHub REST API. The `allow_forking` setting can only be changed for **organization-owned** repositories.

Practical options if you must minimize forking:
- Transfer the repository to an organization and set `allow_forking=false`.
- Make the repository private.
- Use licensing + NOTICE to clearly restrict commercial use.

## Token hygiene

- Never commit tokens or credentials.
- Prefer GitHub secrets for CI.
- Use short-lived tokens where possible.

