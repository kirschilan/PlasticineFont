VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: venv install test run git-push

venv:
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip

install: venv
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@$(PIP) install -r dev-requirements.txt
	@$(PIP) install -e .

test: install
	@$(PYTHON) -m pytest

run: test
	@OPENAI_API_KEY=$$(security find-generic-password -a $$USER -s openai_api_key -w) \
	$(PYTHON) utils/generate_glyphs.py

glyph: test
	$(PYTHON) utils/glyphs_maker_diffusers.py

alpha: test
	$(PYTHON) utils/glyph_bg_to_alpha.py

git-push: test
	@if [ -z "$(m)" ]; then \
		echo "Usage: make git-push m='your commit message'"; \
		exit 1; \
	fi
	git add .
	git commit -m "$(m)"
	git push