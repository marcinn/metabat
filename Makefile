.DEFAULT_GOAL = build
.PHONY = build clean dist

help:
	@echo "  build - run buildout on current code"
	@echo "  clean - rm py[co] files"
	@echo "  dist - rm eggs, parts, downloads, bootstrap.py"


bootstrap.py :
	wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py

bin/buildout : bootstrap.py
	python bootstrap.py

build: bin/buildout
	python bin/buildout

clean:
	find . -name '*.py[oc~]'| xargs rm -f

dist: clean
	rm -rf bin develop-eggs eggs parts .installed.cfg downloads bootstrap.py
