from setuptools import setup, find_packages

setup(
    name='apiAmoCRM',
    version='0.1.22',
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author='wlovem',
    author_email='wlovemrock@gmail.com',
    description='Api for amoCRM',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cheboxarov/DialogServicesWidgets.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
)
