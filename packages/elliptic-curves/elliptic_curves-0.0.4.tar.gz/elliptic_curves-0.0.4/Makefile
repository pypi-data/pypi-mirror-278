python = python3.11
MAXLINE = 120

SETUP_FILES = pyproject.toml
LOGO_FILE = logo.png

BUILD_DIR = dist
DOC_DIR = docs
PDOC_DIR = static
SRC_DIR = src
BUILD_VENV = benv
VENV = venv

get_url = from tomllib import loads; print(loads(open("pyproject.toml").read().strip())["project"]["urls"]["Homepage"])

.PHONY: package doc format lint type test clean

package: $(BUILD_DIR) $(BUILD_VENV)
	$(BUILD_VENV)/bin/python -m build -o $(BUILD_DIR) .

doc: $(DOC_DIR) $(VENV)
	cp $(LOGO_FILE) $(DOC_DIR)/$(LOGO_FILE)
	VERSION="v$$($(VENV)/bin/python -m setuptools_scm)" \
	$(VENV)/bin/pdoc -o $(DOC_DIR) -t $(PDOC_DIR) --logo "$(LOGO_FILE)" --logo-link "$$( \
		$(VENV)/bin/python -c '$(get_url)' \
	)" $(filter-out %.egg-info/,$(wildcard $(SRC_DIR)/*/))

format: $(VENV)
	$(VENV)/bin/isort -l $(MAXLINE) --profile black --no-sections --combine-as --gitignore .
	$(VENV)/bin/black --line-length=$(MAXLINE) .

lint: $(VENV)
	$(VENV)/bin/flake8 --max-line-length=$(MAXLINE) .

type: $(VENV)
	$(VENV)/bin/mypy .

test: $(VENV)
	$(VENV)/bin/python -m unittest

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(DOC_DIR):
	mkdir -p $(DOC_DIR)

$(BUILD_VENV): $(SETUP_FILES)
	$(python) -m venv $(BUILD_VENV)
	$(BUILD_VENV)/bin/pip install -U pip build
	touch $(BUILD_VENV)

$(VENV): $(SETUP_FILES)
	$(python) -m venv $(VENV)
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -e .[dev,doc,quality,testing]
	touch $(VENV)

clean:
	git clean -dfx
