# setup.py

from setuptools import setup, find_packages

setup(
    name="hamsterkombat_clicker",
    version="0.1.0",
    description="A package to interact with the Hamster Kombat Clicker API.",
    author="Diyarbek Oralbaev",
    author_email="diyarbekdev@gmail.com",
    url="https://github.com/Diyarbekoralbaev/hamsterkombat_clicker",  # Replace with your GitHub repo URL
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
