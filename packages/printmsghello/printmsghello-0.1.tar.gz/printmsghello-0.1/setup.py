import setuptools


setuptools.setup(
    name="printmsghello",
    version="0.1",
    author="muneeb",
    author_email="muneeb@example.com",
    description="A simple package",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['libhello.so']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
