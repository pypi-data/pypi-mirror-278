# setup.py

from setuptools import setup, find_packages

setup(
    name='cemirutils',
    version='0.6.3',
    packages=find_packages(),
    install_requires=[],
    author='Cem Emir / Muslu Yüksektepe',
    author_email='musluyuksektepe@gmail.com',
    description='Basit veri işleme, network komutları ve SQL yardımcıları',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cememir/cemirutils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
