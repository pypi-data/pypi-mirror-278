# setup.py
from setuptools import setup, find_packages

setup(
        name='folder_selector',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],
    setup_requires=['wheel'],
    description='A Tkinter-based folder selector for Python applications',
    author='Adolfo Zilli',
    author_email='info@adolfozilli.com',
    url='https://gitlab.com/adolfoweb/multiple-folder-selector',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
