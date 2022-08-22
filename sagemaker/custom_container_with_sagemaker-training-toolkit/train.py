import os
import argparse

from sklearn import tree


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--max_leaf_nodes", type=int, default=-1)


def model_fn(model_dir):
    pass
