import setuptools

setuptools.setup(
    name="thingspire-datasets",
    version="0.1.6",
    author="Inho Kim",
    author_email="inho@thingspire.com",
    description="thingspire feature package",
    long_description="A package that collects and processes weather and "
                     "special day information by local government and "
                     "applies it to various projects",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['Bottleneck', 'numpy', 'pandas', 'requests', 'aiohttp'],
    keywords=['thingspire', 'thingspire'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)