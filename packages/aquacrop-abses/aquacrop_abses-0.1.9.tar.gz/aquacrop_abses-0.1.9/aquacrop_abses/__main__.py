#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

"""运行
"""

from typing import Optional

from abses import MainModel
from hydra import main
from omegaconf import DictConfig

from aquacrop_abses.nature import Nature


@main(version_base=None, config_path="../config", config_name="abses")
def main_model(cfg: Optional[DictConfig] = None):
    """运行模型"""
    model = MainModel(parameters=cfg, nature_class=Nature)
    model.run_model()


if __name__ == "__main__":
    main_model()
