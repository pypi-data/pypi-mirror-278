# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oashya",
    version="0.0.4",
    author="runhey",
    author_email="2234044577@qq.com",
    description="OnmyojiAutoScript for YYS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/runhey/OnmyojiAutoScript",
    project_urls={
        "Bug Tracker": "https://github.com/runhey/OnmyojiAutoScript/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    include_package_data=True,
)

# 测试用的
# python -m twine upload --repository testpypi dist/* --config-file pypi.pypirc
# pypi
# python -m twine upload dist/* --config-file pypi.pypirc