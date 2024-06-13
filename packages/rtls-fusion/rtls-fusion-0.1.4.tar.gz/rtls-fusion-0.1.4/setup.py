from setuptools import setup, find_packages

setup(
    name='rtls-fusion',
    version='0.1.4',
    description='A Python library for location tracking sensor data fusion',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "numpy",
    ],
    author='Ayenew Demeke',
    author_email='ayennew@gmail.com',
    url='https://github.com/ayenewdemeke/rtls-fusion',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.6',
)