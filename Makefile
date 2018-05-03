all: pylint

.PHONY: pylint
pylint:
	pipenv run pylint -f colorized publ

.PHONY: build
build: pylint
	rm -rf build dist
	python3 setup.py sdist
	python3 setup.py bdist_wheel

.PHONY: upload
upload: build
	twine upload dist/*