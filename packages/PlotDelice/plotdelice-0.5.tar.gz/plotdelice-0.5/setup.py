from setuptools import setup, find_packages

setup(
    name='PlotDelice',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'scipy',
        'statsmodels',
    ],
    entry_points={
        'console_scripts': [],
    },
    author='Quillan Favey',
    author_email='quillan.favey@gmail.com',
    description='A package for creating old school style plots',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/daggermaster3000/plotdelice',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
