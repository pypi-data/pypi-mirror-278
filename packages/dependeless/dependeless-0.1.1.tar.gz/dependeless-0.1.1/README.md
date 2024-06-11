# Dependeless

A very small command line tool to list all the installed pip packages that are not dependencies of any other package.  

Uses the `Required-By` field in the output of `pip show` to determine dependencies.

## Installation

```bash
pip install dependeless
```

## Usage

Easiest is to just run the command in your virtualenvironment:
```bash
dependeless
```

You can also run it with manually specified pip path:
```bash
dependeless --pip-path /path/to/pip
```

By the `pip` package and `dependeless` package itself are excluded from the output. You can change this or add more packages to exclude by using the `--pardon` option:
```bash
dependeless --pardon "pip, setuptools, your_package"
```

## Performance
For large projects with many dependencies, the tool can be slow.