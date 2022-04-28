import csv
import random

import numpy as np
import torchdata.datapipes as dp
from torch.utils.data import DataLoader


def generate_csv(file_label, num_rows: int = 5000, num_features: int = 20) -> None:
    fieldnames = ["label"] + [f"c{i}" for i in range(num_features)]
    writer = csv.DictWriter(
        open(f"sample_data{file_label}.csv", "w"), fieldnames=fieldnames
    )
    writer.writeheader()
    for i in range(num_rows):
        row_data = {col: random.random() for col in fieldnames}
        row_data["label"] = random.randint(0, 9)
        writer.writerow(row_data)


def build_datapipes(root_dir="."):
    datapipe = dp.iter.FileLister(root_dir)
    datapipe = datapipe.filter(
        filter_fn=(
            lambda filename: "sample_data" in filename and filename.endswith(".csv")
        )
    )
    datapipe = dp.iter.FileOpener(datapipe, mode="rt")
    datapipe = datapipe.parse_csv(delimiter=",", skip_lines=1)
    datapipe = datapipe.map(
        lambda row: {
            "label": np.array(row[0], np.int32),
            "data": np.array(row[1:], dtype=np.float64),
        }
    )
    return datapipe


if __name__ == "__main__":
    num_files_to_generate = 3
    for i in range(num_files_to_generate):
        generate_csv(file_label=i)
    datapipe = build_datapipes()
    dl = DataLoader(dataset=datapipe, batch_size=50, shuffle=True)
    first = next(iter(dl))
    labels, features = first["label"], first["data"]
    print(f"Labels batch shape: {labels.size()}")
    print(f"Feature batch shape: {features.size()}")
