import numpy as np
import torchdata.datapipes as dp
from torchdata.datapipes.iter import IterDataPipe
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe


@functional_datapipe("new_map")  # DataPipeにmapメソッドを登録
class MapperIterDataPipe(IterDataPipe):
    def __init__(self, source_dp: IterDataPipe, fn) -> None:
        super().__init__()
        self.dp = source_dp
        self.fn = fn  # 関数により変換を加える

    def __iter__(self):
        for d in self.dp:
            yield self.fn(d["data"])  # 変換を加えたあとのiteratorを作成

    def __len__(self):  # DataPipeの長さを返す
        return len(self.dp)


def decoder(x):
    return x * 2


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
    datapipe = build_datapipes()
    print(list(datapipe.new_map(fn=decoder)))
