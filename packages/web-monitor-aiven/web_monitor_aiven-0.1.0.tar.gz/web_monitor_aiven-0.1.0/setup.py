from setuptools import setup, find_packages

setup(
    name='web_monitor_aiven',
    version='0.1.0',
    description='A scalable web monitor application for Aiven Kafka',
    packages=find_packages(),
    install_requires=[
        'requests',
        'kafka-python',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'web_monitor = web_monitor.__main__:main'
        ]
    },
)
