VENV := venv
PYTHON := python3
APP_NAME := TREND
SRC := run.py
VERSION ?= latest

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
	rm -rf build dist instance $(APP_NAME).spec

test: $(VENV)/bin/activate
	@echo "-> Running Tests"
	. $(VENV)/bin/activate && $(VENV)/bin/pytest -s

source: 
	@echo "-> Sourcing Virtual Environment"
	. $(VENV)/bin/activate

# Specify version using make docker-build VERSION=1.0.0
docker-build:
	docker build -t trend-flask-app:$(VERSION) .

# Specify version using make docker-run VERSION=1.0.0
docker-run:
	docker run -p 5050:5050 --env-file .env trend-flask-app:$(VERSION)

docker-push:
	docker tag trend-flask-app:$(VERSION) zackkouba/trend:$(VERSION)
	docker push zackkouba/trend:$(VERSION)

docker-build-amd64:
	docker buildx build --platform linux/amd64 -t trend-flask-app-amd64:$(VERSION) .

docker-push-amd64:
	docker tag trend-flask-app-amd64:$(VERSION) zackkouba/trend:$(VERSION)-amd64
	docker push zackkouba/trend:$(VERSION)-amd64

.PHONY: all install run clean clean-build test build source