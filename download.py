from pathlib import Path

import kagglehub

data_dir = Path(__file__).resolve().parent / "data" / "raw"

path = kagglehub.dataset_download(
    "retailrocket/ecommerce-dataset",
    output_dir=str(data_dir),
)

print("Данные сохранены в:", path)