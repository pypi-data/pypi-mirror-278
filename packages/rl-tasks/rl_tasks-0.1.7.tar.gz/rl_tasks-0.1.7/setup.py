from setuptools import find_packages, setup

setup(
    name='rl-tasks',
    version='0.1.7',
    description='ReversingLabs Test',
    author='Antonio Corluka',
    author_email='antonio.corluka@outlook.com',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        'python-dotenv',
        'rl-test-common',
        'rl-test-storage-handlers',
        'rl-test-task-1',
        'rl-test-task-2',
        'rl-test-task-3'
    ]
)
