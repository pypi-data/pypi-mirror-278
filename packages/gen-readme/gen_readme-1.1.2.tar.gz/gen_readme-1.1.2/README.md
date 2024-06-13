<img align="right" src="https://raw.githubusercontent.com/vroncevic/gen_readme/dev/docs/gen_readme_logo.png" width="25%">

# Create README.md doc module

**gen_readme** is tool for creating README.md doc module.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![gen_readme python checker](https://github.com/vroncevic/gen_readme/actions/workflows/gen_readme_python_checker.yml/badge.svg)](https://github.com/vroncevic/gen_readme/actions/workflows/gen_readme_python_checker.yml) [![gen_readme package checker](https://github.com/vroncevic/gen_readme/actions/workflows/gen_readme_package_checker.yml/badge.svg)](https://github.com/vroncevic/gen_readme/actions/workflows/gen_readme_package.yml) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/gen_readme.svg)](https://github.com/vroncevic/gen_readme/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/gen_readme.svg)](https://github.com/vroncevic/gen_readme/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Installation](#installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [Dependencies](#dependencies)
- [Tool structure](#tool-structure)
- [Docs](#docs)
- [Contributing](#contributing)
- [Copyright and licence](#copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Installation

![debian linux os](https://raw.githubusercontent.com/vroncevic/gen_readme/dev/docs/debtux.png)

[![gen_readme python3 build](https://github.com/vroncevic/gen_readme/actions/workflows/gen_readme_python3_build.yml/badge.svg)](https://github.com/vroncevic/gen_readme/actions/workflows/gen_readme_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

Python package is located at **[pypi.org](https://pypi.org/project/gen_readme/)**.

You can install by using pip

```bash
#python3
pip3 install gen_readme
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/gen_readme/releases/)** download and extract release archive.

To install **gen_readme** type the following

```bash
tar xvzf gen_readme-x.y.z.tar.gz
cd gen_readme-x.y.z/
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build --no-isolation --wheel
pip3 install ./dist/gen_readme-*-py3-none-any.whl
rm -f get-pip.py
chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/gen_readme_run.py
ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/gen_readme_run.py /usr/local/bin/gen_readme_run.py
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/gen_readme/releases)** download and extract release archive.

To install **gen_readme** locate and run setup.py, type the following

```bash
tar xvzf gen_readme-x.y.z.tar.gz
cd gen_readme-x.y.z
#python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
python3 setup.py install_data
```

##### Install using docker

You can use Dockerfile to create image/container.

### Dependencies

**gen_readme** requires next modules and libraries

- [ats-utilities - Python App/Tool/Script Utilities](https://vroncevic.github.io/ats_utilities)

### Tool structure

**gen_readme** is based on OOP

Generator structure

```bash
    gen_readme/
        ├── conf/
        │   ├── gen_readme.cfg
        │   ├── gen_readme.logo
        │   ├── gen_readme_util.cfg
        │   ├── project.yaml
        │   └── template/
        │       ├── README_AVR.template
        │       ├── README_CC.template
        │       ├── README_C.template
        │       ├── README_JS.template
        │       ├── README_PL.template
        │       ├── README_PY.template
        │       ├── README_RPI.template
        │       ├── README_SH.template
        │       ├── README_STM.template
        │       └── README_VALA.template
        ├── __init__.py
        ├── log/
        │   └── gen_readme.log
        ├── pro/
        │   ├── __init__.py
        │   ├── read_template.py
        │   └── write_template.py
        └── run/
            └── gen_readme_run.py
        
        6 directories, 20 files
```

### Docs

[![Documentation Status](https://readthedocs.org/projects/gen_readme/badge/?version=latest)](https://gen-readme.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [gen_readme.readthedocs.io](https://gen-readme.readthedocs.io)
* [www.python.org](https://www.python.org/)

### Contributing

[Contributing to gen_readme](CONTRIBUTING.md)

### Copyright and licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2020 - 2024 by [vroncevic.github.io/gen_readme](https://vroncevic.github.io/gen_readme/)

**gen_readme** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/gen_readme/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)