# Build and upload PyPI package using Twine

PACKAGE_NAME = test_panda_pypi

.PHONY: build
build:
	python -m build

.PHONY: upload
upload:
	twine upload --repository testpypi dist/*

.PHONY: clean
clean:
	rm -rf dist build

.PHONY: all
all: clean build upload