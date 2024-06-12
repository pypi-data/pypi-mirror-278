from setuptools import setup, find_packages

setup(
    name="secoda-airflow",
    version="0.0.18",
    description="Secoda Airflow Provider",
    author="Secoda Engineering",
    author_email="engineering@secoda.co",
    packages=find_packages(),
    install_requires=[
        "requests>=2.23.0",
        "ruff>=0.4.8",
        "apache-airflow>=2.0.0",
    ],
    entry_points={
        "apache_airflow_provider": [
            "provider_info=secoda_airflow.get_provider_info:get_provider_info"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
