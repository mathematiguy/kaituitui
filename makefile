PYTHON ?= venv/bin/python3.10

run:
	python3 kaituitui.py

install:
	$(PYTHON) -m pip install -r requirements.txt
