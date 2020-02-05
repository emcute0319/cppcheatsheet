REQUIREMENT = requirements.txt

VER  = $(word 2, $(shell python --version 2>&1))
SRC  = app.py
PY36 = $(shell expr $(VER) \>= 3.6)

.PHONY: build deps
build: html

%:
	cd docs && make $@

deps:
	pip install -r requirements.txt
ifeq ($(PY36), 1)
	pip install black==19.10b0
endif
