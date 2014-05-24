SHELL := /bin/bash
.PHONY : all test test-write test-read

all :

test : test-write test-read

test-write :
	test/test_write.py | tee /tmp/test_write.geo

test-read :
	test/test_read.py test/example.geo
