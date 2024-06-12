from setuptools import setup, find_packages
import os

def get_package_data_files(package_dir):
    paths = []
    for root, _, filenames in os.walk(package_dir):
        for filename in filenames:
            paths.append(os.path.relpath(os.path.join(root, filename), package_dir))
    return paths

setup(
    name='PyGreed',
    version='0.2',
    packages=find_packages(),
    package_data={
        'PyGreed': get_package_data_files('PyGreed')
    },
    include_package_data=True,
    install_requires=[ 'pybind11',
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'start_greed_game=PyGreed.main:start_game',
        ],
    },
    author='ANCHIT RANA',
    author_email='anchitrana4@gmail.com',
    description='A package to start the Greed game with custom user algorithms',
    long_description='',
    long_description_content_type='text/markdown',
    url='https://github.com/PHANTOM9009/GREED',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
