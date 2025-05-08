from setuptools import setup, find_packages

setup(
    name='pre-commit-hooks-custom',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'check-added-large-files1=pre_commit_hooks.check_added_large_files1:main',
        ],
    },
)