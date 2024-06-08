TAG?=0.4.0

install:
	@pip install --no-cache-dir .'[dev]'

black:
	black flowi tests

run-tests:
	(cd tests && pytest -s --cov=./ --cov-report=xml)

build:
	docker build -t psilvaleo/flowi .

push:
	docker push psilvaleo/flowi:latest
