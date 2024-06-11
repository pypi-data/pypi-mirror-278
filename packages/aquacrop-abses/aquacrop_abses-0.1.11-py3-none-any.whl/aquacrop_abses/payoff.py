#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

"""计算农民的经济收益
"""
from __future__ import annotations

from typing import Dict, Optional, Union

import numpy as np
import pandas as pd

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

PriceType: TypeAlias = Union[Dict[str, float], pd.Series, float]


def calc_yield_payoff(
    crops_yield: PriceType,
    prices: PriceType,
    area: float = 1.0,
    total: bool = False,
) -> float:
    """计算农民的作物收益。"""
    # TODO 重构这个复杂的函数
    result: Union[dict, pd.Series] = {}
    if isinstance(crops_yield, float):
        if isinstance(prices, pd.Series):
            price = prices.mean()
        elif isinstance(prices, dict):
            price = np.mean(prices.values())
        else:
            price = prices
        return crops_yield * price * area if total else pd.Series({0: crops_yield})
    for crop, yield_ in crops_yield.items():
        if isinstance(prices, (dict, pd.Series)):
            price = prices.get(crop, 0.0)
        elif isinstance(prices, (float, int)):
            price = prices
        else:
            raise TypeError(f"prices should be a dict or a float, got {type(prices)}.")
        if isinstance(area, (dict, pd.Series)):
            crop_area = area.get(crop, 1.0)
        elif isinstance(area, (float, int)):
            crop_area = area
        else:
            raise TypeError(f"area should be a dict or a float, got {type(area)}.")
        result[crop] = yield_ * price * crop_area
    result = pd.Series(result, name="payoff", dtype=float)
    if total:
        return result.sum()
    return result


def calc_water_costs(q_surface: float, q_ground: float, prices: PriceType) -> float:
    """计算农民的水费。"""
    if isinstance(prices, (dict, pd.Series)):
        return -q_surface * prices["surface"] - q_ground * prices["ground"]
    if isinstance(prices, (float, int)):
        return -q_surface * prices - q_ground * prices
    raise TypeError(f"prices should be a dict or a float, got {type(prices)}.")


def economic_payoff(
    q_surface: float,  # mm
    q_ground: float,  # mm
    water_prices: PriceType,  # RMB/m3
    crop_yield: Optional[pd.Series] = None,  # t/ha
    crop_prices: Optional[PriceType] = None,  # RMB/t
    area: float = 1.0,  # ha
) -> float:
    """计算农民的经济收益。"""
    q_surface = q_surface * area * 10  # mm -> m3
    q_ground = q_ground * area * 10  # mm -> m3
    costs = calc_water_costs(q_surface, q_ground, water_prices)
    if crop_yield is None:
        return round(costs, 2)
    if crop_prices is None:
        crop_prices = {}
    payoff = calc_yield_payoff(crop_yield, crop_prices, area, total=True)
    return round(payoff + costs, 2)
