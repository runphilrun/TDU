setup.py := python setup.py
sphinx-build := sphinx-build ./docs ./build/docs -E -d ./.doctrees -q -n -b
sphinx-deploy := travis-sphinx --source=./docs --outdir=./build/docs

all: clean build test docs install

build:
	$(setup.py) build

test:
	$(sphinx-build) doctest

docs:
	$(sphinx-build) html

docs-deploy:
	$(sphinx-deploy) deploy

install:
	$(setup.py) install

uninstall:
	pip uninstall thrusted

clean:
	rm -rf ./dist
	rm -rf ./build
	rm -rf ./.eggs
	rm -rf ./src/thrusted.egg-info
	rm -rf ./.doctrees

deploy:
	$(setup.py) register -r ${source}
	$(setup.py) sdist upload -r ${source}

help:
	@echo 'Makefile build automation                                              '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make all                         clean, build, test, docs, install  '
	@echo '   make build                       compiles source                    '
	@echo '   make test                        runs all the tests                 '
	@echo '   make install                     install the built application      '
	@echo '   make uninstall                   uninstall the built application    '
	@echo '   make clean                       clean out all temporary files      '
	@echo '   make docs                        generate application documentation '
	@echo '   make docs-deploy                 deploy built docs to gh-pages      '
	@echo '   make help                        displays this help text            '
	@echo '                                                                       '
	@echo 'DEFAULT:                                                               '
	@echo '   make all                                                            '
	@echo '                                                                       '

.PHONY: all build test docs install uninstall help
