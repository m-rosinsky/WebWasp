from pathlib import Path

from setuptools import find_packages, setup

version = (Path(__file__).parent / "webwasp/VERSION").read_text("ascii").strip()

install_requires = [
    "beautifulsoup4>=4.0.0",
    "readchar>=4.0.0",
    "requests>=2.28.0",
    "pyyaml>=5.3.0",
    "pygments>=2.3.0",
]

setup(
    name="WebWasp",
    version=version,
    url="https://webwasp.readthedocs.io/en/latest/",
    project_urls={
        "Documentation": "https://webwasp.readthedocs.io/en/latest/",
        "Source": "https://github.com/m-rosinsky/WebWasp",
        "Tracker": "https://github.com/m-rosinsky/WebWasp/issues",
    },
    description="A web pentesting command suite",
    long_description=open("README.md", encoding='utf-8').read(),
    author="Mike Rosinsky",
    author_email="rosinskymike@gmail.com",
    maintainer="Mike Rosinsky",
    maintainer_email="rosinskymike@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={"console": ["webwasp = webwasp.webwasp:main"]},
    classifiers=[
        "Framework :: WebWasp",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
    install_requires=install_requires,
)