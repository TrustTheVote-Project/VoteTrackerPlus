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
DOC_DIR     := docs
SRC_DIR     := src/vtp
TEST_DIR    := test
BUILD_DIR   := _tools/build
BUILD_FILES := pyproject.toml poetry.lock setup.cfg 

INTERACTIVE := $(shell test -t 0 && echo 1)
ifdef INTERACTIVE
    RED	:= \033[0;31m
    END	:= \033[0m
else
    RED	:=
    END	:=
endif

# Let there be no default target
.PHONY: default
default:
	@echo "${RED}There is no default make target.${END}  Specify one of:"
	@echo "poetry-build            - performs a poetry local install"
	@echo "setuptools-build        - performs a setuptools local install"
	@echo "setuptools-legacy-build - performs a legacy setuptools local install"
	@echo "pylint                  - runs pylint"
	@echo "pytest                  - runs pytest"
	@echo "etags                   - constructs an emacs tags table"
	@echo ""
	@echo "See ${BUILD_DIR}/README.md for more details and info"

# Create the python environment and requirement files
.PHONY: conda-export
conda-export:
	conda env export --from-history > environment.yml
	pip freeze > requirements.txt

# Build with poetry
.PHONY: poetry-build
poetry-build:
	rm -f ${BUILD_FILES}
	ln -s ${BUILD_DIR}/poetry_pyproject.toml pyproject.toml
	ln -s ${BUILD_DIR}/poetry_poetry.lock poetry.lock
	poetry shell && poetry install

# Build with setuptools
.PHONY: setuptools-build
setuptools-build:
	rm -f ${BUILD_FILES}
	ln -s ${BUILD_DIR}/setuptools_pyproject.toml pyproject.toml
	python -m venv .venv
	source .venv/bin/activate && pip install --editable .

.PHONY: setuptools-legacy-build
setuptools-legacy-build:
	rm -f ${BUILD_FILES}
	ln -s ${BUILD_DIR}/setuptools_pyproject.toml pyproject.toml
	ln -s ${BUILD_DIR}/setuptools_legacy_setup.cfg setup.cfg
	python -m venv .venv
	source .venv/bin/activate && pip install --editable .

# Run pylint
.PHONY: pylint
pylint: requirements.txt
	@echo "${RED}NOTE - isort and black disagree on 3 files${END} - let black win"
	isort ${SRC_DIR} ${TEST_DIR}
	black ${SRC_DIR} ${TEST_DIR}
	pylint --recursive y ${SRC_DIR} ${TEST_DIR}

# Run tests
.PHONY: pytest
pytest:
	pytest ${TEST_DIR}

# emacs tags
ETAG_SRCS := $(shell find * -type f -name '*.py' -o -name '*.md' | grep -v defunct)
.PHONY: etags
etags: ${ETAG_SRCS}
	etags ${ETAG_SRCS}

# Generate a requirements.txt for dependabot (ignoring the symlinks)
requirements.txt: ${BUILD_DIR}/poetry_pyproject.toml ${BUILD_DIR}/poetry_poetry.lock
	poetry export --dev -f requirements.txt --output requirements.txt
