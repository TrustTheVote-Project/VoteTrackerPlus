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
	pylint -d duplicate-code bin

# Run tests
.PHONY: pytest
pytest:
	pytest

# emacs tags
ETAG_SRCS := $(shell find bin -type file -name '*.py')
TAGS: ${ETAG_SRCS}
	etags ${ETAG_SRCS}
