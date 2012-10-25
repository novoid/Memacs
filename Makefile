# note: This file is just for development purposes


all: clean quiettest whitespace todo pep8

whitespace:
	@echo "removing trailing whitespaces"
	@find .  -name "*.py" -exec remove-trailing-whitespace.py {} \; 

test:
	@nosetests

quiettest:
	@nosetests >/dev/null 2>&1 || echo "!!!!!!!!!!!! \n nosetests has errors\n!!!!!!!!!!!!\n"

todo:
	@echo "TODO:"
	@grep -Hnr TODO * | grep -v Makefile | grep -v ".pyc" | grep -v ".py~"  | grep ".py" | grep -v "tmp" || echo 

pep8:
	@echo "pep8:"
	@find . -name "*.py" -exec pep8 {} \; | grep -v "tmp" || echo

pylint:
	@echo "pylint:"
	@find .  -name "*.py" -exec pylint {} \; | grep -v "tmp" || echo


exec:
	@echo "executing all crontab entries"
	@crontab -l | grep . | grep -v "#" | cut -d '*' -f6- | /bin/sh

clean:
	@find  -name "*.pyc" -exec rm {} \;
	@find  -name "*~" -exec rm {} \;
	@find  -name "#*" -exec rm {} \;
	@find  -name ".#*" -exec rm {} \;
	@rm -rf core
	@rm -rf MANIFEST build/ dist 

countorgmodeentries:
	@echo "number of orgmode-entries in ~/orgmode/memacs/*.org_archive:"
	@grep -Hnr "\*\*" ~/orgmode/memacs/*.org_archive | wc

upload:
	python setup.py sdist upload

pipcheckouttest:
	mkdir -p /tmp/memacs-test
	virtualenv /tmp/memacs-test --no-site-packages
	source /tmp/memacs-test/bin/activate
	pip install memacs
	deactivate