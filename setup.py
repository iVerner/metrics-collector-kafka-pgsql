import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metrics_collector_kafka_pgsql",
    version="0.0.6",
    author="Ignat Kudryavtsev",
    author_email="ignat@ignat.tel",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iVerner/metrics-collector-kafka-pgsql",
    package_dir={'': 'src'},
    packages=["metrics_collector_kafka_pgsql"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    install_requires=[
        "kafka-python",
        "psycopg2 >= 2.0.0",
        "psutil",
    ],

    entry_points={
        'console_scripts': [
            'metrics_collector = metrics_collector_kafka_pgsql.__main__:main'
        ],
    }
)
