import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dollar-yen",  # パッケージ名
    version="0.0.1",
    author="naoyuki murata",
    author_email="nmurata@sciencepark.co.jp",
    description="Convert dollars to yen.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spc-nmurata/dollar-yen",
    project_urls={
        "Bug Tracker": "https://github.com/spc-nmurata/dollar-yen",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),  # すべてのパッケージを自動的に検出
    python_requires=">=3.8",
    install_requires=[
        'yfinance',
        'multitasking',
    ],
    entry_points={
        'console_scripts': [
            'dollar_yen = dollar_yen.main:main'  # main.pyのmain関数をエントリーポイントに
        ]
    },
)
