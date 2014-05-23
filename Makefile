SHELL := /bin/bash
.PHONY : all

all :

test-write :
	./test/test_write.py | tee /tmp/test_write.geo
