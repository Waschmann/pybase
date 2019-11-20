from functools import *



def _compose(f, g):
	return lambda x: f(g(x))

def _starcompose(f, g):
	return lambda x: f(*g(x))

def compose(*funs):
	return reduce(_compose, funs)

def startcompose(*funs):
	return reduce(_starcompose, funs)

