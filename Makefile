.DEFAULT_GOAL = build
.PHONY = build clean dist

help:
	@echo "  build - run buildout on current code"
	@echo "  clean - rm py[co] files"
	@echo "  dist - rm eggs, parts, downloads, bootstrap.py"
	@echo "  test - run test suite"


bootstrap.py :
	wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py

bin/buildout : bootstrap.py
	python2 bootstrap.py

build: bin/buildout
	python2 bin/buildout

clean:
	find . -name '*.py[oc~]'| xargs rm -f

dist: clean
	rm -rf bin develop-eggs eggs parts .installed.cfg downloads bootstrap.py

test:
	./bin/python2 run_tests.py
