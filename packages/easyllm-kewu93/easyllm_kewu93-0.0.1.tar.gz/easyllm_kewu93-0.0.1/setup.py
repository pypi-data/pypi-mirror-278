from setuptools import setup, find_packages

setup(
    name='easyllm',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    tests_require=[
        'unittest',
    ],
    test_suite='tests',
    author='Kevin Wu',
    author_email='kevinywu@stanford.edu',
    description='A wrapper for your LLM APIs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kevinwu23/easyllm',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.2',
)