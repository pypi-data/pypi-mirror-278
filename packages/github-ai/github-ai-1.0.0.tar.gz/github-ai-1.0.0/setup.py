from setuptools import setup, find_packages

setup(
    name="github-ai",
    version="1.0.0",
    author="Fidal",
    author_email="mrfidal@proton.me",
    description="A tool to search GitHub repositories using the GitHub API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://mrfidal.in/basic-pip-package/github-ai",
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
)
