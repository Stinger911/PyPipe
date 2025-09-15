.DEFAULT_GOAL := help

help: ## this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m%s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@printf "\n\n"

TOPTARGETS := all clean

install: ## install the dependencies
	poetry install
	poetry update

cc: ## run the code cleaning
	poetry run ruff format pypipe
	poetry run ruff check --select I --fix pypipe
	poetry run ruff format src
	poetry run ruff check --select I --fix src
	poetry run ruff format tests
	poetry run ruff check --select I --fix tests

test: ## run the tests on local environment
	python -m unittest discover -s tests