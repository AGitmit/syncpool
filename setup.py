from setuptools import setup, find_packages

setup(
    name="syncpool-py",
    version="0.1.1",
    description="Synchronization object-pools, imitating Go's (Golang) sync.Pool implementation.",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests"]),
    author="Amit Nakash",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    url="https://github.com/AGitmit/syncpool",
)
