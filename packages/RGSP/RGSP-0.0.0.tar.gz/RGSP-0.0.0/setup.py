from setuptools import setup, find_packages

setup(
    name='RGSP',
    version='0.0.0',
    author='Xia Jiang, Yijun Zhou',
    author_email='xij6@pitt.edu',
    description='Random Hyperparameter Search',
    packages=find_packages(),
    install_requires=[
    'scikit-learn',
    'numpy',
    'keras==2.6.0',
    'tensorflow==2.6.0',
    'pandas',
    'xgboost'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='==3.7',
)