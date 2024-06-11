from setuptools import setup, find_packages
from pathlib import Path

dir = Path(__file__).parent
README = (dir / "README.md").read_text()

setup(
    name='PrettyDF',
    version='1.1',
    packages=find_packages(),
    author='DawnSaju',
    description='Pretty Print DataFrames',
    long_description=README,
    long_description_content_type='text/markdown',
    author_email = "dawnsajubusiness@gmail.com",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],

    install_requires=[
        'pandas',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'prettydf = PrettyDF:hello'
        ]
    }
)

