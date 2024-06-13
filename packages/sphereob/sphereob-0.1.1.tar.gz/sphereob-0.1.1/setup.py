from setuptools import setup, find_packages

setup(
    name='sphereob',
    version='0.1.1',  # Incremented version number
    author='Your Name',
    author_email='your.email@example.com',
    description='A description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/sphereob',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt5',
        'numpy',
        'matplotlib',
        'pandas',
        'qdarkstyle',
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'sphereob=sphereob.GUI.sphere_overburden_gui:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)