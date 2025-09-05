import kagglehub
import pandas as pd
import os

path = kagglehub.dataset_download("sujalsuthar/amazon-delivery-dataset")

csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
if csv_files:
  df = pd.read_csv(os.path.join(path, csv_files[0]))
  print(f"\nDataset carregado: {csv_files[0]}")
  print(f"Shape: {df.shape}")
  print(df.head())