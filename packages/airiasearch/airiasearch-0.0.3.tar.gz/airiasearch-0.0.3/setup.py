
from setuptools import setup, find_packages

setup(
    name="airiasearch",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        'pymilvus==2.4.3',
        'scikit-learn==1.5.0',
        'numpy==1.26.4',
        'requests==2.32.3',
        'python-decouple==3.8',
        'typing'
    ],
    entry_points={
        'console_scripts': [
            'airiasearch=airiasearch.airiasearch:main',
        ],
    },
    author="Ashutosh Renu",
    author_email="ashutosh@airia.in",
    description="airiasearch is a powerful tool designed by team AIRIA that utilizes airiadb to deliver intent-based search capabilities. By interpreting the underlying intent behind user queries, airiasearch provides more accurate and relevant search results, enhancing the efficiency and effectiveness of information retrieval.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/airia-in/airiasearch.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)