import setuptools

with open("docs/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crypto_package",
    version="0.0.1",
    author="Natalia Brzozowska",
    author_email="author@example.com",
    description="Cryptoparadise tools library",
    long_description="see readme.md",
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    package_dir={"": "crypto_package"},
    packages=setuptools.find_packages(where="crypto_package"),
    python_requires=">=3.6",
)
