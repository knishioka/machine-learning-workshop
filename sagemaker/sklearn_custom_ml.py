# 参考元のスクリプトはこちら: https://github.com/aws/amazon-sagemaker-examples/blob/main/sagemaker-python-sdk/scikit_learn_iris/scikit_learn_estimator_example_with_batch_transform.ipynb
import joblib
import os
import pandas as pd
import argparse

from sklearn import tree


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # ハイパーパラメータは、argparseを使って指定できる
    parser.add_argument("--max_leaf_nodes", type=int, default=-1)

    # SageMaker独自の引数。デフォルトのものは環境変数にセットされている。
    parser.add_argument("--output-data-dir", type=str, default=os.environ["SM_OUTPUT_DATA_DIR"])
    parser.add_argument("--model-dir", type=str, default=os.environ["SM_MODEL_DIR"])
    parser.add_argument("--train", type=str, default=os.environ["SM_CHANNEL_TRAIN"])

    args = parser.parse_args()

    # 複数のファイルを取得して一つのDataFrameに格納
    input_files = [os.path.join(args.train, file) for file in os.listdir(args.train)]
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

    # 学習済みモデルを `model_dir` にdump
    joblib.dump(clf, os.path.join(args.model_dir, "model.joblib"))


def model_fn(model_dir):
    """学習済みモデル読み込む."""
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf
