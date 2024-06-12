from setuptools import setup, find_packages

setup(
    name='my_unique_ml_package',  # 패키지 이름 변경
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'run_decision_tree=my_unique_ml_package.decision_tree:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple machine learning package for decision tree classification',
    url='https://github.com/yourusername/my_unique_ml_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
