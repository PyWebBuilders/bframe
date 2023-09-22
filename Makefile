test:
	@python -m unittest discover -s tests -p "*_test.py" -v

test-report:
	@python test.py

build: test
	@build

build-docs:
	copy README.md docs\\index.md
	@mkdocs build