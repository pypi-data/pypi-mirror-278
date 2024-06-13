import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doller-yen",  # パッケージ名を調整
    version="0.0.4",
    author="naoyuki murata",
    author_email="nmurata@sciencepark.co.jp",
    description="Convert dollars to yen.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spc-nmurata/doller_yen",
    project_urls={
        "Bug Tracker": "https://github.com/spc-nmurata/doller_yen",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "doller_yen"},
    py_modules=['doller_yen'],
    packages=setuptools.find_packages(where="doller_yen"),
    python_requires=">=3.8",
    install_requires=[
        'yfinance',  # 依存関係を追加
        'multitasking',
    ],
    entry_points = {
        'console_scripts': [
            'doller_yen = doller_yen:main'
        ]
    },
)
