from setuptools import setup, find_packages

setup(
    name='flutter-smartstart',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'prompt_toolkit',
    ],
    entry_points={
        'console_scripts': [
            'flutter-smartstart = flutter_smartstart.cli:main',
        ],
    },
    author='Kapil Bhandari',
    author_email='iam.bkpl031@gmail.com',
    description='A CLI tool to create and customize Flutter projects with a clean code folder structure',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/iam-bkpl/flutter_smartstart',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
