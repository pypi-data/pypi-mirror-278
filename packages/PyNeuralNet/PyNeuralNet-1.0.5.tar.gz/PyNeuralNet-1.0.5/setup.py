from setuptools import setup, find_packages

with open("README.md", "r") as r:
    desc = r.read()

with open("LICENSE", "r") as l:
    lice = l.read()

description = 'PyNeuralNet is a python library for prototyping and building neural networks. PyNeuralNet uses PyTorch as a computational backend for deep learning models.'

setup(
    name='PyNeuralNet',
    version='1.0.5',
    author='ItzLoghotXD',
    author_email='loghot.gamerz.official@gmail.com',
    maintainer='ItzLoghotXD',
    maintainer_email='loghot.gamerz.official@gmail.com',
    description=description,
    long_description=desc,
    long_description_content_type="text/markdown",
    license=lice,
    packages=find_packages(),
    install_requires=[
        'torch==2.1.1',
        'torchvision==0.16.1',
        'matplotlib==3.8.3',
        'pillow==10.1.0'
    ],
    entry_points={
        'console_scripts': [
            'pyneuralnet-train-image = pyneuralnet.images:train.py',
        ],
    },
    url='https://github.com/ItzLoghotXD/PyNeuralNet/',
    download_url='https://pypi.org/project/PyNeuralNet/',
    keywords=['neural', 'network', 'ai', 'neural network', 'algorithm', 'loghot'],
    
)
