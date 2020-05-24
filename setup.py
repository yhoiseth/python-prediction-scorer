import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    author="Yngve Hoiseth",
    author_email="yngve@hoiseth.net",
    description="Python library to score predictions",
    include_package_data=True,
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="predictionscorer",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    url="https://github.com/yhoiseth/python-prediction-scorer",
    version="0.3.0",
    zip_safe=False,
)
