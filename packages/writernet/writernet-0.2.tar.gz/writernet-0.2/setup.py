# setup.py

from setuptools import setup, find_packages

setup(
    name='writernet',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyautogui',
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'writernet=writernet.app:main',
        ],
    },
    author='Abdulfarith',
    author_email='abdullfarith@gmail.com',
    description='A package for automated typing and taking screenshots',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
