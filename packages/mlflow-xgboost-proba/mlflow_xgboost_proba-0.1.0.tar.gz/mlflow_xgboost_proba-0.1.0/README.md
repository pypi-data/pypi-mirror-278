# mlflow-xgboost-proba

[![Release](https://img.shields.io/github/v/release/sergray/mlflow-xgboost-proba)](https://img.shields.io/github/v/release/sergray/mlflow-xgboost-proba)
[![Build status](https://img.shields.io/github/actions/workflow/status/sergray/mlflow-xgboost-proba/main.yml?branch=main)](https://github.com/sergray/mlflow-xgboost-proba/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/sergray/mlflow-xgboost-proba/branch/main/graph/badge.svg)](https://codecov.io/gh/sergray/mlflow-xgboost-proba)
[![Commit activity](https://img.shields.io/github/commit-activity/m/sergray/mlflow-xgboost-proba)](https://img.shields.io/github/commit-activity/m/sergray/mlflow-xgboost-proba)
[![License](https://img.shields.io/github/license/sergray/mlflow-xgboost-proba?cacheSeconds=600)](https://img.shields.io/github/license/sergray/mlflow-xgboost-proba?cacheSeconds=600)

MLflow XGBoost flavour with probabilities

This package implements `mlflow_xgboost_proba` MLflow flavour, which allows to run `predict_proba` method of `xgboost` models during inference with MLflow `mlflow models serve` CLI command.

Implementation is based on [mlflow.xgboost](https://github.com/mlflow/mlflow/blob/master/mlflow/xgboost/__init__.py) module, which is copied and modified to have the wrapper with `predict_proba` method and `predict` method calling `predict_proba` by default.

The API of the module is identical to [mlflow.xgboost](https://mlflow.org/docs/latest/python_api/mlflow.xgboost.html), only without support of autologging.

- **Github repository**: <https://github.com/sergray/mlflow-xgboost-proba/>

## Getting started with your project

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:sergray/mlflow-xgboost-proba.git
git push -u origin main
```

Finally, install the environment and the pre-commit hooks with

```bash
make install
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

## Releasing a new version

- Create an API Token on [Pypi](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/sergray/mlflow-xgboost-proba/settings/secrets/actions/new).
- Create a [new release](https://github.com/sergray/mlflow-xgboost-proba/releases/new) on Github.
- Create a new tag in the form `*.*.*`.

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
