VENV := venv
PYTHON := python3

all: install

$(VENV)/bin/activate: requirements.txt
	@echo "-> Creating Virtual Environment"
	$(PYTHON) -m venv $(VENV)

install: $(VENV)/bin/activate
	@echo "-> Installing Dependencies"
	$(VENV)/bin/pip install -r requirements.txt

run:
	@echo "-> Running Flask App"
	. $(VENV)/bin/activate && $(VENV)/bin/python run.py

clean:
	@echo "-> Removing Virtual Environment"
	rm -rf $(VENV)

test: $(VENV)/bin/activate
	@echo "-> Running Tests"
	. $(VENV)/bin/activate && $(VENV)/bin/pytest

.PHONY: all install run clean test