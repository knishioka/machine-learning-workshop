import argparse
import os

import joblib
import pandas as pd
from sklearn import tree

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_leaf_nodes", type=int, default=-1)
    args = parser.parse_args()
    channel_train = os.environ["SM_CHANNEL_TRAIN"]  # channelをtrainにしておく必要がある
    model_dir = os.environ["SM_MODEL_DIR"]

    # /opt/ml/input/data/train　以下にあるデータを取得
    print(channel_train)
    input_files = [
        os.path.join(channel_train, file) for file in os.listdir(channel_train)
    ]
    if len(input_files) == 0:
        raise ValueError(f"There are no files in {args.train}.\n")
    raw_data = [pd.read_csv(file, header=None, engine="python") for file in input_files]
    train_data = pd.concat(raw_data)

    # ラベルは最初のカラム
    train_y = train_data.iloc[:, 0]
    train_X = train_data.iloc[:, 1:]

    # scikit-learnのdecision　treeにハイパーパラメータを渡して学習
    max_leaf_nodes = args.max_leaf_nodes
    clf = tree.DecisionTreeClassifier(max_leaf_nodes=max_leaf_nodes)
    clf = clf.fit(train_X, train_y)

    # 学習済みモデルを /opt/ml/modelの下にdump
    joblib.dump(clf, os.path.join(model_dir, "model.joblib"))


def model_fn(model_dir):
    """学習済みモデル読み込む."""
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf
