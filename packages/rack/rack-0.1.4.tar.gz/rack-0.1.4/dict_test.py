#!/usr/bin/env python
# SPDX-FileCopyrightText: 2024 Jérôme Carretero <cJ-rack@zougloub.eu> & contributors
# SPDX-License-Identifier: MIT

import os
import logging
import tempfile

import pytest

from .dict import PersistentDict as dict_


logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def dir():
	with tempfile.TemporaryDirectory() as tdir:
		yield tdir

@pytest.fixture()
def d(dir, foo):
	name = os.path.join(dir, "dict_1")
	with dict_(name=name) as d:
		data = {
			foo: 1,
			foo +"1": 1,
		}
		d.update(**data)
		yield d
		d.clear()

@pytest.fixture()
def foo():
	return "pouet"

def test_smoke(d, foo):
	d[1] = 2
	assert d[1] == 2

	assert 1 in d

	d["2"] = 3
	assert d.get("2") == 3

	d.update(a=1)

	d["2"] = 4

	logger.info("keys")
	for x in d:
		logger.info("- %s", x)

	logger.info("keys")
	for k in d.keys():
		logger.info("- k:%s", k)

	logger.info("values")
	for v in d.values():
		logger.info("- v:%s",  v)

	logger.info("items")
	for k, v in d.items():
		logger.info("- %s=%s", k, v)

	logger.info("keys2")
	for k in d:
		logger.info("- %s", k)


def test_clear(d, foo):
	foo1 = foo + "1"

	assert foo in d
	assert foo1 in d

	l = len(d)
	assert l > 1

	d.clear()
	assert foo not in d
	assert foo1 not in d
	assert len(d) == 0


def test_delete(d, foo):
	foo1 = foo + "1"
	assert foo in d
	assert foo1 in d

	del d[foo]

	assert foo not in d
	assert foo1 in d

def test_pop(d, foo):
	assert foo in d

	res = d.pop(foo)
	assert foo not in d
	assert res == 1

def test_popitem(d, foo):
	l = len(d)
	assert l

	x = d.popitem()
	assert len(d) == l-1

def test_update(d, foo):
	assert not "foo2" in d
	assert not "foo3" in d

	l = len(d)

	d.update(foo2=1, foo3=1)

	assert "foo2" in d
	assert "foo3" in d
	assert len(d) == l+2

def test_setdefault(d, foo):
	foo2 = foo +"2"
	assert foo in d
	v = d[foo]

	res = d.setdefault(foo)
	assert res == v

	assert not foo2 in d
	res = d.setdefault(foo2, 2)
	assert res == 2
	assert foo2 in d

	res = d.setdefault(foo2)
	assert res == 2


def test_copy(d, foo):
	foo1 = foo + "1"
	foo2 = foo + "2"
	foo3 = foo + "3"

	assert foo in d
	assert foo1 in d

	new = d.copy()

	with new as n:
		assert foo in n
		assert foo1 in n

		n[foo2] = 1
		assert foo2 in n
		assert not foo2 in d

		del d[foo]
		assert not foo in d
		assert foo in n


def test_fromkeys(d, foo):
	keys =[1,2,3,4,5]
	new = d.fromkeys(keys, foo)

	with new as n:
		for k in keys:
			assert k in n
		for v in n.values():
			assert v == foo
