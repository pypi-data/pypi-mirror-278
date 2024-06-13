from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='IntelliMaint',
    version='0.8',
    author='IPTLP0032',
    author_email='iptgithub@intellipredikt.com',
    description='A prognostics package by IPT',
    long_description=long_description, 
    long_description_content_type='text/markdown',  
    install_requires=[
        'scikit-learn', 'GPy', 'minisom', 'scipy', 'matplotlib==3.7.3', 'numpy>=1.16.1', 'mplcursors', 'fpdf2', 'tensorflow==2.12.0', 'keras==2.12.0', 'pandas', 'seaborn', 'imbalanced-learn'
    ],
    dependency_links=[
        'git+https://github.com/caisr-hh/group-anomaly-detection.git#egg=grand-0.2.0'
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'IntelliMaint.examples.data.battery_data': ['*'],
        'IntelliMaint.examples.data.bearing_data': ['*'],
        'IntelliMaint.examples.data.phm08_data.csv': ['*']
    },
    python_requires='>=3.5',   
)
