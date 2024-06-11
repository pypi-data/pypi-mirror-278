import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="mygo",
    version="1.0.0",
    author="HisAtri",
    author_email="yz@ghacg.com",
    description="Some useful tools",
    install_requires=[],
    long_description=open(r'README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PythonNotebook/pyMygo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
