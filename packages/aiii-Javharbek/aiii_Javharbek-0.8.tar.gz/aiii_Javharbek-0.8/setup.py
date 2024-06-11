from setuptools import setup, find_packages

setup(
    name='aiii_Javharbek',
    version='0.8',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        'scipy',
        'matplotlib',
        'tensorflow'
        'keras',
        'imgaug',
        'scikit-learn'
    ],
    author='Javharbek',
    author_email='jakharbek@gmail.com',
    description='AIII',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
