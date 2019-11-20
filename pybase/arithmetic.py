from numbers import Number
from itertools import *
from collections.abc import Iterator, Iterable
from operator import add, sub, mul, truediv, pow as pow_, neg, mod, abs as abs_
from operator import and_, or_, lt, gt, eq





class Iter(Iterable):
	"""
	Iterator which supports the use of basic operators lazily
	"""
	def __init__(self, iterable):
		self._iterable = iterable if isinstance(iterable, Iterable) else repeat(iterable)

	# factory function for left-operators
	def __mapper(self, operator, other):
		if not isinstance(other, Iterable):
			return operator(self, repeat(other))
		return Iter(map(operator, self._iterable, other))

	# factory function for right-operators
	def __rmapper(self, operator, other):
		if not isinstance(other, Iterable):
			return operator(repeat(other), self)
		return Iter(map(operator, other, self._iterable))

	# arithmetic
	def __add__(self, other):
		return self.__mapper(add, other)

	def __sub__(self, other):
		return self.__mapper(sub, other)

	def __rsub__(self, other):
		return self.__rmapper(sub, other)

	def __radd__(self, other):
		return self + other

	def __mul__(self, other):
		return self.__mapper(mul, other)

	def __rmul__(self, other):
		return self * other

	def __truediv__(self, other):
		return self.__mapper(truediv, other)

	def __rtruediv__(self, other):
		return self.__rmapper(truediv, other)

	def __pow__(self, other):
		return self.__mapper(pow_, other)

	def __rpow__(self, other):
		return self.__rmapper(pow_, other)

	def __mod__(self, other):
		return self.__mapper(mod, other)

	def __rmod__(self, other):
		return self.__rmapper(mod, other)

	def __abs__(self, other):
		return Iter(map(abs_, self._iterable))

	def __neg__(self):
		return Iter(map(neg, self._iterable))

	# comparison
	def __and__(self, other):
		return self.__mapper(and_, other)

	def __rand__(self, other):
		return self & other 

	def __or__(self, other):
		return self.__mapper(or_, other)

	def __ror__(self, other):
		return self | other

	def __lt__(self, other):
		return self.__mapper(lt, other)

	def __gt__(self, other):
		return self.__mapper(gt, other)

	def __eq__(self, other):
		return self.__mapper(eq, other)

	# class functionality
	def __iter__(self):
		return iter(self._iterable)

	def __str__(self):
		return f'{type(self).__name__}({self._iterable})'


class ifunc:
	"""
	Callable which applies f lazy over an Iterator
	"""
	def __init__(self, f):
		self.__f = f

	def __call__(self, *args):
		return Iter(map(self.__f, *map(Iter, args)))





