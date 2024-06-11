from setuptools import setup, find_packages

setup(
    name='jrnl2tumblr',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pytumblr',
    ],
    tests_require=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'jrnl2tumblr=jrnl2tumblr.__main__:main',
        ],
    },
    author='Ricardo Ruiz Fernández de Alba',
    author_email='ricardoruizfdez@gmail.com',
    description='Publish your jrnl entries on your Tumblr.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eigenric/jrnl2tumblr',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
