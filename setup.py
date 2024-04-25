from setuptools import setup, find_packages

setup(
    name="syncpool",
    description="Synchronization object-pools, imitating Go's (Golang) sync.Pool implementation.",
    packages=find_packages(),
    author="Amit Nakash",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    url="https://github.com/AGitmit/syncpool.git",
)
