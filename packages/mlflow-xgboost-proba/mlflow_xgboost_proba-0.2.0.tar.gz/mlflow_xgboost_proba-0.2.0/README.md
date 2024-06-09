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

## Usage

Install package with `pip install mlflow-xgboost-proba`.

Prepare XGBoost model and save as MLflow model:

```python
from xgboost import XGBClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

import mlflow_xgboost_proba

# Prepare training dataset
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data["data"], data["target"], test_size=0.2)
# Prepare XGBoost model
xgb_model = XGBClassifier(n_estimators=2, max_depth=2, learning_rate=1, objective="binary:logistic")
xgb_model.fit(X_train, y_train)
# Save XGBoost model as MLflow model
mlflow_xgboost_proba.save_model(xgb_model, "mlflow_xgb_iris_classifier")
```

Run model inference with the probabilities using MLflow:

```shell
mlflow models serve --model-uri mlflow_xgb_iris_classifier --env-manager local
```

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
