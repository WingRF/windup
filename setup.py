from setuptools import setup, Extension


ext_modules = [
    Extension(
        'windup.rfc3339',
        sources=['./src/rfc3339.c'],
        extra_compile_args=['-Ofast', '-std=c99']
    )
]

setup(packages=['windup'], ext_modules=ext_modules)
