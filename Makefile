.PHONY: build install clean format lint unittest test

build: # force build
	poetry build

install:
	poetry install

format: updatesetup
	isort pentestgpt
	black pentestgpt

updatesetup:
	bash pentestgpt/scripts/update.sh