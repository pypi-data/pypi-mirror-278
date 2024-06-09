from setuptools import setup, find_packages

setup(
    name="out_of_domain_library",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "torch>=1.7.1",
        "torchvision>=0.8.2",
        "Pillow>=8.0.1",
        "numpy>=1.19.4",
        "scikit-learn>=0.23.2",
    ],
    author="Suraj Gautam",
    author_email="beoingsuraz3385@gmail.com",
    description="A library for out-of-domain tasks.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/suraj385/out_of_domain_library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
