from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# Get OpenMP setting from environment  
try:
    use_omp = int(os.environ['USE_OMP'])
except KeyError:
    use_omp = True

# Custom builder to handler compiler flags. Edit if needed.
class build_ext_subclass(build_ext):
    def build_extensions(self):
        comp = self.compiler.compiler_type 
        if comp in ('unix', 'cygwin', 'mingw32'):
            # Check if build is with OpenMP 
            if use_omp:
                extra_compile_args = ['-std=c99', '-O3', '-fopenmp']
                extra_link_args=['-lgomp']
            else:
                extra_compile_args = ['-std=c99', '-O3']
                extra_link_args = []
        elif comp == 'msvc':
            extra_compile_args = ['/Ox']
            extra_link_args = []
            if use_omp:
                extra_compile_args.append('/openmp')
        else:
            # Add support for more compilers here
            raise ValueError('Compiler flags undefined for %s. Please modify setup.py and add compiler flags'
                             % comp)
        self.extensions[0].extra_compile_args = extra_compile_args
        self.extensions[0].extra_link_args = extra_link_args
        build_ext.build_extensions(self)

    def finalize_options(self):
        '''
        In order to avoid premature import of numpy before it gets installed as a dependency
        get numpy include directories during the extensions building process
	http://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py
        '''
        build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

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
    ext_modules=cythonize("PGG/*.pyx", include_path=[np.get_include()]),
    cmdclass = {'build_ext': build_ext_subclass }
    
)