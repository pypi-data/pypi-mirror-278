from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='trained_scoring_models',
    version='1.0.0',
    author='schubenkin',
    author_email='schubenkin00@gmail.com',
    description='Library contains trained models ',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests>=2.25.1', 'pickle', 'numpy', 'pandas'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='example python',
    python_requires='>=3.11'
)
