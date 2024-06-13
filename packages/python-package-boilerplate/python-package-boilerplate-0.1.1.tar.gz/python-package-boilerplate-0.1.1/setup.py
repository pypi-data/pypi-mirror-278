from setuptools import setup, find_packages

setup(
    name="python-package-boilerplate",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Runners Co., Ltd.",
    author_email="dev@runners.im",
    description="A boilerplate Python package for easy project setup",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RUNNERS-IM/python-package-boilerplate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)
