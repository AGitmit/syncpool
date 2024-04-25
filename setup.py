from setuptools import setup, find_packages

setup(
    name="syncpool-py",
    description="Synchronization object-pools, imitating Go's (Golang) sync.Pool implementation.",
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=['src.tests']),
    author="Amit Nakash",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    url="https://github.com/AGitmit/syncpool",
)
