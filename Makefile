SETUP := python setup.py

all: clean build test docs install

build:
	$(SETUP) build

test:
	$(SETUP) test

docs:
	$(SETUP) docs

install:
	$(SETUP) install

uninstall:
	pip uninstall thrusted

clean:
	rm -rf .\dist
	rm -rf .\build
	rm -rf .\.eggs

help:
	@echo 'Makefile build automation                                              '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make all                         clean, build, test, install        '
	@echo '   make build                       compiles source                    '
	@echo '   make test                        runs all the tests                 '
	@echo '   make install                     install the built application      '
	@echo '   make uninstall                   uninstall the built application    '
	@echo '   make clean                       clean out all temporary files      '
	@echo '   make docs                        generate application documentation '
	@echo '   make help                        displays this help text            '
	@echo '                                                                       '
	@echo 'DEFAULT:                                                               '
	@echo '   make all                                                            '
	@echo '                                                                       '

.PHONY: all build test docs install uninstall clean help
