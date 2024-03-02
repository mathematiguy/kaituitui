PYTHON ?= venv/bin/python3.10

run: venv
	$(PYTHON) kaituitui.py

clean:
	rm -rf *.eps *.gif

venv:
	python3 -m venv venv

install:
	python3 -m pip install -r requirements.txt
