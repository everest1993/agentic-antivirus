import pandas as pd


train_df = pd.read_parquet("agentic-antivirus/src/data/archive/train_ember_2018_v2_features.parquet")
test_df = pd.read_parquet("/Users/luigivannozzi/Agentic Antivirus/agentic-antivirus/src/data/archive/test_ember_2018_v2_features.parquet")

print(train_df.head())
print(train_df.info())