import setuptools
from pip._internal.req import parse_requirements
reqs = [
    "requests~=2.25.1",
    "setuptools~=49.2.1",
    "pandas",
    "boto3==1.20.5",
    "grpcio==1.41.0",
    "mariadb==1.0.8",
    "pandas==1.3.4",
    "pika==1.2.0",
    "protobuf==3.19.1",
    "pydantic==1.8.2",
    "python-dotenv==0.19.2",
    "PyYAML==6.0",
    "requests==2.25.1",
    "setuptools==49.2.1",
    "TA_Lib==0.4.21",
    "technical==1.3.0",
    "tenacity==8.0.1"
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
