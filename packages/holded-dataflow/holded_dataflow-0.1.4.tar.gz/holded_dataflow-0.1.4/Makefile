all: lib

.PHONY: lib
lib:
	-@docker run --rm -v $(shell pwd):/io ghcr.io/pyo3/maturin build --release -i python3.11
