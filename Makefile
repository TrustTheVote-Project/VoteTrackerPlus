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
	pylint bin/*.py

# Run tests
.PHONY: pytest
pytest:
	pytest
