from setuptools import setup, find_packages

setup(
    name="py_sat_sdk",
    packages=find_packages(),
    version="1.0.0",
    description="Python SDK for Tokopedia SAT API",
    author="SAT Team",
    install_requires=[
        "requests==2.27.1",
        "requests-oauthlib==2.0.0",
        "pycryptodome==3.11.0",
        "dataclasses==0.8",
        "dataclasses-json==0.5.9",
        "python-dateutil==2.9.0.post0",
    ],
    tests_require=[
        "pytest==4.4.1",
        "pytest-dotenv==0.5.2",
        "pytest-httpserver==1.0.5",
    ],
    test_suite="tests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
    ],
)
