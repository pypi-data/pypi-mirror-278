from setuptools import find_packages, setup

setup(
    name='rl-test-common',
    version='0.1.4',
    description='Common',
    author='Antonio Corluka',
    author_email='antonio.corluka@outlook.com',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        'psutil'
    ]
)
