# -*- coding: utf-8 -*-
import setuptools

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ZYYA_Codes",
    version="2024.6.0.1",
    author="Yitong Gong",
    author_email="yitong.gong@qq.com",
    description="Python codes for China Post Yongan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "": [
            "src/ZYYA_Codes/Web_UI/templates/*",
            "src/ZYYA_Codes/Web_UI/templates/fonts/*",
            "src/ZYYA_Codes/Web_UI/templates/html/*",
            "src/ZYYA_Codes/Web_UI/templates/img/*",
            "src/ZYYA_Codes/Web_UI/templates/js_code/*",
        ]
    },
    license="MIT License",
    install_requires=[
        "pandas",
        "numpy",
        "chinese-calendar",
        "chardet",
        "pymongo",
        "pyecharts",
        "typing",
        "pytz",
        "imapclient",
        "flask"
    ]
)
