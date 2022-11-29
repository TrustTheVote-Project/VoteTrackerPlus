# Ancient Makefile implicit rule disabler
(%): %
%:: %,v
%:: RCS/%,v
%:: s.%
%:: SCCS/s.%
%.out: %
%.c: %.w %.ch
%.tex: %.w %.ch
%.mk:

# Variables
DOC_DIR  := docs
SRC_DIR  := src/vtp
TEST_DIR := test

TOOLS_BUILD_DIR := _tools/build

# Setup of pyproject.toml for builds

pyproject: pyproject_poetry

# Set up to build with Poetry
pyproject_poetry:
	@ln -s $(TOOLS_BUILD_DIR)/poetry_pyproject.toml pyproject.toml
	@ln -s $(TOOLS_BUILD_DIR)/poetry_poetry.lock poetry.lock

# Set up to build with modern Setuptools
pyproject_setuptools:
	@ln -s _tools/build/setuptools_pyproject.toml pyproject.toml

# Set up to build with legacy Setuptools
pyproject_setuptools_legacy:
	@ln -s _tools/build/setuptools_legacy_pyproject.toml pyproject.toml
	@ln -s _tools/build/setuptools_legacy_setup.cfg setup.cfg

# Create the python environment files
.PHONY: export
export:
	conda env export --from-history > environment.yml
	pip freeze > requirements.txt

# Run pylint
.PHONY: pylint
pylint:
# As there are multiple commands with the same boilerplate scaffolding, when
# pylinting from the top ignore R0801
	pylint --recursive y ${SRC_DIR}

# Run tests
.PHONY: pytest
pytest:
	pytest ${TEST_DIR}

# emacs tags
ETAG_SRCS := $(shell find * -type f -name '*.py' -o -name '*.md' | grep -v defunct)
.PHONY: etags
etags: ${ETAG_SRCS}
	etags ${ETAG_SRCS}
