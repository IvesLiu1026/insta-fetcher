from setuptools import setup

setup(
    name='insta_fetcher',
    version='0.1.0',
    description='A script to fetch and organize Instagram data using instaloader',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/IvesLiu1026/insta-fetcher.git',
    author='Ives Liu',
    author_email='ivesliutaiwan@gmail.com',
    py_modules=['insta_fetcher'],
    install_requires=[
        'instaloader',
    ],
    entry_points={
        'console_scripts': [
            'insta_fetcher=insta_fetcher:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
