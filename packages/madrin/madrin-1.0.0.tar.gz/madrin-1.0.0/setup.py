from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="madrin",
    version="1.0.0",
    description="A Neural Network Library",
    packages=find_packages(),
    install_requires=['numpy'],
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/manohar3000/Madrin-A_Neural_Network_Library",
    author="Manohar",
    author_email="manohargehlot3000@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
    ],
)