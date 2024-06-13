from setuptools import setup, find_packages

setup(
    name="event_subscriber",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "web3",
        "asyncio",
        "colorama",
        "pyfiglet",
        "argparse",
        "logging",
    ],
    entry_points={
        'console_scripts': [
            'event_subscriber=event_subscriber.subscriber:main',
        ],
    },
    author="Stephen Ajayi",
    author_email="5m477code@gmail.com",
    description="A tool to subscribe and handle Ethereum events",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
