from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="validlink",
    version="0.2",
    description="A simple URL validity checker",
    author="Fidal",
    author_email="mrfidal@proton.me",
    url="https://mrfidal.in/basic-pip-package/validlink",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
