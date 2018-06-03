from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [Extension("get_temperature",["get_temperature.pyx"])]
setup(
    name = "get_temperature pyx",
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)