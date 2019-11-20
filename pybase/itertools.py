from itertools import *
from collections import deque
from collections.abc import Iterator




def exhaust(iterable):
	deque(iterable, 0)

def apply(f, iterable):
	exhaust(map(f, iterable))

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


