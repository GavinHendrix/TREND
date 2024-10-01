VENV := venv
PYTHON := python3
APP_NAME := TREND
SRC := run.py

all: install build

$(VENV)/bin/activate: requirements.txt
	@echo "-> Creating Virtual Environment"
	$(PYTHON) -m venv $(VENV)

install: $(VENV)/bin/activate
	@echo "-> Installing Dependencies"
	$(VENV)/bin/pip install -r requirements.txt

build: $(SRC)
	$(VENV)/bin/pyinstaller --onefile --name $(APP_NAME) \
	--add-data "app/templates:app/templates" \
	--add-data "app/static:app/static" \
	$(SRC)

run:
	@echo "-> Running Flask App"
	. $(VENV)/bin/activate && $(VENV)/bin/python run.py

clean:
	@echo "-> Removing Virtual Environment"
	rm -rf $(VENV)

clean-build:
	@echo "-> Removing Build"
	rm -rf build dist $(APP_NAME).spec

test: $(VENV)/bin/activate
	@echo "-> Running Tests"
	. $(VENV)/bin/activate && $(VENV)/bin/pytest -s

source: 
	@echo "-> Sourcing Virtual Environment"
	. $(VENV)/bin/activate

.PHONY: all install run clean clean-build test build source