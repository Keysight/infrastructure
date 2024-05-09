help:
	@awk -F ':|##' '/^[^\t].+:.*##/ { printf "\033[36mmake %-28s\033[0m -%s\n", $$1, $$NF }' $(MAKEFILE_LIST) | sort

env: ## install env requirements
	echo "installing python packages..." && \
	pip install -r requirements.txt

.PHONY: build
GENERATED_DIR := ./src/generated
build: ## compile all .proto files and generate artifacts
	curl -L -o ./protos/et_def.proto https://raw.githubusercontent.com/mlcommons/chakra/main/schema/protobuf/et_def.proto
	rm -rf $(GENERATED_DIR) || true
	mkdir -p $(GENERATED_DIR)
	python3 -m grpc_tools.protoc \
		--proto_path=./protos \
		--python_out=$(GENERATED_DIR) --pyi_out=$(GENERATED_DIR) \
		et_def.proto infra.proto
	python3 -m pip uninstall -y mlcommons-chakra
	python3 setup.py bdist_wheel
	python3 -m pip install --no-cache .

.PHONY: test
test: build ## run sanity tests on the distribution
	python3 -m pytest -s src/tests


