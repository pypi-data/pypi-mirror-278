# rpmlint-codeclimate

This project provides a Python-based parser for rpmlint to write
CodeClimate-format reports, mainly to assist using rpmlint in
Gitlab CI/CD pipelines.

## Install

```shell
python -m pip install rpmlint-codeclimate
```

## Usage

Just pipe the output of `rpmlint --info` to the `rpmlint_codeclimate` module.

```shell
rpmlint --info *.rpm | python -m rpmlint_codeclimate
```
