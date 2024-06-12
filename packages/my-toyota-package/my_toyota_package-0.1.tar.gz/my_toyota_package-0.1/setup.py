from setuptools import setup, find_packages

setup(
    name='my_toyota_package',
    version='0.1',
    packages=find_packages(),
    package_data={
        'my_toyota_package': ['data/ToyotaCorolla.csv']
    },
    include_package_data=True,
    install_requires=[
        'pandas',
        'scikit-learn',
    ],
    entry_points={
        'console_scripts': [
            'run_toyota_decision_tree=my_toyota_package.decision_tree:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A machine learning package for optimizing and training decision trees on Toyota Corolla dataset',
    url='https://github.com/yourusername/my_toyota_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
