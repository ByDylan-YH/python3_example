#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager

@contextmanager
def closing(fname):
    f = None
    try:
        f = open(fname, 'r')
        yield f
    finally:
        if f:
            f.close()

with closing('E:/WorkSpace/PycharmProjects/python3_example/samples/context/text.txt') as f:
    print(f.read())
