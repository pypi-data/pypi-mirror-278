from setuptools import setup, find_packages


setup(
    name="tubemixer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytube",
        "pydub",
    ],
    entry_points={
        'console_scripts': [
            'tubemixer=tubemixer.__main__.main',
        ],
    },
    author='Dylan M. Garrett',
    author_email='nullchamberdev@pm.me',
    description='A tool to extract audio from YouTube videos',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nullchamber/tubemixer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
