from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='textPlay',
    version='0.1.2',
    description='A package for many unique text tools. to make your text beautiful.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rakeshkanna-rk/textPlay',
    author='Rakesh Kanna S',
    license="Apache License 2.0",
    author_email='rakeshkanna0108@gmail.com',
    packages=find_packages(),
    keywords=['text tools', 'cli', 'terminal', 'google search', 'web search', 'morse code', 'decode', 'encode', 'box', 'colors', 'options', 'password generator', 'progress bar', 'encryption animation'],
    install_requires=[
        "click>=8.1.7",
        "beautifulsoup4>=4.12.3",
        "requests>=2.31.0",
        "keyboard>=0.13.5",
    ],
    project_urls={
        'GitHub': 'https://github.com/rakeshkanna-rk/textPlay',
        'Python Package Index': 'https://pypi.org/project/textPlay/',
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'textplay = textPlay.cli:textPlay_cli'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)
