from setuptools import find_packages, setup

setup(
    name='rl-test-storage-handlers',
    version='0.1.4',
    description='Storage handlers',
    author='Antonio Corluka',
    author_email='antonio.corluka@outlook.com',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        'python-dotenv',
        'rl-test-common'
    ]
)
