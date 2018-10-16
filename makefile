SHELL := /bin/bash

install:
		source venv/bin/activate
		pip3 install -r requirements.txt
		python3 manage.py db upgrade

test:
		python3 -m pytest tests/

run:
		source venv/bin/activate
		pip3 install -r requirements.txt
		python3 manage.py runserver -h 0.0.0.0
