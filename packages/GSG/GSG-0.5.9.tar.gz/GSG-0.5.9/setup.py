from setuptools import setup, find_packages
import os

setup(
    name = 'GSG',
    version='0.5.9',
    packages=find_packages(),
    python_requires='>=3.8',
    py_modules=['GSG'],
    long_description=open(os.path.join("./","README.md"), encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT Licence",
    url="https://github.com/keaml-Guan/GSG",
    install_requires=[
        'torch==1.9.0',
        'numpy==1.22.0',
        'scanpy==1.8.2',
        'anndata==0.8.0',
        'dgl==0.9.0',
        'pandas==1.2.4',
        'scipy==1.7.3',
        'scikit-learn==1.0.1',
        'tqdm==4.64.1',
        'matplotlib==3.5.3',
        'tensorboardX==2.5.1',
        'pyyaml==6.0.1',
        'plotly==5.21.0',
        'kaleido==0.2.1',
        'igraph==0.9.8',
    ]
)