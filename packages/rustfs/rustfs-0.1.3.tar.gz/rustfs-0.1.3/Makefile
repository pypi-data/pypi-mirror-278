.SILENT: help
.PHONY: help
help:
	echo Available recipes:
	cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN { FS = ":.*?## " } { cnt++; a[cnt] = $$1; b[cnt] = $$2; if (length($$1) > max) max = length($$1) } END { for (i = 1; i <= cnt; i++) printf "  $(shell tput setaf 6)%-*s$(shell tput setaf 0) %s\n", max, a[i], b[i] }'
	tput sgr0

.PHONY: build_and_push
build_and_push:  ## Build and push the image
	docker build --push --platform linux/amd64 -t ghcr.io/unionai-oss/flytekit-rustfs:latest -f benchmark/Dockerfile .


.PHONY: flyte_workflow
flyte_workflow: ## Register a flyte workflow and run it
	pyflyte run --remote benchmark/flyte_workflow.py wf


.PHONY: local_test
local_test:  ## Upload/download a file locally
	python benchmark/local_test.py

.PHONY: lint
lint: ## Run linter
	cargo fmt --all
	cargo clippy --all-targets --all-features -- -D warnings
	pre-commit run ruff --all-files || true
	pre-commit run ruff-format --all-files || true