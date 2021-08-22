install:
	poetry install
build:
	poetry build
test:
	poetry run pytest
test-with-coverage:
	poetry run pytest --cov=pageloader tests  --cov-report xml
package-install:
	python3 -m pip install --user dist/*.whl
package-reinstall:
	python3 -m pip install --user dist/*.whl --force-reinstall
publish:
	poetry publish --dry-run
lint:
	poetry run flake8 gendiff
pageloader:
	poetry run pageloader