from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='myErp',
    version='5.1',
    author='Neeraj Yadav',
    author_email='nyadav70096@gmail.com',
    description='A Minimal Client for NITJ Erp',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/neernjan1/pyErp',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'BeautifulSoup4',
        'matplotlib',
        'requests',
        'tabulate',
        'pandas',
        'colorama',
        'tqdm'
        
    ],
    zip_safe=True,
    include_package_data=True,
    package_data={
        '': ['LICENSE.txt', 'README.md']
    },
    entry_points={
        'console_scripts': [
            'myerp = myErp.erp:exit'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
)
