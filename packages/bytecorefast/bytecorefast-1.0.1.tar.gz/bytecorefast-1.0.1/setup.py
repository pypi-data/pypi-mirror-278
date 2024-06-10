from setuptools import setup, Extension, find_packages

module = Extension(
    'bytecorefast.fast_emulator',
    sources=[
        'src/bytecorefast/fast_emulator.c',
        'src/emulator.c',
        'src/control_unit.c',
        'src/memory.c'
    ],
    include_dirs=['src'],
    extra_compile_args=['-O3'],
)

setup(
    ext_modules=[module],
    packages=find_packages(where='src', exclude=['benchmarks', 'tests']),
    package_dir={'': 'src'},
    package_data={'': ['*.h']},
    include_package_data=True,
)
