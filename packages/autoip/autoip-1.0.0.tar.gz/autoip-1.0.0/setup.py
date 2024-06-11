from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='autoip',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'requests[socks]',
    ],
    entry_points={
        'console_scripts': [
            'autoip=autoip.autoip:main',
        ],
    },
    author='Fidal',
    author_email='mrfidal@proton.me',
    description='AutoIP - Automate IP address changes using Tor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ByteBreac/autoip',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
