#!/usr/bin/env python
# SPDX-FileCopyrightText: 2019,2024 Jérôme Carretero <cJ-rack@zougloub.eu> & contributors
# SPDX-License-Identifier: MIT

import os
import logging
import marshal
import typing as t

import lmdb

from .utils import create_new_name, h


logger = logging.getLogger(__name__)


class PersistentDict(t.Dict):
	"""
	Persistent dict using LMDB database as backend
	"""
	def __init__(self, name=None, hasher=None, serdes=None):
		self._name = name
		if hasher is None:
			hasher = h
		self._h = hasher
		self._debug = False
		if serdes is None:
			self._loads = marshal.loads
			self._dumps = marshal.dumps
		else:
			self._loads, self._dumps = serdes

	def __enter__(self):
		self._env = env = lmdb.open(self._name + ".lmdb",
		 subdir=False,
		 max_dbs=4,
		 sync=False,
		 map_size=(50<<30),
		)

		self.h2n = env.open_db(b"h2n",
		 dupsort=True,
		 dupfixed=True,
		 create=True,
		)

		self.n2k = env.open_db(b"n2k",
		 create=True,
		)

		self.n2v = env.open_db(b"n2v",
		 create=True,
		)

		return self

	def __exit__(self, ext_type, exc_value, exc_tb):
		self._env.close()


	def _set(self, txn, key, value):
		k = self._dumps(key)
		v = self._dumps(value)
		h = self._h(k)

		with txn.cursor(db=self.h2n) as cur:
			res = cur.set_key(h)
			if res:
				if self._debug:
					logger.debug("Found compatible hash key")
				for n_ in cur.iternext_dup():
					d = txn.get(n_, db=self.n2k)
					if d == k:
						if self._debug:
							logger.debug("Replace %s (%d) = %s",
							 key, int.from_bytes(n_, "big"), value)
						txn.put(n_, v, db=self.n2v)
						return

			with txn.cursor(db=self.n2k) as cur:
				res = cur.last()
				if res:
					n_ = int.from_bytes(cur.key(), "big")+1
				else:
					n_ = 1
			n = n_.to_bytes(8, "big")
			if self._debug:
				logger.debug("Insert #%d", n_)
			txn.put(h, n, db=self.h2n)
			txn.put(n, k, db=self.n2k)
			txn.put(n, v, db=self.n2v)

	def __setitem__(self, key, value):
		with self._env.begin(write=True) as txn:
			self._set(txn, key, value)

	def __getitem__(self, key):
		with self._env.begin() as txn:
			k = self._dumps(key)
			h = self._h(k)

			with txn.cursor(db=self.h2n) as cur:
				res = cur.set_key(h)
				if res:
					for n_ in cur.iternext_dup():
						d = txn.get(n_, db=self.n2k)
						if d == k:
							return self._loads(txn.get(n_, db=self.n2v))

		raise KeyError(key)

	def __delitem__(self, key):
		k = self._dumps(key)
		h = self._h(k)
		with self._env.begin(write=True) as txn:
			with txn.cursor(db=self.h2n) as cur:
				res = cur.set_key(h)
				if res:
					for n_ in cur.iternext_dup():
						d = txn.get(n_, db=self.n2k)
						if d == k:
							txn.delete(n_, db=self.n2v)
							txn.delete(n_, db=self.n2k)
							if cur.count() == 1:
								txn.delete(h, db=self.h2n)
							return
		raise KeyError(key)

	def get(self, key, default=None):
		with self._env.begin() as txn:
			k = self._dumps(key)
			h = self._h(k)

			with txn.cursor(db=self.h2n) as cur:
				res = cur.set_key(h)
				if res:
					for n_ in cur.iternext_dup():
						d = txn.get(n_, db=self.n2k)
						if d == k:
							return self._loads(txn.get(n_, db=self.n2v))

		return default

	def clear(self):
		with self._env.begin(write=True) as txn:
			txn.drop(db=self.n2v, delete=False)
			txn.drop(db=self.n2k, delete=False)
			txn.drop(db=self.h2n, delete=False)


	def update(self, other=None, **kw):
		with self._env.begin(write=True) as txn:
			if other:
				for k, v in other.items():
					self._set(txn, k, v)

			for k, v in kw.items():
				self._set(txn, k, v)

	def __contains__(self, key):
		k = self._dumps(key)
		h = self._h(k)
		with self._env.begin() as txn:
			with txn.cursor(db=self.h2n) as cur:
				res = cur.set_key(h)
				if res:
					for n_ in cur.iternext_dup():
						d = txn.get(n_, db=self.n2k)
						if d == k:
							return True
		return False

	def __len__(self):
		"""
		:return: number of items in dict
		"""
		with self._env.begin(db=self.n2k) as txn:
			s = txn.stat()
			entries = s["entries"]
			return entries

	def keys(self):
		env = self._env
		with env.begin(db=self.n2k) as txn:
			curk = txn.cursor()
			curk.first()
			while True:
				k = curk.value()
				yield self._loads(k)
				if not curk.next():
					break

	def values(self):
		env = self._env
		with env.begin(db=self.n2v) as txn:
			curv = txn.cursor()
			curv.first()
			while True:
				v = curv.value()
				yield self._loads(v)
				if not curv.next():
					break

	def items(self):
		env = self._env
		with env.begin() as txn:
			curk = txn.cursor(db=self.n2k)
			curv = txn.cursor(db=self.n2v)
			curk.first()
			curv.first()
			while True:
				k = curk.value()
				v = curv.value()
				yield self._loads(k), self._loads(v)
				if not curk.next() and curv.next():
					break

	def __iter__(self):
		env = self._env
		with env.begin(db=self.n2k) as txn:
			cur = txn.cursor()
			cur.first()
			while True:
				v = cur.value()
				yield self._loads(v)
				if not cur.next():
					break

	def popitem(self):
		with self._env.begin(write=True) as txn:
			with txn.cursor(db=self.h2n) as cur:
				res = cur.last()
				if res:
					n_ = cur.value()
					k = txn.get(n_, db=self.n2k)
					v = txn.get(n_, db=self.n2v)
					txn.delete(n_, db=self.n2v)
					txn.delete(n_, db=self.n2k)
					if cur.count() == 1:
						txn.delete(cur.key(), db=self.h2n)
					return self._loads(k), self._loads(v)
				raise KeyError("Empty")

	def pop(self, key):
		k = self._dumps(key)
		h = self._h(k)
		with self._env.begin(write=True) as txn:
			with txn.cursor(db=self.h2n) as cur:
				res = cur.set_key(h)
				if res:
					n_ = cur.value()
					v = txn.get(n_, db=self.n2v)
					txn.delete(n_, db=self.n2v)
					txn.delete(n_, db=self.n2k)
					if cur.count() == 1:
						txn.delete(cur.key(), db=self.h2n)
					return self._loads(v)
		raise KeyError()

	def setdefault(self, key, value=None):
		k = self._dumps(key)
		h = self._h(k)
		with self._env.begin(write=True) as txn:
			with txn.cursor(db=self.h2n) as cur:
				res = cur.set_key(h)
				if res:
					for n_ in cur.iternext_dup():
						d = txn.get(n_, db=self.n2k)
						if d == k:
							v = txn.get(n_, db=self.n2v)
							return self._loads(v)
				self._set(txn, key, value)
				return value

	def copy(self, name: str=None):
		new_name = name
		if new_name is None:
			new_name = create_new_name(self._name)
		with PersistentDict(name=new_name) as new:
			with new._env.begin(write=True) as new_txn:
				for k,v in self.items():
					new._set(new_txn, k, v)
		return new

	@classmethod
	def fromkeys(cls, keys: t.Iterable, value=None, name: str=None):
		new_name = name
		if new_name is None:
			new_name = create_new_name()
		with PersistentDict(name=new_name) as new:
			with new._env.begin(write=True) as txn_new:
				for key in keys:
					new._set(txn_new, key, value)
		return new
