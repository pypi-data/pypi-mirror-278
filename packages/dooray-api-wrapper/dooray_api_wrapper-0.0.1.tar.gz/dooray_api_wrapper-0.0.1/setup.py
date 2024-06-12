from setuptools import setup, find_packages


setup(
    name="dooray-api-wrapper",
    version="0.0.1",
    description="Wrapper of NHN Dooray API",
    author="jooss287",
    author_email="jooss287@gmail.com",
    url="https://github.com/Jooss287/dooray-api-wrapper",
    install_requires=["pydantic", "requests", "python-dotenv"],
    packages=find_packages(),
    keywords=["dooray", "api", "nhn"],
    python_requires=">=3.6",
    package_data={},
    zip_safe=False,
)
