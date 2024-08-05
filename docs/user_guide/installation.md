# Installation Guide

## Prerequisites

Before installing Orchestr8, ensure you have the following prerequisites:

- Python 3.7 or higher
- pip (Python package installer)

## Installing Orchestr8

To install the core Orchestr8 package, run:

```sh
pip install orchestr8
```

Installing Database-Specific Packages

Orchestr8 supports various databases. You can install support for a specific database as follows:

Snowflake

```sh
pip install orchestr8[snowflake]
```

Postgres

```sh
pip install orchestr8[postgres]
```

MySQL

```sh
pip install orchestr8[mysql]
```

Verifying the Installation
To verify that Orchestr8 is installed correctly, you can run:

```sh
python -m orchestr8 --version
```

Troubleshooting
If you encounter any issues during installation, please check the GitHub Issues page for solutions or to report a new issue.