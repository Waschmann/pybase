import cProfile as cp
import pstats
import io
from time import time
import os
import re

import pandas as pd

_FILE = os.path.realpath(__file__)
_PATH = os.path.dirname(_FILE)
_EXEPATH = os.getcwd()


def _compile(pattern):
	try:
		regex = re.compile(pattern)
		return regex
	except:
		raise


class StrExtract:
	def __init__(self, pattern, default='', trafo=lambda match: match[0]):
		self.regex = _compile(pattern)
		self.default = default
		self.trafo = trafo

	def __call__(self, string):
		match = self.regex.findall(string)
		if not match:
			return self.default
		return self.trafo(match)


class Profiler:
	"""
	Useage:
	prof = Profiler()
	with prof:
		...
	print(prof.stats)
	"""
	def __init__(
		self):
		
		self.__profile = None
		self.__raw = None
		self.__stats = None
		self.__overview = None


	def __enter__(self):
		if self.__profile is not None:
			raise ValueError('Cannot nest profilers. ')
		self.__profile = cp.Profile()
		self.__profile.enable()

	def __exit__(
		self, 
		exec_type, 
		exec_value, 
		traceback):
		
		self.__profile.disable()
		stream = io.StringIO()
		data = pstats.Stats(
			self.__profile, 
			stream=stream)
		data.print_stats()
		stats = stream.getvalue()
		stream.close()
		self.__raw = stats
		self.__overview, self.__stats = _to_pandas(stats)
		self.reset()
		print(str(self) + 'check .stats for details\n')

	def reset(self):
		self.__profile = None

	def save(self, path, sep=','):
		self.stats.to_csv(path, sep=sep, index=False)

	@property
	def stats(self):
		return self.__stats.sort_values('Time', ascending=False).reset_index(drop=True)

	@property
	def raw(self):
		return self.__raw

	def __repr__(self):
		return '\n'+self.__overview+'\n'



## parsing of cProfile-result

_COLS = ['ncalls', 'tottime', 'percall', 'cumtime', 'percall', 'filename:lineno(function)']


_calls = StrExtract(
	pattern=r'(\d+)/?(\d+)?', trafo=lambda x: (x[0][0],)*2 if x[0][1]=='' else x[0])
_file = StrExtract(
	pattern=r'^(.*)/([^/]+):|([^/]+\.py)', 
	default=('', ''), 
	trafo = lambda x: x[0][1:] if x[0][2]!='' else x[0][:2])

def _function_trafo(match):
	match = match[0]
	if match[0] != '':
		return match[0]
	if match[1] != '':
		return match[2] + '.' + match[1]
	if match[-1] != '':
		return match[-1] + '.' + match[-3]
	return match[3]

_function = StrExtract(
	pattern=r'\((.+)\)$|^\{.+\'(.+)\'.+\'(.+)\'|^\{built-in method ([^\s]+)( of type )?([^\s]*).*\}', 
	trafo=_function_trafo)
_line = StrExtract(
	pattern=r':(\d+)', )

_BLACKLIST = {'_lsprof.Profiler', _FILE}


def _to_pandas(result):
	lines = result.strip().split('\n')

	cols = lines[4].strip().split()
	assert len(cols)==len(_COLS) 
	assert all(c==_c for c, _c in zip(cols, _COLS))

	data = []
	for line in lines[5:]:
		fields = line.strip().split(maxsplit=5)
		calls, time, percall, cumtime, _, fileinfo = fields

		if any(b in fileinfo for b in _BLACKLIST):
			continue
		try:
			calls, primitive = _calls(calls)
			fpath, fname = _file(fileinfo)
			fpath = fpath.replace(_EXEPATH, '.')
			function = _function(fileinfo)
			if fname=='':
				fname = '[internal]'
			line = _line(fileinfo)
		except:
			print(f'Could not parse the following line: \n{line}\n\n')
			continue

		res = calls, primitive, time, cumtime, function, fname, fpath, line

		data.append(res)

	header = ['Calls', 'Primitive', 'Time', 'Cumulative', 'Function', 'File', 'FilePath', 'Line']

	dtypes = {'Calls': int, 'Primitive': int, 'Time': float, 'Cumulative': float}
	data = pd.DataFrame(data, columns=header).astype(dtypes)#.query('Time > 0')
	return lines[0], data






