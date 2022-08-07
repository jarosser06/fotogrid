import setuptools

with open('README.md') as rdme:
    long_description = rdme.read()


setuptools.setup(
    name='fotogrid',
    version='0.1.0',
    description='Photo grid tool for painters',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jim Rosser',
    packages=setuptools.find_packages(exclude='tests'),
    install_requires=[
        'pillow'
    ],
    extras_require={
        'testing': [
            'pytest',
            'flake8',
        ]
    },
    entry_points={
        'console_scripts': [
            'fotogrid=fotogrid.shell:main'
        ]
    },
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3 :: Only'
    ],
)
