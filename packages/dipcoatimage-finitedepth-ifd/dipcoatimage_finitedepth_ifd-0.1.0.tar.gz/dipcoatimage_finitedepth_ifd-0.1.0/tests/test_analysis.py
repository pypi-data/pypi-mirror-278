import os
import subprocess

import yaml


def test_command(finitedepth_tmp_path):
    dirname, _ = os.path.split(__file__)
    confpath = os.path.join(dirname, "config.yml")

    code = subprocess.call(
        [
            "finitedepth",
            "analyze",
            confpath,
        ],
    )
    assert not code

    with open(confpath, "r") as f:
        data = yaml.load(f, Loader=yaml.Loader)["test"]
    imgpath = os.path.expandvars(data["output"]["layerImage"])
    datapath = os.path.expandvars(data["output"]["layerData"])
    assert os.path.exists(imgpath)
    assert os.path.exists(datapath)
