from itertools import *
from collections import deque
from collections.abc import Iterator




def exhaust(iterable):
	deque(iterable, 0)

def apply(f, iterable):
	exhaust(map(f, iterable))

def starapply(f, iterable):
	exhaust(starmap(f, iterable))

def advance(iterable, n):
	exhaust(islice(iterable, n))



def rotate(iterable, by):
	"""
	Returns an Iterator over (a_by, ..., a_N, a_0, ..., a_by-1) where N = len(iterable). 
	"""
	if isinstance(iterable, Iterator):
		head, tail = tee(iterable, 2)
		return chain(islice(head, by, None), islice(tail, by))
	return chain(islice(iterable, by, None), islice(iterable, by))

def zip_adjacent(iterable, n):
	"""
	Returns an Iterator yielding (a_k, ..., a_k+n-1) for each k < len(iterable) - n. 
	"""
	if isinstance(iterable, Iterator):
		return zip(*(islice(it, i, None) for (i, it) in enumerate(tee(iterable))))
	return zip(*(islice(iterable, i, None) for i in range(n)))



def rollmap(f, iterable, n):
	"""
	Returns an Iterator yielding f((a_k, ..., a_k+n-1)) for each k < len(iterable) - n. 
	"""
	return map(f, zip_adjacent(iterable, n))

def rollstarmap(f, iterable, n):
	"""
	Returns an Iterator yielding f(a_k, ..., a_k+n-1) for each k < len(iterable) - n. 
	"""
	return starmap(f, zip_adjacent(iterable, n))



class jiter:
	"""
	just-in-time-iterator. 
	Advances to idx if accessed & caches previous cache_limit values (using a deque). 
	If cache_limit is None, caches all previous values
	"""
	def __init__(self, iterator, cache_limit=None):
		self._iterator = iterator
		self._cache_limit = cache_limit
		self._cache = [] if cache_limit is None else deque(maxlen=cache_limit)
		self._n = 0

	def __getitem__(self, idx):
		n = len(self)
		if idx < n:
			return self._cache[idx]
		self._cache.extend(islice(self._iterator, 0, idx - n))
		item = next(self._iterator)
		self._cache.append(item)
		self._n = idx + 1
		return item

	def __len__(self):
		return self._n


