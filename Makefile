help:
	@awk -F ':|##' '/^[^\t].+:.*##/ { printf "\033[36mmake %-28s\033[0m -%s\n", $$1, $$NF }' $(MAKEFILE_LIST) | sort

env: ## install env requirements
	echo "installing python packages..." && \
	pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf build/* || true
	rm -rf dist/* || true

.PHONY: build
PROTO_PACKAGE_DIR := ./keysight_chakra/protobuf
build: ## compile all .proto files and generate artifacts
	curl -L -o ./keysight_chakra/protobuf/et_def.proto https://raw.githubusercontent.com/mlcommons/chakra/main/schema/protobuf/et_def.proto
	sed -i 's/ChakraProtoMsg/keysight_chakra.protobuf/g' ./keysight_chakra/protobuf/et_def.proto
	rm -rf $(PROTO_PACKAGE_DIR)/*pb2* || true
	python3 -m grpc_tools.protoc \
		--proto_path=./ \
		--python_out=./ \
		--pyi_out=./ \
		--grpc_python_out=./ \
		$(PROTO_PACKAGE_DIR)/infra.proto \
		$(PROTO_PACKAGE_DIR)/annotate.proto \
		$(PROTO_PACKAGE_DIR)/service.proto \
		$(PROTO_PACKAGE_DIR)/et_def.proto 
	python3 -m pip uninstall -y keysight-chakra
	python3 setup.py bdist_wheel
	python3 -m pip install --no-cache .

.PHONY: test
test: build ## run sanity tests on the distribution
	python3 -m pytest -s keysight_chakra/tests


