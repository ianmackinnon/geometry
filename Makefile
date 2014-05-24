SHELL := /bin/bash
.PHONY : all test test-write test-read

all :

test : test-write test-read

test-write :
	test/test_write.py > /tmp/test_write.geo

test-read :
	test/test_read.py test/example.geo > /tmp/test_read.geo
