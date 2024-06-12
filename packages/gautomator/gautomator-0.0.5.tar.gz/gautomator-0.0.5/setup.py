from setuptools import setup, find_packages

setup(
    name='gautomator',
    version='0.0.5',
    packages=find_packages(),
    description='Automation framework developed by Dale',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dale Hoang',
    author_email='huy.quochoang2308@gmail.com',
    install_requires=[
    "requests>=2.31",
    "colorlog>=6.7",
    "pydantic>=2.4.2",
    "behave>=1.2.6",
    "requests-to-curl>=1.1",
    "mysql-connector-python>=8.0.30",
    "pymongo>=4.2.0",
    "redis>=4.3.4",
    "psycopg2-binary>=2.9.7",
    "locust>=2.16.1",
    "python-gitlab>=3.15.0",
    "webdriver_manager>=4.0.1",
    "selenium>=4.4.3",
    "Appium-Python-Client>=2.9.0",
    "dataclasses-json>=0.6.2",
    "Faker==19.6.2",
    "TestLink-API-Python-client>=0.8.1",
    "getgauge>=0.4.0"
    ],
    python_requires='>=3.10',
)
