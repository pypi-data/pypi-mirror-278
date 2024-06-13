from setuptools import setup, find_packages

setup(
    name='doscon_tb_api',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [],
    },
    author='Aleksander Hykkerud',
    author_email='lorithai@gmail.com',
    description='minmalistic library to connect to the thingsboard API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DOSCON-development/doscon_tb_api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)