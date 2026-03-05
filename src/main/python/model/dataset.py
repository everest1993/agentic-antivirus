"""
Modulo di pulizia del dataset
"""
from pathlib import Path

import pandas as pd
import tensorflow as tf


# dataset EMBER
DATA_DIR = Path(__file__).resolve().parent / "parquet"
TRAIN_PARQUET = DATA_DIR / "train_ember_2018_v2_features.parquet"
TEST_PARQUET = DATA_DIR / "test_ember_2018_v2_features.parquet"


def _load_dataframe(parquet_path: Path) -> pd.DataFrame:
    if not parquet_path.exists():
        raise FileNotFoundError(f"Dataset non trovato: {parquet_path}")

    return pd.read_parquet(parquet_path)


def _get_arrays():
    train_df = _load_dataframe(TRAIN_PARQUET)
    test_df = _load_dataframe(TEST_PARQUET)

    train_df = train_df.dropna()
    train_df = train_df[train_df["Label"] != -1.0]

    X_train = train_df.drop(columns=["Label"]).to_numpy(dtype="float32")
    y_train = train_df["Label"].to_numpy(dtype="float32")

    X_test = test_df.drop(columns=["Label"]).to_numpy(dtype="float32")
    y_test = test_df["Label"].to_numpy(dtype="float32")

    return X_train, y_train, X_test, y_test


def split_dataset():
    X_train, y_train, X_test, y_test = _get_arrays()
    train_ds, val_ds = tf.keras.utils.split_dataset(
        (X_train, y_train), left_size=0.8, shuffle=True, seed=42
    )

    return train_ds, val_ds, X_test, y_test


def get_input_shape():
    """
    Calcola la shape dei set per il layer di input del modello
    """
    X_train, _, _, _ = _get_arrays()
    return X_train.shape[1]