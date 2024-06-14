from setuptools import setup, find_packages

setup(
    name='sezer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
    ],
    author='Adınız',
    author_email='email@example.com',
    description='Sezer\'s swiss army knife',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Natgho/sezer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
