import os
import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="GameWorldNavigator",
    version="0.0.7.7",
    author="NanJunLYS",
    author_email="18906571516@163.com",
    description="A framework for game automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JunNanLYS/GameWorldNavigator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    requires=[],
    install_requires=[i.strip() for i in open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), encoding="utf-16").readlines() if i.strip()]
)

