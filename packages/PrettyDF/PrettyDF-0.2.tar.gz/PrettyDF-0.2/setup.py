from setuptools import setup, find_packages

setup(
    name='PrettyDF',
    version='0.2',
    packages=find_packages(),
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

