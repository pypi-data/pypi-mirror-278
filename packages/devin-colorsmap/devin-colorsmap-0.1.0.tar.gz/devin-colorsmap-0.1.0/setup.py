from setuptools import setup, find_packages

setup(
    name='devin-colorsmap',
    version='0.1.0',
    author='Your Name',
    author_email='long.sc@qq.com',
    description='A short description of your library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Devin-Long-7/esil',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)