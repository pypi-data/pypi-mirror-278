import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "dms-patterns",
    "version": "0.0.11",
    "description": "L3-level cdk constructs for DMS",
    "license": "Apache-2.0",
    "url": "https://github.com/MarcDuQuesne/dms-patterns",
    "long_description_content_type": "text/markdown",
    "author": "Matteo Giani<matteo.giani.87@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/MarcDuQuesne/dms-patterns"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "dms_patterns",
        "dms_patterns._jsii"
    ],
    "package_data": {
        "dms_patterns._jsii": [
            "dms-patterns@0.0.11.jsii.tgz"
        ],
        "dms_patterns": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.110.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.99.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
