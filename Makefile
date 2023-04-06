test:
	@python -m unittest discover -s tests -p "*_test.py" -v

test-report:
	@python test.py

build: test
	@build