import pandas as pd
import tensorflow as tf


train_df = pd.read_parquet("agentic-antivirus/src/main/python/model/parquet/train_ember_2018_v2_features.parquet")
test_df = pd.read_parquet("/Users/luigivannozzi/Agentic Antivirus/agentic-antivirus/src/main/python/model/parquet/test_ember_2018_v2_features.parquet")

# esplorazione dataset
print(train_df.info())
print(test_df.info())
print(f"Train labels: {train_df['Label'].unique().tolist()}")
print(f"Test labels: {test_df['Label'].unique().tolist()}")
print(train_df.head())

# pulizia dataset
train_df = train_df.dropna()
train_df = train_df[train_df["Label"] != -1.0]

print(f"Cleaned train labels: {train_df['Label'].unique().tolist()}")

X = train_df.drop(columns=["Label"]).to_numpy(dtype="float32")
y = train_df["Label"].to_numpy(dtype="float32")


# generazioine sets
def split_dataset():
    train_ds, val_ds = tf.keras.utils.split_dataset(
        (X, y), left_size=0.8, shuffle=True, seed=42
    )

    X_test = test_df.drop(columns=["Label"]).to_numpy(dtype="float32")
    y_test = test_df["Label"].to_numpy(dtype="float32")
    
    return train_ds, val_ds, X_test, y_test


def get_input_shape():
    return X.shape[1]