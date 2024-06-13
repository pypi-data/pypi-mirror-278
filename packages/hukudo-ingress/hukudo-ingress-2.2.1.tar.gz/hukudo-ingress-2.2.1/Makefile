MAKEFLAGS += --always-make

_: code-style unit-test

clean:
	rm -rf build/ dist/

code-style:
	./env/dev/git-hooks/pre-commit

unit-test:
	pytest --cov=. --cov-report=html --cov-report=term --cov-report=xml

build:
	python setup.py sdist bdist_wheel

patch_release: clean unit-test
	bumpversion patch
	make build push_with_tags upload

minor_release: clean unit-test
	bumpversion minor
	make build push_with_tags upload

major_release: clean unit-test
	bumpversion major
	make build push_with_tags upload

push_with_tags:
	git push
	git push --tags

upload:
	twine upload --repository pypi-hukudo dist/*

requirements.txt:
	pip-compile

dev-setup:
	pyenv virtualenv 3.10.11 hukudo-ingress
	pyenv local hukudo-ingress
	pip install -U pip
	pip install -e .[dev]
