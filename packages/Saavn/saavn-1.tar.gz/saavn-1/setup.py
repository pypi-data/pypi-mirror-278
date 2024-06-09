from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='Saavn',
    version='1',
    author='Neeraj Yadav',
    author_email='nyadav70096@gmail.com',
    description='A Minimal Client for JioSaavn',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/neernjan1/Saavn',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'BeautifulSoup4',
        'pyDes',
        'requests',
        'tqdm',
        'mutagen'
    ],
    zip_safe=True,
    include_package_data=True,
    package_data={
        '': ['LICENSE.txt', 'README.md']
    },
    entry_points={
        'console_scripts': [
            'saavn = saavn.cli:exit'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
)
