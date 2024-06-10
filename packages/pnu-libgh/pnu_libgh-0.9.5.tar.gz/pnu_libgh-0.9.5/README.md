[![PyPI package](https://repology.org/badge/version-for-repo/pypi/python:pnu-libgh.svg)](https://repology.org/project/python:pnu-libgh/versions)
[![Servier Inspired](https://raw.githubusercontent.com/servierhub/.github/main/badges/inspired.svg)](https://github.com/ServierHub/)

# libGH(1), libGH(3) - GitHub scraping tool and library

This repository includes a command-line utility:
* [libgh(1)](https://github.com/HubTou/libgh/blob/main/LIBGH.1.md) - GitHub scraping tool
  (returning data as [text](https://www.frbsd.org/xch/libgh.txt),
  [JSON](https://www.frbsd.org/xch/libgh.json)
  or [XML](https://www.frbsd.org/xch/libgh.xml))

And a Python library:
* [libgh(3)](https://github.com/HubTou/libgh/blob/main/LIBGH.3.md) - GitHub scraping library
  (returning data as a [Python dictionary](https://www.frbsd.org/xch/libgh.txt))

This software will scrap either personal or organizational accounts, or repositories.
You can [check which data you can get here](https://github.com/HubTou/libgh/blob/main/FIELDS.md).

Feel free to [discuss your needs and use cases there](https://github.com/HubTou/libgh/discussions).

# Installation
Once you have installed [Python](https://www.python.org/downloads/) and its packages manager [pip](https://pip.pypa.io/en/stable/installation/),
use one of the following commands, depending on if you want only this tool, the full set of PNU tools, or PNU plus a selection of additional third-parties tools:

```
pip install pnu-libgh
pip install PNU
pip install pytnix
```
