from setuptools import setup, find_packages

setup(
    name='PrettyDF',
    version='0.3',
    packages=find_packages(),
    author='DawnSaju',
    description='Pretty Print DataFrames',
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

