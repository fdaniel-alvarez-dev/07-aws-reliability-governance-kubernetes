# 07-aws-reliability-governance-kubernetes

A reference data platform blueprint with pragmatic governance: quality checks, lineage, access controls, and CI for data assets.

Focus: kubernetes


## The top pains this repo addresses
1) Designing a resilient, scalable cloud platform foundation—Kubernetes/container orchestration, networking, and standard patterns teams can reuse.
2) Replacing manual, risky changes with automated delivery—repeatable infrastructure, safe deployments, and drift-free environments (IaC + CI/CD + GitOps).
3) Building a data platform people trust—reliable pipelines, clear ownership, data quality checks, and governance that scales without slowing delivery.

## Quick demo (local)
```bash
make demo
make test
```

What you get:
- a tiny governed pipeline (CSV → JSONL or Parquet)
- strict, dependency-free schema checks
- deterministic lineage (`lineage.json`) with a content hash
- a basic “trust contract” (docs + tests + CI)

## Kubernetes (what is real in this repo)

Manifests under `k8s/` define a hardened Job + NetworkPolicy and are validated locally:

```bash
make k8s-validate
```

Build a local image and apply (demo):

```bash
docker build -t governed-pipeline:dev .
kubectl apply -k k8s/
```

## Test modes (demo vs production)

This repository supports exactly two test execution modes controlled by `TEST_MODE`:

- `demo`: runs local fixture checks only (no external calls)
- `production`: runs real integration checks when configured (S3 via AWS CLI) and explicitly acknowledged

Run production-mode tests (guarded):

```bash
PRODUCTION_TESTS_CONFIRM=1 S3_TEST_BUCKET=your-bucket AWS_REGION=us-east-1 make test-production
```

## Sponsorship and authorship

Sponsored by:
CloudForgeLabs  
https://cloudforgelabs.ainextstudios.com/  
support@ainextstudios.com

Built by:
Freddy D. Alvarez  
https://www.linkedin.com/in/freddy-daniel-alvarez/

For job opportunities, contact:  
it.freddy.alvarez@gmail.com

## License

Personal and other non-commercial use is free.

Commercial use requires paid permission. Contact `it.freddy.alvarez@gmail.com`.

Note: the included `LICENSE` is intentionally **not** an OSI-approved open-source license. It is a noncommercial license that aligns with the “personal use free, commercial use paid” model.
