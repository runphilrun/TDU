SETUP := python setup.py

all: build test install

build:
	$(SETUP) build

test:
	$(SETUP) test

install:
	$(SETUP) install --record files.txt

uninstall:
	pip uninstall thrusted

clean:
	rm -rf .\dist
	rm -rf .\build


help:
	@echo 'Makefile build automation                                              '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make all                         dependencies, build, test, install '
	@echo '   make build                       compiles source                    '
	@echo '   make test                        runs unit tests                    '
	@echo '   make install                     install the built application      '
	@echo '   make uninstall                   uninstall the built application    '
	@echo '   make clean                       clean out all temporary files      '
	@echo '   make help                        displays this help text            '
	@echo '                                                                       '
	@echo 'DEFAULT:                                                               '
	@echo '   make all                                                            '
	@echo '                                                                       '

.PHONY: all get-deps build test install clean help
