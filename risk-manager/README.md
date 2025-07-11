## Setup
pip install -r requirements-dev.txt

## Format Code
black .

## Run Linter
flake8 .
pylint main.py

## Run Tests
pytest