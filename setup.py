from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

setup(
    name='mobile-cooperation',
    version='',
    packages=['PGG', 'KDTree', 'MobilityModel', 'ProbabilityModel'],
    url='',
    license='',
    author='',
    author_email='',
    description='',
    include_dirs=[np.get_include()],
    ext_modules=cythonize("PGG/*.pyx", include_path=[np.get_include()])

)