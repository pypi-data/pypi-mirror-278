from setuptools import setup, find_packages

setup(
    name='web_monitor_aiven',
    version='0.1.1',
    description='A scalable web monitor application for Aiven Kafka',
    packages=find_packages(),
    install_requires=[
        'requests',
        'kafka-python',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'web_monitor_aiven=web_monitor.__main__:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
