#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

"""
这个脚本定义了农民类。

农民应该根据当前的可用水量，选择自己的灌溉策略。
"""

from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union, overload

import numpy as np
import pandas as pd
import xarray as xr
from abses import Actor
from aquacrop import AquaCropModel, Crop, FieldMngt, IrrigationManagement, Soil
from loguru import logger
from sko.GA import GA

from aquacrop_abses.cell import DT_PATTERN
from aquacrop_abses.load_datasets import convert_to_dataframe
from aquacrop_abses.payoff import PriceType, economic_payoff

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias


DY = "Dry yield (tonne/ha)"
FY = "Fresh yield (tonne/ha)"
YP = "Yield potential (tonne/ha)"
IRR = "Seasonal irrigation (mm)"

YieldItem: TypeAlias = Literal[
    "dry_yield",
    "fresh_yield",
    "yield_potential",
]


class Farmer(Actor):
    """
    可以选择自己灌溉策的农民行动者。。

    Irrigation management parameters are selected by creating an `IrrigationManagement` object.
    With this class we can specify a range of different irrigation management strategies.
    The 6 different strategies can be selected using the `IrrMethod` argument:

    - `IrrMethod=0`: Rainfed (no irrigation)
    - `IrrMethod=1`: Irrigation if soil water content drops below a specified threshold.
    Four thresholds representing four major crop growth stages
    (emergence, canopy growth, max canopy, senescence).
    - `IrrMethod=2`: Irrigation in every N days
    - `IrrMethod=3`: Predefined irrigation schedule
    - `IrrMethod=4`: Net irrigation
    (maintain a soil-water level by topping up all compartments daily)
    - `IrrMethod=5`: Constant depth applied each day

    预测得到的结果包括：
    - fy: "Fresh yield (tonne/ha)"
    - dy: "Dry yield (tonne/ha)"
    - yp: "Yield potential (tonne/ha)"
    - irr: "Seasonal irrigation (mm)"
    """

    irr_methods = {
        0: "Rainfed",
        1: "Soil Moisture Targets",
        2: "Set Time Interval",
        3: "Predefined Schedule",
        4: "Net Irrigation",
        5: "Constant Depth",
    }

    def __init__(self, *args, single: bool = False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # 只有一个作物的情况
        self._single_crop = single
        # 灌溉策略
        self.irr_method: int = self.p.get("irr_method", 0)
        # 当前年份的产量估算结果
        self._results: pd.DataFrame = pd.DataFrame()

    def __repr__(self) -> str:
        irr: str = self.irr_methods[self.irr_method]
        return f"<{self.unique_id} [{irr}]>"

    @property
    def crop_here(self) -> Crop | List[Crop]:
        """当前地块上的作物"""
        crops = self.get("crops")
        return crops[0] if self._single_crop else crops

    @property
    def irr_method(self) -> int:
        """灌溉策略"""
        return self._irr_method

    @irr_method.setter
    def irr_method(self, value: int) -> None:
        if value not in self.irr_methods:
            raise ValueError(f"Invalid value for irr_method: {value}.")
        self._irr_method = value

    @property
    def field_management(self) -> FieldMngt:
        """当前的田间管理策略"""
        return FieldMngt(**self.p.get("FieldMngt", {}))

    @property
    def dry_yield(self) -> pd.Series | float:
        """当前年份的干产量"""
        return self._results.get(DY)

    @property
    def fresh_yield(self) -> pd.Series | float:
        """当前年份的湿产量"""
        return self._results.get(FY)

    @property
    def yield_potential(self) -> pd.Series | float:
        """当前年份的潜在产量"""
        return self._results.get(YP)

    @property
    def seasonal_irrigation(self) -> pd.Series | float:
        """当前年份的灌溉量"""
        if self._single_crop:
            return self._results.get(IRR)
        return self._results[IRR].sum()

    def irr_management(self, **kwargs) -> IrrigationManagement:
        """当前的灌溉管理策略。"""
        params = self.p.get("IrrigationManagement", {})
        params.update(kwargs)
        return IrrigationManagement(irrigation_method=self.irr_method, **params)

    def optimize_smt(
        self,
        weather_df: pd.DataFrame,
        size_pop: int = 50,
        max_iter: int = 50,
        prob_mut: float = 0.001,
        **kwargs,
    ) -> pd.DataFrame:
        """以土壤水为目标，优化灌溉管理策略。
        使用该方法后，将会更新 `irr_method` 属性为 1。
        即分别设置四个阶段的土壤水量目标，每个阶段都是 0-100% 的浮点数。

        Parameters:
            weather_df:
                包含气象数据的 DataFrame。
            size_pop:
                种群大小。
            max_iter:
                最大迭代次数。
            prob_mut:
                变异概率。
            **kwargs:
                用来覆盖默认灌溉管理措施参数的关键字参数。

        Returns:
            优化后灌溉策略的产量数据。
        """
        self.irr_method = 1

        def fitness(smts: np.ndarray) -> float:
            reward = self.simulate(
                weather_df, is_test=True, SMT=smts.tolist(), **kwargs
            )
            return 0 - reward

        ga = GA(
            func=fitness,
            n_dim=4,
            size_pop=size_pop,
            max_iter=max_iter,
            prob_mut=prob_mut,
            lb=[0, 0, 0, 0],
            ub=[100, 100, 100, 100],
            precision=10.0,
        )
        best_x, best_y = ga.run()
        logger.debug(f"Best SMT: {best_x}, Reward: {0 - best_y}")
        return self.simulate(weather_df, SMT=best_x.tolist(), **kwargs)

    def water_withdraw(
        self,
        ufunc: Optional[Callable] = None,
        total_irrigation: Optional[float] = None,
        surface_boundaries: Optional[Tuple[float, float]] = None,
        crop_yield: YieldItem | PriceType = "dry_yield",
        ga_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Tuple[float, float]:
        """估算取水方式。

        通过遗传算法优化表面水和地下水的取水量。
        用户可以自定义收益函数，这个收益函数需允许接受以下三个参数：
        - crop_yield: 作物产量，是一个 Series，分别是不同类型作物的产量。
        - q_surface: 表面水取水量，是一个浮点数。
        - q_ground: 地下水取水量，是一个浮点数。

        如果用户不输入自定义函数，优化的目标是最大化经济收益。
        需要输入一个 water_prices 的参数，这个参数是一个字典，包含两个键值对：
        - "surface": 表面水价格。
        - "ground": 地下水价格。

        Parameters:
            ufunc:
                自定义的收益函数。
            surface_lb:
                表面水取水量的下限。
            yield_col:
                作物产量的列名。
            ga_kwargs:
                传递给遗传算法的参数。
            **kwargs:
                传递给收益函数的参数。

        Returns:
            最优的表面水和地下水取水量。

        Raises:
            ValueError:
                如果表面水取水量超出范围。
                或者没有提供自定义函数，但是缺少了 water_prices 参数。
        """
        if total_irrigation is None:
            total_irrigation = self.seasonal_irrigation
        if total_irrigation == 0.0:
            logger.warning(f"Zero irr volume for {self.unique_id}.")
            return 0.0, 0.0
        if surface_boundaries is None:
            surface_boundaries = (0.0, total_irrigation)
        surface_lb, surface_ub = surface_boundaries
        if surface_lb < 0.0 or max(surface_lb, surface_ub) > total_irrigation:
            raise ValueError(f"Invalid boundary values: {surface_boundaries}.")
        if ga_kwargs is None:
            ga_kwargs = {}
        if ufunc is None:
            if "water_prices" not in kwargs:
                raise ValueError(
                    "No custom function provided, calculating water costs."
                    "However, Missing arg `water_prices` in kwargs."
                )
            ufunc = economic_payoff
        if isinstance(crop_yield, str):
            crop_yield = getattr(self, crop_yield)

        def fitness(q_surface: np.ndarray) -> float:
            q_surface = q_surface.item()
            q_ground = total_irrigation - q_surface
            kwargs.update(
                {
                    "crop_yield": crop_yield,
                    "q_surface": q_surface,
                    "q_ground": q_ground,
                }
            )
            return -ufunc(**kwargs)

        ga = GA(
            fitness,
            n_dim=1,
            lb=[surface_lb],
            ub=[surface_ub],
            **ga_kwargs,
        )
        best_x, _ = ga.run()
        q_surface_opt = best_x[0]
        q_ground_opt = total_irrigation - q_surface_opt
        return q_surface_opt, q_ground_opt

    @overload
    def simulate(
        self, weather_df: pd.DataFrame, is_test: bool = True, **kwargs
    ) -> float:
        ...

    @overload
    def simulate(
        self, weather_df: pd.DataFrame, is_test: bool = False, **kwargs
    ) -> pd.DataFrame:
        ...

    def simulate(
        self, weather_df: pd.DataFrame, is_test: bool = False, **kwargs
    ) -> Union[pd.DataFrame, float]:
        """模拟本地块上所有作物的生长。

        Parameters:
            weather_df:
                包含气象数据的 DataFrame。
            is_test:
                如果为 True，只返回产量数据，用来模型调优。
            **kwargs:
                用来覆盖默认灌溉管理措施参数的关键字参数。

        Returns:
            如果 `is_test` 为 True，返回产量数据。
            否则返回一个 DataFrame，包含所有作物的模拟结果。
        """
        if self._single_crop:
            res = self.simulate_once(self.crop_here, weather_df, **kwargs)
            if is_test:
                return res.get(DY)
            res["Season"] = self.time.year
            self._results = res.iloc[0, :]
        else:
            data = []
            for crop in self.crop_here:
                res = self.simulate_once(crop, weather_df, **kwargs)
                data.append(res)
            result_all = pd.concat(data)
            if is_test:
                return result_all[DY].sum()
            result_all["Season"] = self.time.year
            self._results = result_all.set_index("crop Type")
        return self._results

    def simulate_once(
        self, crop: Crop, weather_df: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        """模拟一个时间步长。
        这个时间步应该是一年，因为作物通常按年来种植。
        但是气象数据集是按日来的，而且有些作物会跨年。
        所以我们用两个自然年的数据来模拟一个作物年。
        """
        start_dt, end_dt = self.get("crops_datetime")
        model = AquaCropModel(
            sim_start_time=start_dt.strftime(DT_PATTERN),
            sim_end_time=end_dt.strftime(DT_PATTERN),
            weather_df=weather_df,  # fixed
            soil=Soil(self.get("soil")),  # fixed
            crop=crop,  # fixed
            initial_water_content=self.get("init_wc"),  # fixed?
            # 这里灌溉管理策略是可变的
            irrigation_management=self.irr_management(**kwargs),
            field_management=self.field_management,  # fixed/strategy
            groundwater=self.get("groundwater"),  # fixed
        )
        model.run_model(till_termination=True)
        return model.get_simulation_results()

    def weather_data(
        self,
        climate_ds: Dict[str, xr.DataArray],
        var_mapping: Dict[str, str],
        crops_dates_only: bool = False,
        **kwargs,
    ) -> pd.DataFrame:
        """Load data from a climate dataset."""
        df = convert_to_dataframe(
            datasets=climate_ds,
            coordinate=self.at.coordinate,
            var_mapping=var_mapping,
            **kwargs,
        )
        if crops_dates_only:
            start, end = self.get("crops_datetime")
            df = df[(df["Date"] >= start) & (df["Date"] <= end)]
        return df
