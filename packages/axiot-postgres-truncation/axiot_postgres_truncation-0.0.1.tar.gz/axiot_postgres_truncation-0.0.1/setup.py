from setuptools import setup, find_packages

setup(
    name="axiot_postgres_truncation",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        # list your dependencies here, e.g.,
        # 'numpy', 'requests',
        "flask", "pymongo"
    ],
    entry_points={
        'console_scripts': [
            'axiot_postgres_truncation=backend.main:__name__',  # If you have a main function to run
        ],
    },
    author="Arjun Sigadam",
    author_email="arjun@pseudocode.co",
    description="Truncating the Data stored in Postgres DB and moving into history for Performance Improvement",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    giturl="https://PITPL@dev.azure.com/PITPL/AXIoT-Product-PSEUDOCODE/_git/axiot_postgres_truncation",
    url="https://dev.azure.com/PITPL/AXIoT-Product-PSEUDOCODE/_git/axiot_postgres_truncation",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0, <4',
)
