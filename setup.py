from setuptools import setup, find_packages

setup(
    name='trend_lens',
    version='0.0.0.1',
    description='A library that identified the Candlistic pattern',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Mahesh Kumar',
    author_email='maheshrajbhar90@gmail.com',
    # url='https://github.com/maheshrajbhar90/smartapi-login.git',
    packages=find_packages(),
    
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=2.0.0',
        ],
    
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    
    python_requires='>=3.6',
    include_package_data=True,
    
    entry_points={
    "console_scripts": [
        "trend_lens=main:TechnicalAnalysis", ],
    },

)