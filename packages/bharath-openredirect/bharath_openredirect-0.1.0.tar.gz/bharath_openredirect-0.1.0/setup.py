from setuptools import setup, find_packages

setup(
    name='bharath_openredirect',  
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'openredirect=openredirect.main:main',
        ],
    },
    author='Y',
    author_email='your.email@example.com',
    description='A tool to identify potential open redirect vulnerabilities in URLs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',  # Update this URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
