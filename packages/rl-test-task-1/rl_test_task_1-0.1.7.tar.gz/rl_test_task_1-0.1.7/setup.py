from setuptools import find_packages, setup

setup(
    name='rl-test-task-1',
    version='0.1.7',
    description='Task 1',
    author='Antonio Corluka',
    author_email='antonio.corluka@outlook.com',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        'python-dotenv',
        'rl-test-common',
        'rl-test-storage-handlers'
    ]
)
