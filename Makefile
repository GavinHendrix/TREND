VENV := venv
PYTHON := python3.12
APP_NAME := TREND
SRC := run.py
VERSION := 0.5.0

all: check-python install build

check-python:
	@echo "-> Checking for Python version $(PYTHON)"
	@if ! command -v $(PYTHON) >/dev/null 2>&1; then \
		echo "Error: $(PYTHON) is not installed. Please install Python $(PYTHON) to continue."; \
		echo "	MacOS: brew install $(PYTHON)"; \
		echo "	Windows: https://www.python.org/downloads/"; \
		echo "	Linux: sudo apt install $(PYTHON) $(PYTHON)-venv $(PYTHON)-dev"; \
		exit 1; \
	fi

$(VENV)/bin/activate: requirements.txt
	@echo "-> Creating Virtual Environment"
	$(PYTHON) -m venv $(VENV)

install: $(VENV)/bin/activate
	@echo "-> Installing Dependencies"
	$(VENV)/bin/pip install -r requirements.txt

build: $(SRC)
	. $(VENV)/bin/activate && $(VENV)/bin/pyinstaller --onefile \
	--name $(APP_NAME)_v$(VERSION) \
	--add-data "app/templates:app/templates" \
	--add-data "app/static:app/static" \
	$(SRC)

build-docker: $(SRC)
	pyinstaller --onefile \
	--name $(APP_NAME)_v$(VERSION) \
	--add-data "app/templates:app/templates" \
	--add-data "app/static:app/static" \
	$(SRC)

run:
	@echo "-> Running Flask App"
	. $(VENV)/bin/activate && ./dist/$(APP_NAME)_v$(VERSION)

clean:
	@echo "-> Removing Virtual Environment"
	rm -rf $(VENV)

clean-build:
	@echo "-> Removing Build"
	rm -rf build dist instance $(APP_NAME)_v$(VERSION).spec

test: $(VENV)/bin/activate
	@echo "-> Running Tests"
	. $(VENV)/bin/activate && $(VENV)/bin/pytest -s

source: 
	@echo "-> Sourcing Virtual Environment"
	. $(VENV)/bin/activate

.PHONY: all check-python install run clean clean-build test build source