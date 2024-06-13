# -*- encoding: utf-8 -*-
# Source: https://packaging.python.org/guides/distributing-packages-using-setuptools/

import io
import re

from setuptools import find_packages, setup

dev_requirements = [
    "flake8",
    "pytest",
]
unit_test_requirements = [
    "pytest",
]
integration_test_requirements = [
    "pytest",
]
run_requirements = [
    "argparse>=1.4.0",
    "urllib3>=2.2.1",
    "requests>=2.31.0",
    "playwright>=1.42.0",
    "survey>=5.3.0",
    "tabulate>=0.9.0"
]

with io.open("./oas_mini/__init__.py", encoding="utf8") as version_f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

with io.open("README.md", encoding="utf8") as readme:
    long_description = readme.read()

setup(
    name="oas_mini",
    version=version,
    author="Banco do Brasil S.A.",
    author_email="rodrigo.siqueira@bb.com.br",
    packages=find_packages(exclude="tests"),
    include_package_data=True,
    url="https://fontes.intranet.bb.com.br/oas/oas-mini",
    license="COPYRIGHT",
    description="Adicione uma descricao para o seu projeto",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    install_requires=run_requirements,
    extras_require={
         "dev": dev_requirements,
         "unit": unit_test_requirements,
         "integration": integration_test_requirements,
    },
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6"
    ],
    keywords=(),
    entry_points={
        "console_scripts": [
            "oas_mini = oas_mini.__main__:facade"
        ],
    },
)
