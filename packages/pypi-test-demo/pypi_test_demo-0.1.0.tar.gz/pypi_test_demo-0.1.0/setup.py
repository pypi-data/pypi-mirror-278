from setuptools import setup, find_packages

setup(
    name="pypi_test_demo",
    version="0.1.0",
    author="Muhammad Umer farooq",
    author_email="umerfarooq397@gmail.com",
    description="This is a sample package",
    # long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/my_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)