import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="portfolio-manager",
    version="0.0.1",
    author="James Curwell -- George Calvert",
    author_email="jamescurwell97@gmail.com",
    description="Simple tool for monitoring investment portfolio performance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/J-Curwell/portfolio-manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
