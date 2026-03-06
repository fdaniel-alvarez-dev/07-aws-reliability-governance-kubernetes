.PHONY: setup demo demo-rich test test-demo test-production k8s-validate clean

# Optional rich dependencies (parquet + heavier validation). Not required for demo tests.
setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

demo:
	python3 -m pipelines.pipeline --format jsonl

demo-rich:
	. .venv/bin/activate && python -m pipelines.pipeline --format parquet

test: test-demo

test-demo:
	@TEST_MODE=demo python3 tests/run_tests.py

test-production:
	@TEST_MODE=production python3 tests/run_tests.py

k8s-validate:
	@python3 scripts/k8s_validate.py

clean:
	rm -rf .venv data/processed
