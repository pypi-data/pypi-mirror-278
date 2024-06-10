from setuptools import setup, find_packages

from pkg_resources import parse_requirements

with open("requirements.txt", encoding="utf-8") as fp:
    install_requires = [str(requirement) for requirement in parse_requirements(fp)]

setup(
    name="vbsbox",
    version="1.0.0",
    author="Available_Kid",
    author_email="2755803649@qq.com",
    description="vbs msgbox",
    long_description="nothing to show",
    license="Apache License, Version 2.0",
    url="http://test.pypi.org/",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    include_package_data=True,  # 一般不需要
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'test = test.help:main'
        ]
    }
)
