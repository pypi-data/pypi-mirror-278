from setuptools import setup, find_packages

setup(
    name="forecast_order",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        'console_scripts': [
            # 'forecast-order=forecast_order.forecast_order:main', # もしCLIとして使用する場合のエントリーポイント
        ],
    },
    include_package_data=True,
    description="A package for forecasting orders using Hawk API.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Yuto Sasa",
    author_email="y_sasa@zenk.co.jp",
    url="https://github.com/zenk-github/forecast_order",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
