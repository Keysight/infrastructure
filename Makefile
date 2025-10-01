MLCOMMONS_PACKAGE_DIR := ./keysight_chakra/mlcommons
INFRA_PACKAGE_DIR := ./keysight_chakra/infra

help:
	@awk -F ':|##' '/^[^\t].+:.*##/ { printf "\033[36mmake %-28s\033[0m -%s\n", $$1, $$NF }' $(MAKEFILE_LIST) | sort

env: ## install env requirements
	echo "installing python packages..." && \
	pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf build/* || true
	rm -rf dist/* || true
	rm -rf $(MLCOMMONS_PACKAGE_DIR)/*pb2* || true
	rm -rf $(INFRA_PACKAGE_DIR)/*pb2* || true

.PHONY: build
build: ## compile all .proto files and generate artifacts
	curl -L -o $(MLCOMMONS_PACKAGE_DIR)/et_def.proto https://raw.githubusercontent.com/mlcommons/chakra/main/schema/protobuf/et_def.proto
	sed -i 's/ChakraProtoMsg/keysight_chakra.mlcommons/g' $(MLCOMMONS_PACKAGE_DIR)/et_def.proto
	rm -rf $(MLCOMMONS_PACKAGE_DIR)/*pb2* || true
	rm -rf $(INFRA_PACKAGE_DIR)/*pb2* || true
	python3 -m grpc_tools.protoc \
		--proto_path=./ \
		--python_out=./ \
		--pyi_out=./ \
		--grpc_python_out=./ \
		$(INFRA_PACKAGE_DIR)/infra.proto \
		$(INFRA_PACKAGE_DIR)/annotate.proto \
		$(INFRA_PACKAGE_DIR)/service.proto \
		$(MLCOMMONS_PACKAGE_DIR)/et_def.proto 
	python3 -m pip uninstall -y keysight_chakra
	python3 setup.py bdist_wheel
	python3 -m pip install --no-cache .

.PHONY: test
test: build ## run sanity tests on the distribution
	python3 -m pytest -s tests


