format:
	poetry run isort -rc .
	poetry run black .

test:
	poetry run flake8 .
	poetry run mypy keybase_loremipsumbot/