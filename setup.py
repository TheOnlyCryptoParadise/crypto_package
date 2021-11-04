import setuptools
from pip._internal.req import parse_requirements
reqs = [
    "requests~=2.25.1",
    "setuptools~=49.2.1",
    "pandas"
]
setuptools.setup(
    name="crypto_package",
    version="0.0.1",
    author="Natalia Brzozowska",
    author_email="author@example.com",
    description="Cryptoparadise tools library",
    long_description="see readme.md",
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # package_dir={"": "crypto_package"},
    packages=setuptools.find_packages(),
    install_requires=reqs,
    python_requires=">=3.6",
)
