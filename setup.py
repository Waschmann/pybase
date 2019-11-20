from distutils.core import setup

setup(
        name='dwa', 
        version=0.1, 
        packages=['itertools', 'functools', 'profiling'], 
        install_requires=[
            "numpy", 
            "pandas"
            ]
        )
