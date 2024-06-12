import os
import setuptools


long_desc = """# hwrag

RAG pipeline from 南京海维可信.
"""


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "r", encoding="utf-8") as fh:
        return fh.read()


setuptools.setup(
    name="hwrag",
    version=read("VERSION"),
    description="hwrag",
    license="MIT License",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://git.jiankanghao.net/haiwei/hwrag",
    author="haiweikexin",
    author_email="huangxp@haiweikexin.com, jiny@haiweikexin.com",
    packages=["hwrag"],
    install_requires=read("requirements.txt"),
    include_package_data=True,
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
