from typing import Iterator, Union, Tuple

import torchdata.datapipes as dp
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

FOLDER = "data"
datapipe = dp.iter.FileLister([FOLDER]).filter(
    filter_fn=lambda filename: filename.endswith(".csv")
)
datapipe = dp.iter.FileOpener(datapipe, mode="rt")
datapipe = datapipe.parse_csv(delimiter=",")

for idx, d in enumerate(datapipe):
    print(idx, d)
