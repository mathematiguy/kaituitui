PYTHON ?= venv/bin/python3.10

run: venv
	bash run.sh

clean:
	rm -rf gif/*.eps gif/*.gif

venv:
	python3 -m venv venv

install:
	python3 -m pip install -r requirements.txt
