from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class TestDemoPipeline(unittest.TestCase):
    def test_pipeline_writes_outputs_and_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "processed"
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pipelines.pipeline",
                    "--raw",
                    "data/raw/events.csv",
                    "--out-dir",
                    str(out_dir),
                    "--format",
                    "jsonl",
                ],
                cwd=str(REPO_ROOT),
                check=True,
            )

            out_jsonl = out_dir / "events.jsonl"
            lineage = out_dir / "lineage.json"
            self.assertTrue(out_jsonl.exists())
            self.assertTrue(lineage.exists())

            obj = json.loads(lineage.read_text(encoding="utf-8"))
            self.assertEqual(obj["row_count"], 4)
            self.assertIn("content_sha256", obj)

    def test_k8s_validation_runs(self) -> None:
        subprocess.run([sys.executable, "scripts/k8s_validate.py"], cwd=str(REPO_ROOT), check=True)

    def test_problem_statement_present(self) -> None:
        p = (REPO_ROOT / "07-problem-statement.txt").read_text(encoding="utf-8")
        self.assertIn("Top 3 pain points", p)
