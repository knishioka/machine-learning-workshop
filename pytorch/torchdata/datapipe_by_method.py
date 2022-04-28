from operator import itemgetter

from torchdata.datapipes.iter import IterableWrapper, MapKeyZipper
from torchdata.datapipes.map import SequenceWrapper


def merge_fn(tuple_from_iter, value_from_map):
    return tuple_from_iter[0], tuple_from_iter[1] + value_from_map


if __name__ == "__main__":
    dp1 = IterableWrapper([("a", 1), ("b", 2), ("c", 3)])
    mapdp = SequenceWrapper({"a": 100, "b": 200, "c": 300, "d": 400})
    res_dp = dp1.zip_with_map(
        map_datapipe=mapdp, key_fn=itemgetter(0), merge_fn=merge_fn
    )
    print(
        list(
            MapKeyZipper(
                source_iterdatapipe=dp1,
                map_datapipe=mapdp,
                key_fn=itemgetter(0),
                merge_fn=merge_fn,
            )
        )
    )
