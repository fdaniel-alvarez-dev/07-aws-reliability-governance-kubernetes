#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
K8S_DIR = REPO_ROOT / "k8s"


def main() -> int:
    if not K8S_DIR.exists():
        print("Missing k8s/ directory.")
        return 2

    yaml_files = sorted(p for p in K8S_DIR.rglob("*.yaml") if p.is_file())
    if not yaml_files:
        print("No YAML files found under k8s/.")
        return 2

    all_text = "\n".join(p.read_text(encoding="utf-8") for p in yaml_files)

    errors: list[str] = []
    if "kind: NetworkPolicy" not in all_text:
        errors.append("Missing a NetworkPolicy (basic deny-all or scoped policy expected).")
    if "kind: Job" not in all_text:
        errors.append("Missing a Job (pipeline execution workload is expected).")

    required_markers = [
        "runAsNonRoot: true",
        "allowPrivilegeEscalation: false",
        "readOnlyRootFilesystem: true",
    ]
    for marker in required_markers:
        if marker not in all_text:
            errors.append(f"Missing required hardening marker in manifests: {marker}")

    if errors:
        print("Kubernetes manifest validation failed:\n" + "\n".join(f"- {e}" for e in errors))
        return 1

    print("Kubernetes manifest validation OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

