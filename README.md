# Colvert

[![PyPI - Version](https://img.shields.io/pypi/v/colvert.svg)](https://pypi.org/project/colvert)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/colvert.svg)](https://pypi.org/project/colvert)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/colvert.svg)](https://pypi.org/project/colvert)

![Logo](colvert/ui/static/logo.png)

-----

**Table of Contents**

- [Colvert](#colvert)
  - [Charts](#charts)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Documentation](#documentation)
  - [License](#license)
  - [FAQ](#faq)
    - [What does Colvert mean?](#what-does-colvert-mean)

**THIS PROJECT IS IN EARLY DEVELOPMENT**

`colvert` is a tool for fast data exploration and visualization. Running on your machine you can explore large datasets using SQL an visualize them. AI generation of SQL queries is also supported.

`colvert` is a Frontend for DuckDB a fast and lightweight in-memory database designed for analytical queries. It's design to be a simple and easy to use tool for data analysis and visualization. 

It's a web frontend running on top of DuckDB. It's support SQL queries and visualization using Plotly. Even if it's a web frontend it's designed to be used locally on your machine like a Jupyter notebook.

It's support loading data from CSV, Parquet, JSON files and directly from Hugging Face.

Using [LiteLLM](https://github.com/BerriAI/litellm) for AI support allow usage of all 

## Charts

![Table screenshot](colvert/docs/charts/table/table.png)
![Pie chart screenshot](colvert/docs/charts/pie/pie.png)

## Installation

We recommend installing `colvert` using `pipx` or `uvx`:
```console
pipx install colvert
```

Pipx is a tool to install Python applications in isolated environments. It's a great way to install Python applications without cluttering your system Python environment.

## Usage

```console
colvert  open samples/test.csv 
```

This will detect the type of the file and open it in a new browser tab.

## Documentation

Once `colvert` is installed, you can access the documentation from the web interface. You can also access the documentation in the [documentation](colvert/docs/index.md) folder.

## License

`colvert` is distributed under the terms of the Apache 2.0 license.

## FAQ

### What does Colvert mean?

Colvert is the french name for the Mallard Duck. It's a reference to DuckDB the database engine used by Colvert and the fact the author is French and born in the region of France where Mallard Duck are important.

https://en.wikipedia.org/wiki/Mallard
