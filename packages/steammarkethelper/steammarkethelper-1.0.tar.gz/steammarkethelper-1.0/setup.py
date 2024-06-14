from setuptools import setup, find_packages

setup(
    name='steammarkethelper',
    author="Vadim Sosnin",
    author_email="VadimSosnin02@yandex.ru",
    version='1.0',
    description="A helper tool for Steam Market that enables users to generate detailed tables from their Steam Market transaction history, making it easier to track and analyze their market activity.",
    url="https://github.com/Zavintyshka/SteamMarketHelper",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "annotated-types",
        "beautifulsoup4",
        "certifi",
        "charset-normalizer",
        "click",
        "idna",
        "lxml",
        "prettytable",
        "pydantic",
        "pydantic_core",
        "pydantic-settings",
        "python-dotenv",
        "requests",
        "soupsieve",
        "typing_extensions",
        "urllib3",
        "wcwidth",
    ],
    entry_points={
        'console_scripts': [
            'smh=steam_market_helper.smh:smh_commands'
        ],
    },
)
