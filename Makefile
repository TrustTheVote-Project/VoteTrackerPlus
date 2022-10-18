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
SRC_DIR := src/vtp

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
	pytest ${SRC_DIR}

# emacs tags
ETAG_SRCS := $(shell find ${SRC_DIR} -type file -name '*.py')
.PHONY: etags
etags: ${ETAG_SRCS}
	etags ${ETAG_SRCS}
