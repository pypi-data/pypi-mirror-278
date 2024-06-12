from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='asyncpg_lite',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'asyncpg>=0.21.0',
    ],
    author='Алексей Яковенко',
    author_email='mr.mnogo@gmail.com',
    description='Простая асинхронная библиотека, основанная на asyncpg',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Yakvenalex/asyncpg_lite',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
