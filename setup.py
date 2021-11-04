import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryptoparadise_lib",
    version="0.0.1",
    author="Natalia Brzozowska",
    author_email="author@example.com",
    description="Cryptoparadise tools library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # package_dir={"": "src"},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
