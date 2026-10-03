import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import train_test_split


def get_dataset_path():
    """Resolve dataset path with priority: CLI arg > env var > ~/ml-benchmark/creditcard.csv > ./creditcard.csv"""
    # Check CLI argument
    if len(sys.argv) > 1:
        return sys.argv[1]

    # Check environment variable
    if "CREDITCARD_CSV_PATH" in os.environ:
        return os.environ["CREDITCARD_CSV_PATH"]

    # Check ~/ml-benchmark/creditcard.csv
    default_path = os.path.expanduser("~/ml-benchmark/creditcard.csv")
    if os.path.exists(default_path):
        return default_path

    # Fallback to ./creditcard.csv
    if os.path.exists("./creditcard.csv"):
        return "./creditcard.csv"

    # If none exist, return the default path (will error on read if not found)
    return default_path


def main():
    seed = 42
    early_stopping_rounds = 50
    early_stopping_metric = "auc"
    dataset_path = get_dataset_path()

    # Load data
    started = time.perf_counter()
    df = pd.read_csv(dataset_path)
    data_load_seconds = time.perf_counter() - started

    # Separate features and target
    X, y = df.drop(columns="Class"), df["Class"]

    # Split into train/val and test (60% train, 20% val, 20% test)
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed, stratify=y,
    )
    X_train, X_valid, y_train, y_valid = train_test_split(
        X_trainval, y_trainval, test_size=0.25, random_state=seed,
        stratify=y_trainval,
    )

    # Train model with early stopping
    model = lgb.LGBMClassifier(
        n_estimators=1000, learning_rate=0.05, random_state=seed,
        n_jobs=2, verbosity=-1,
    )
    started = time.perf_counter()
    model.fit(
        X_train, y_train, eval_set=[(X_valid, y_valid)], eval_metric=early_stopping_metric,
        callbacks=[lgb.early_stopping(
            early_stopping_rounds, first_metric_only=True, verbose=False,
        )],
    )
    training_seconds = time.perf_counter() - started

    # Evaluate on test set
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    # Prepare data for inference benchmarking
    one_row = X_test.iloc[:1]
    batch = X_test.iloc[:1000]

    # Warm-up
    model.predict_proba(one_row)
    model.predict_proba(batch)

    # Measure latency: single row (200 repeats)
    latency_repeats = 200
    latency_times = []
    for _ in range(latency_repeats):
        started = time.perf_counter()
        model.predict_proba(one_row)
        latency_times.append(time.perf_counter() - started)
    latency_1_row_ms = float(np.mean(latency_times)) * 1000

    # Measure throughput: batch of 1000 rows (10 repeats)
    batch_repeats = 10
    batch_times = []
    for _ in range(batch_repeats):
        started = time.perf_counter()
        model.predict_proba(batch)
        batch_times.append(time.perf_counter() - started)
    batch_seconds = float(np.median(batch_times))
    throughput_1000_rows_per_second = len(batch) / batch_seconds

    # Compile results
    result = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "architecture": platform.machine(),
        "versions": {
            "python": platform.python_version(),
            "lightgbm": lgb.__version__,
            "sklearn": sklearn.__version__,
            "pandas": pd.__version__,
            "numpy": np.__version__,
        },
        "dataset_rows": len(df),
        "fraud_rows": int(y.sum()),
        "seed": seed,
        "split": {
            "train": len(X_train),
            "validation": len(X_valid),
            "test": len(X_test),
        },
        "n_jobs": 2,
        "decision_threshold": 0.5,
        "data_load_seconds": float(data_load_seconds),
        "training_seconds": float(training_seconds),
        "early_stopping_metric": early_stopping_metric,
        "early_stopping_rounds": early_stopping_rounds,
        "best_iteration": int(model.best_iteration_),
        "auc_roc": float(roc_auc_score(y_test, probabilities)),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "latency_1_row_ms": latency_1_row_ms,
        "latency_repeats": latency_repeats,
        "latency_unit": "milliseconds",
        "batch_rows": len(batch),
        "batch_repeats": batch_repeats,
        "batch_1000_rows_seconds": float(batch_seconds),
        "throughput_1000_rows_per_second": float(throughput_1000_rows_per_second),
        "timing_summary": "mean for single-row latency; median for batch throughput; warm-up excluded; predict_proba on pandas input",
    }

    # Write results to JSON
    Path("benchmark_result.json").write_text(
        json.dumps(result, indent=2, allow_nan=False), encoding="utf-8",
    )

    # Print results to terminal
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
