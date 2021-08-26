install:
	poetry install
publish:
	poetry build
	poetry publish --dry-run
test:
	poetry run pytest
test-with-coverage:
	poetry run pytest --cov=pageloader tests  --cov-report xml
package-install:
	python3 -m pip install --user dist/*.whl
package-reinstall:
	python3 -m pip install --user dist/*.whl --force-reinstall
lint:
	poetry run flake8 pageloader
analyze:
	poetry run mypy pageloader
isort:
	poetry run isort pageloader
	poetry run isort tests/*.py
pageloader:
	poetry run pageloader