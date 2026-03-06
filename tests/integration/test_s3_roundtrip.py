from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _run(cmd: list[str], *, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )


class TestS3RoundTrip(unittest.TestCase):
    def test_upload_and_download_outputs(self) -> None:
        bucket = os.environ["S3_TEST_BUCKET"]
        prefix = os.environ.get("S3_TEST_PREFIX", "governed-pipeline-test")

        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "processed"
            _run(
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
                ]
            )

            local_lineage = out_dir / "lineage.json"
            local_events = out_dir / "events.jsonl"
            self.assertTrue(local_lineage.exists())
            self.assertTrue(local_events.exists())

            s3_base = f"s3://{bucket}/{prefix}/"
            _run(["aws", "s3", "cp", str(local_events), s3_base])
            _run(["aws", "s3", "cp", str(local_lineage), s3_base])

            dl_dir = Path(td) / "downloaded"
            dl_dir.mkdir(parents=True, exist_ok=True)
            _run(["aws", "s3", "cp", f"{s3_base}events.jsonl", str(dl_dir / "events.jsonl")])
            _run(["aws", "s3", "cp", f"{s3_base}lineage.json", str(dl_dir / "lineage.json")])

            self.assertEqual((dl_dir / "events.jsonl").read_text(encoding="utf-8"), local_events.read_text(encoding="utf-8"))
            self.assertEqual((dl_dir / "lineage.json").read_text(encoding="utf-8"), local_lineage.read_text(encoding="utf-8"))
