# -*- coding: utf-8 -*-
import imaplib
import time
import typing
import datetime
import pandas
import os
import numpy
import chardet
import email.parser
import email.header
import platform

from ZYYA_Codes.Balance_Sheet import read_balance_sheet
from ZYYA_Codes.utils import get_fridays, get_configs, decode_str
from ZYYA_Codes.market_data_api import tushare_pro_api
from ZYYA_Codes.utils.pyecharts_plot import *
from ZYYA_Codes.utils import Mongo_Client
from ZYYA_Codes.FOF_Analysis.Basic_Index import basic_index
from ZYYA_Codes.Net_Value import RiskIndex

__all__ = ["Analysis_Results", "balance_sheet_fetch", "balance_sheet_analysis", "basic_index"]

Configs = get_configs()


class balance_sheet_analysis(basic_index):
    sheets: typing.Dict[datetime.date, read_balance_sheet]

    def __init__(
            self,
            balance_sheets: typing.Union[
                typing.List[read_balance_sheet],
                typing.Dict[datetime.date, read_balance_sheet]
            ],
            **kwarg
    ):
        if isinstance(balance_sheets, list) and len(balance_sheets) > 0:
            self.sheets = {x.Date: x for x in balance_sheets}
        elif isinstance(balance_sheets, list) and len(balance_sheets) == 0:
            self.sheets = {}
        else:
            self.sheets = balance_sheets
        self.__platform = kwarg.get("platform", "")

        self.__Grade = "%s份额" % kwarg.get("Grade", "总")
        self.Client = Mongo_Client()
        self.Holdings = self.__get_everyday_holding()
        self.Holdings_Costs = self.__get_everyday_cost().sort_index()
        self.Holdings_Scales = self.__get_everyday_scale().sort_index()
        self.Holdings_Amount = self.__get_everyday_amount().sort_index()
        self.Fridays = list(set([
                                    min([y for y in self.sheets.keys() if y >= x]) for x in
                                    get_fridays(min(self.Holdings), max(self.Holdings))
                                ] if len(self.Holdings) else []))
        self.Fridays.sort()
        self.__Transaction_path = kwarg.get("Transactions", None)
        self.Transactions = self.__transactions(
            Transactions=pandas.read_excel(self.__Transaction_path)
            if self.__Transaction_path and os.path.exists(self.__Transaction_path) else None,
            name=kwarg.get("name"),
            code=kwarg.get("code")
        ) if len(self.Holdings) else None
        self.Short_Names = {
            x: self.__change_fund_name(x) for x in self.get_all_securities()
        } if len(self.Holdings) else None
        self.Strategy_File_Route: str = kwarg.get("Strategy_File_Route")
        self.Interest_Rate = self.__Interest_Rate()
        super().__init__(start=min(self.Fridays), end=max(self.Fridays))
        self.Strategy_Basic_Index = self.strategy_index(grade=kwarg.get("index_category", 2))

    def __Interest_Rate(self) -> pandas.Series:
        shibor: pandas.DataFrame = tushare_pro_api.shibor(
            start_date=min(self.Fridays).strftime("%Y%m%d"),
            end_date=max(self.Fridays).strftime("%Y%m%d"),
            fields="date,on"
        )
        shibor["date"] = [pandas.to_datetime(x).date() for x in shibor["date"]]
        return shibor.set_index("date")["on"].sort_index()

    def get_cash(self):
        return pandas.Series({x: y.Cash for x, y in self.sheets.items()}).sort_index()

    def __get_strategies(self):
        if self.__platform.lower() == "web":
            result = pandas.read_excel(self.Strategy_File_Route, index_col=0, na_filter="")
            return result["细分策略"].to_dict()
        else:
            run = True
            labels = self.Strategy_Basic_Index.columns.tolist()
            while run:
                try:
                    result = pandas.read_excel(self.Strategy_File_Route, index_col=0, na_filter="")
                    no_labels = set(self.get_all_securities()).difference(set(result.index))
                    for label in no_labels:
                        result.loc[label] = [""]
                    if len(result[result["细分策略"] == ""]) == 0:
                        for x in result.index:
                            if result["细分策略"][x] not in labels and result["细分策略"][x] != "货币基金":
                                result["细分策略"][x] = ""
                        if len(result[result["细分策略"] == ""]) == 0:
                            run = False
                            return result["细分策略"].to_dict()
                except:
                    pandas.DataFrame(
                        {"细分策略": {x: "" for x in self.get_all_securities()}}
                    ).to_excel(self.Strategy_File_Route)
                    os.system(
                        '"%s"' % self.Strategy_File_Route.replace("/", "\\")
                        if platform.platform().__contains__("Windows")
                        else 'open "%s"' % self.Strategy_File_Route
                    )
                    time.sleep(4)
                    continue
                    # raise FileNotFoundError("给定的文件不存在，系统已自动生成子基金名单，请将子基金策略标签补足")
                result.to_excel(self.Strategy_File_Route)
                os.system(
                    '"%s"' % self.Strategy_File_Route.replace("/", "\\")
                    if platform.platform().__contains__("Windows")
                    else 'open "%s"' % self.Strategy_File_Route
                )
                time.sleep(4)
                # raise ValueError("请将子基金策略标签补足")


    def get_all_securities(self) -> list:
        List = set()
        for y in self.Holdings.values():
            List = List.union(set(y.index.tolist()))
        return list(List)

    @staticmethod
    def __change_fund_name(name: str):
        if name.__contains__("基金"):
            return name.replace(
                "私募基金", ""
            ).replace(
                "私募证券投资基金", ""
            ).replace(
                "私募证券基金", ""
            )
        else:
            return name

    def __get_everyday_holding(self) -> typing.Dict[datetime.date, pandas.DataFrame]:
        return {x: y.Properties for x, y in self.sheets.items()}

    def __get_everyday_cost(self) -> pandas.DataFrame:
        return pandas.DataFrame(
            {x: y["成本-本币"].to_dict() for x, y in self.Holdings.items()}
        ).T.fillna(0)

    def __get_everyday_amount(self) -> pandas.DataFrame:
        return pandas.DataFrame(
            {x: y["数量"].to_dict() for x, y in self.Holdings.items()}
        ).T.fillna(0)

    def __get_everyday_scale(self) -> pandas.DataFrame:
        return pandas.DataFrame(
            {x: y["市值-本币"].to_dict() for x, y in self.Holdings.items()}
        ).T.fillna(0)

    def __subscribes(self) -> pandas.DataFrame:
        change = self.Holdings_Costs.diff().dropna()
        return pandas.DataFrame(
            [[y, x, -change[y][x], "申购"] for x in change.index for y in change.columns if change[y][x] > 0],
            columns=["产品名称", "日期", "发生金额", "类型"]
        )

    def __redeems(self) -> pandas.DataFrame:
        Net_Value = self.Holdings_Scales / self.Holdings_Amount
        change = self.Holdings_Amount.sort_index(ascending=False).diff().dropna(how="all")
        change = change.where(change > 0).fillna(0)
        change *= Net_Value
        change = change.rename(index={x: min([y for y in Net_Value.index if y > x]) for x in change.index}).fillna(0)
        return pandas.DataFrame(
            [[y, x, change[y][x], "赎回"] for x in change.index for y in change.columns if change[y][x] > 0],
            columns=["产品名称", "日期", "发生金额", "类型"]
        )

    def __dividends(self) -> pandas.DataFrame:
        change = pandas.DataFrame({x: y.Dividends for x, y in self.sheets.items()}).fillna(0)
        dividends = pandas.DataFrame(
            [[x, y, change[y][x], "分红"] for x in change.index for y in change.columns if change[y][x] > 0],
            columns=["产品名称", "日期", "发生金额", "类型"]
        ).sort_values(by="日期").set_index("日期").drop_duplicates().reset_index(drop=False)
        return dividends

    def __transactions_from_db(self, **kwargs) -> pandas.DataFrame:
        if kwargs.get("name") and kwargs.get("code"):
            result = pandas.DataFrame(
                [
                    x for x in self.Client["CBS数据"]["申赎记录"].find(
                    {"母基金名称": kwargs.get("name"), "母基金代码": kwargs.get("code")},
                    {"_id": 0, "母基金名称": 0, "母基金代码": 0}
                )
                ]
            )
        else:
            result = pandas.DataFrame()
        return result

    def __transactions(self, **kwargs) -> pandas.DataFrame:
        name = kwargs.get("name", None)
        code = kwargs.get("code", None)
        result = pandas.concat(
            [
                self.__subscribes(), self.__dividends(),
                self.__redeems(), kwargs.get("Transactions", None),
                self.__transactions_from_db(name=name, code=code)
            ]
        )
        result["日期"] = [pandas.to_datetime(x).date() for x in result["日期"]]
        result["发生金额"] = result["发生金额"].round(2)
        result = result[
            (result["日期"] >= min(self.Fridays)) & (result["日期"] <= max(self.Fridays))
            ].sort_values(by="日期").drop_duplicates().reset_index(drop=True)
        if name and code:
            result["母基金名称"] = name
            result["母基金代码"] = code
            datetime_result = result.copy()
            datetime_result["日期"] = [pandas.to_datetime(x) for x in datetime_result["日期"]]
            self.Client["CBS数据"]["申赎记录"].delete_many(
                {
                    "母基金名称": name,
                    "母基金代码": code,
                    "$and": [
                        {"日期": {"$gte": pandas.to_datetime(min(self.Fridays))}},
                        {"日期": {"$lte": pandas.to_datetime(max(self.Fridays))}}
                    ]
                }
            )
            if [y for y in datetime_result.T.to_dict().values()]:
                self.Client["CBS数据"]["申赎记录"].insert_many([y for y in datetime_result.T.to_dict().values()])
        result[
            [x for x in result.columns if x != "母基金名称" and x != "母基金代码"]
        ].set_index("产品名称").to_excel(self.__Transaction_path)
        result = result[(result["日期"] >= min(self.Fridays)) & (result["日期"] <= max(self.Fridays))]
        return result

    @property
    def Scale(self) -> pandas.Series:
        return pandas.Series(
            {x: y.Hierachical_Scale.get(self.__Grade, float("nan")) for x, y in self.sheets.items()}
        ).sort_index()

    @property
    def Cash(self) -> pandas.Series:
        return pandas.Series(
            {x: y.Cash for x, y in self.sheets.items()}
        ).sort_index()

    @property
    def Liability(self) -> pandas.Series:
        return pandas.Series(
            {x: y.Liability for x, y in self.sheets.items()}
        ).sort_index()

    @property
    def Tax(self) -> pandas.Series:
        return pandas.Series(
            {x: y.Tax for x, y in self.sheets.items()}
        ).replace("", 0).sort_index()

    @property
    def Net_Value(self) -> pandas.Series:
        return pandas.Series(
            {x: y.Hierachical_Net_Value.get(self.__Grade, float("nan")) for x, y in self.sheets.items()}
        ).sort_index()

    @property
    def Shares(self) -> pandas.Series:
        return pandas.Series(
            {x: y.Hierachical_Shares.get(self.__Grade, float("nan")) for x, y in self.sheets.items()}
        ).sort_index()

    @property
    def Accumulated_Value(self) -> pandas.Series:
        NV = self.Net_Value.copy()
        AV = pandas.Series(
            {x: y.Hierachical_Accumulated_Value.get(self.__Grade, float("nan")) for x, y in self.sheets.items()}
        ).sort_index()
        NV_change = NV.diff()
        NV_change_round = NV.round(4).diff().fillna(0).round(4)
        AV_change_round = AV.diff().fillna(0).round(4)
        compare: pandas.Series = NV_change_round == AV_change_round
        result = [NV[0]]
        for i in range(1, len(NV)):
            if compare[NV.index[i]]:
                result.append(result[-1] + NV_change[NV.index[i]])
            else:
                result.append(result[-1] + AV_change_round[AV.index[i]])
        return pandas.Series(result, index=NV.index).sort_index()

    @property
    def Adjusted_Value(self) -> pandas.Series:
        CNV = self.Accumulated_Value.copy()
        NV = self.Net_Value.copy()
        ANV = [1]
        for x, y in zip(NV.index[: -1], NV.index[1:]):
            ANV.append(ANV[-1] * ((CNV[y] - CNV[x]) / NV[x] + 1))
        return pandas.Series(ANV, index=NV.index).sort_index()
        # return CNV

    def Adjust_Value_without_Fee(self, **kwargs) -> pandas.Series:
        NV_Chg = self.Adjusted_Value[self.Fridays].pct_change()
        Share_Chg = self.Shares[self.Fridays].pct_change() + 1
        Tax_Influence = - self.Tax[self.Fridays].diff() / self.Scale[self.Fridays].shift()
        return numpy.exp(
            numpy.log(
                (NV_Chg +
                 kwargs.get("fee_ratio", 0.0004) / 365 * self.Holdings_Scales.loc[
                     self.Fridays].sort_index().index.diff().days
                 - Tax_Influence
                 ) * Share_Chg + 1
            ).fillna(0).sort_index().cumsum()
        )[self.Fridays].sort_index()

    # def Adjust_Value_without_Fee(self, **kwargs) -> pandas.Series:
    #     NV_Chg = self.Adjusted_Value.pct_change()
    #     Share_Chg = self.Shares.pct_change() + 1
    #     Tax_Influence = - self.Liability.diff() / self.Scale.shift()
    #     return numpy.exp(
    #         numpy.log(
    #             NV_Chg * Share_Chg + 1 - Tax_Influence
    #         ).fillna(0).sort_index().cumsum()
    #     )[self.Fridays]

    @property
    def Pct_Change(self) -> pandas.Series:
        result = self.Adjusted_Value[self.Fridays].sort_index().pct_change().fillna(0)
        result = pandas.DataFrame(result, columns=["周度涨跌幅"])
        return result["周度涨跌幅"].sort_index()

    @property
    def Net_Value_Set(self) -> pandas.DataFrame:
        return pandas.DataFrame(
            {"单位净值": self.Net_Value.round(8),
             "累计单位净值": self.Accumulated_Value.round(8),
             "复权净值（归一）": self.Adjusted_Value.round(8)
             }
        ).loc[self.Fridays].sort_index()

    @property
    def Strategy_Scale(self) -> pandas.DataFrame:
        Scales: pandas.DataFrame = self.Holdings_Scales.loc[self.Fridays]
        Strategy = pandas.Series(self.__get_strategies())
        Strategy = Strategy[[x for x in Strategy.index if x in Scales.columns.tolist()]]
        Strategy = Strategy.groupby(Strategy).agg(lambda x: ",".join(x.index).split(","))
        result = pandas.DataFrame(
            {x: Scales[Strategy[x]].T.sum().T for x in Strategy.index}
        )
        result["现金"] = (result["货币基金"] + self.get_cash()) if "货币基金" in result.columns else self.get_cash()
        result = result[[x for x in result.columns if x != "货币基金"]]
        return result.sort_index()

    @property
    def Strategy_Scale_Change(self) -> pandas.DataFrame:
        return self.Strategy_Scale.drop(columns=["现金"]).diff()

    @property
    def Strategy_Proportion(self) -> pandas.DataFrame:
        Scales = self.Strategy_Scale
        return (
                Scales.T / self.Scale
        )[self.Fridays].sort_values(by=max(self.Fridays)).T

    @property
    def Strategy_Profit(self) -> pandas.DataFrame:
        Strategy = pandas.Series(self.__get_strategies())
        Transactions = self.Transactions.copy()
        Transactions["细分策略"] = [Strategy[a] for a in Transactions["产品名称"]]
        Transactions = Transactions[Transactions["细分策略"] != "货币基金"]
        Product_Scale = self.Scale.copy()
        Scales: pandas.DataFrame = self.Strategy_Scale.copy()
        Profit = Scales.diff()
        Profit = Profit[[a for a in Profit.columns if a != "现金"]]
        for x, y, z in zip(Transactions["细分策略"], Transactions["日期"], Transactions["发生金额"]):
            if min(self.Fridays) <= y <= max(self.Fridays) and x != "货币基金":
                Profit.loc[min([a for a in self.Fridays if a >= y]), x] += z
        Profit = (Profit.T / self.Scale[self.Fridays].sort_index().shift()).T
        # for date in Profit.index[1:]:
        #     Profit.loc[date] /= Product_Scale[max([a for a in self.Fridays if a <= date])]
        Profit["现金"] = ((self.Strategy_Proportion["现金"].T * self.Interest_Rate).T.dropna().shift().fillna(
            0) / 100 + 1) ** (7 / 365) - 1
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit = Profit.T.sort_values(by=max(self.Fridays), ascending=False).T
        return Profit

    @property
    def Strategy_Profit_dollar(self) -> pandas.DataFrame:
        Strategy = pandas.Series(self.__get_strategies())
        Transactions = self.Transactions.copy()
        Transactions["细分策略"] = [Strategy[a] for a in Transactions["产品名称"]]
        Transactions = Transactions[Transactions["细分策略"] != "货币基金"]
        Scales: pandas.DataFrame = self.Strategy_Scale.copy()
        Profit = Scales.diff()
        Profit = Profit[[a for a in Profit.columns if a != "现金"]]
        for x, y, z in zip(Transactions["细分策略"], Transactions["日期"], Transactions["发生金额"]):
            if min(self.Fridays) <= y <= max(self.Fridays) and x != "货币基金":
                Profit.loc[min([a for a in self.Fridays if a >= y]), x] += z
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit = Profit.T.sort_values(by=max(self.Fridays), ascending=False).T
        return Profit

    @property
    def Strategy_Profit_Cumsum(self) -> pandas.DataFrame:
        Strategy = pandas.Series(self.__get_strategies())
        Transactions = self.Transactions.copy()
        Transactions["细分策略"] = [Strategy[a] for a in Transactions["产品名称"]]
        Transactions = Transactions[Transactions["细分策略"] != "货币基金"]
        Product_Scale = self.Scale
        Scales: pandas.DataFrame = self.Strategy_Scale.copy()
        Profit = Scales.diff()
        Profit = Profit[[a for a in Profit.columns if a != "现金"]]
        for x, y, z in zip(Transactions["细分策略"], Transactions["日期"], Transactions["发生金额"]):
            if min(self.Fridays) <= y <= max(self.Fridays) and x != "货币基金":
                Profit.loc[min([a for a in self.Fridays if a >= y]), x] += z
        Profit = (Profit.T / self.Scale[self.Fridays].sort_index().shift()).T
        # for date in Profit.index[1:]:
        #     Profit.loc[date] /= Product_Scale[max([a for a in self.Fridays if a <= date])]
        Profit["现金"] = ((self.Strategy_Proportion["现金"].T * self.Interest_Rate).T.dropna().shift().fillna(
            0) / 100 + 1) ** (7 / 365) - 1
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit = ((Profit.T.sum() + 1).shift().cumprod().fillna(1) * Profit.T).T.cumsum()
        Profit = Profit.T.sort_values(by=max(self.Fridays), ascending=False).T
        return Profit

    @property
    def Strategy_Profit_Cumsum_dollar(self) -> pandas.DataFrame:
        Strategy = pandas.Series(self.__get_strategies())
        Transactions = self.Transactions.copy()
        Transactions["细分策略"] = [Strategy[a] for a in Transactions["产品名称"]]
        Transactions = Transactions[Transactions["细分策略"] != "货币基金"]
        Scales: pandas.DataFrame = self.Strategy_Scale.copy()
        Profit = Scales.diff()
        Profit = Profit[[a for a in Profit.columns if a != "现金"]]
        for x, y, z in zip(Transactions["细分策略"], Transactions["日期"], Transactions["发生金额"]):
            if min(self.Fridays) <= y <= max(self.Fridays) and x != "货币基金":
                Profit.loc[min([a for a in self.Fridays if a >= y]), x] += z
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0}).cumsum()
        Profit = Profit.T.sort_values(by=max(self.Fridays), ascending=False).T
        return Profit

    @property
    def Strategy_NV(self) -> pandas.DataFrame:
        Strategy = pandas.Series(self.__get_strategies())
        Transactions = self.Transactions.copy()
        Transactions["细分策略"] = [Strategy[a] for a in Transactions["产品名称"]]
        Transactions = Transactions[Transactions["细分策略"] != "货币基金"]
        Scales: pandas.DataFrame = self.Strategy_Scale.copy()
        Profit = Scales.diff()
        Profit = Profit[[a for a in Profit.columns if a != "现金" and a != "货币基金"]]
        for x, y, z in zip(Transactions["细分策略"], Transactions["日期"], Transactions["发生金额"]):
            if min(self.Fridays) <= y <= max(self.Fridays) and x != "货币基金":
                Profit.loc[min([a for a in self.Fridays if a >= y]), x] += z
        Profit = Profit / Scales.shift()
        # for date in Profit.index[1:]:
        #     Profit.loc[date] /= Scales.loc[max([a for a in self.Fridays if a <= date])]
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit: pandas.DataFrame = numpy.exp(numpy.log(Profit + 1).cumsum()).ffill()
        Profit = Profit.T.sort_values(by=max(self.Fridays), ascending=False).T.round(4)
        return Profit

    @property
    def Fund_Proportion(self) -> pandas.DataFrame:
        return (
                self.Holdings_Scales.T / self.Scale
        ).sort_values(
            by=max([x for x in self.Holdings])
        ).T.loc[self.Fridays]

    @property
    def Fund_Profit(self) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        Scales: pandas.DataFrame = self.Holdings_Scales.loc[self.Fridays]
        Profit = Scales.diff()
        Names = Profit.columns.tolist()
        for x, y, z in zip(self.Transactions["产品名称"], self.Transactions["日期"], self.Transactions["发生金额"]):
            if x in Names:
                Profit.loc[min([a for a in self.Fridays if a >= y]), x] += z
        Profit = Profit[[x for x in Profit.columns if Strategy.get(x) != "货币基金"]]
        Profit = (Profit.T / self.Scale[self.Fridays].sort_index().shift()).T
        # for date in Profit.index[1:]:
        #     Profit.loc[date] /= Product_Scale[max([a for a in self.Fridays if a <= date])]
        Profit["现金"] = ((self.Strategy_Proportion["现金"].T * self.Interest_Rate).T.dropna().shift().fillna(
            0) / 100 + 1) ** (7 / 365) - 1
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit = Profit.T.sort_values(by=max(self.Fridays), ascending=False).T
        return Profit

    @property
    def Fund_Profit_dollar(self) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        Scales: pandas.DataFrame = self.Holdings_Scales.loc[self.Fridays]
        Profit = Scales.diff()
        Names = Profit.columns.tolist()
        for x, y, z in zip(self.Transactions["产品名称"], self.Transactions["日期"], self.Transactions["发生金额"]):
            if x in Names:
                Profit.loc[min([a for a in self.Fridays if a >= y]), x] += z
        Profit = Profit[[x for x in Profit.columns if Strategy.get(x) != "货币基金"]]
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit = Profit.T.sort_values(by=max(self.Fridays), ascending=False).T
        return Profit

    @property
    def Fund_Profit_Cumsum(self) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        Scales: pandas.DataFrame = self.Holdings_Scales.loc[self.Fridays]
        Profit = Scales.diff()
        Names = Profit.columns.tolist()
        for x, y, z in zip(self.Transactions["产品名称"], self.Transactions["日期"], self.Transactions["发生金额"]):
            if x in Names:
                Profit.loc[min([a for a in self.Fridays if a >= y]), x] += z
        Profit = Profit[[x for x in Profit.columns if Strategy.get(x) != "货币基金"]]
        Profit = (Profit.T / self.Scale[self.Fridays].sort_index().shift()).T
        # for date in Profit.index[1:]:
        #     Profit.loc[date] /= Product_Scale[max([a for a in self.Fridays if a <= date])]
        Profit["现金"] = ((self.Strategy_Proportion["现金"].T * self.Interest_Rate).T.dropna().shift().fillna(
            0) / 100 + 1) ** (7 / 365) - 1
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit = ((Profit.T.sum() + 1).shift().cumprod().fillna(1) * Profit.T).T.cumsum()
        Profit = Profit.T.sort_values(by=max(self.Fridays), ascending=False).T
        return Profit

    @property
    def Fund_Profit_Cumsum_dollar(self) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        Scales: pandas.DataFrame = self.Holdings_Scales.loc[self.Fridays]
        Profit = Scales.diff()
        Names = Profit.columns.tolist()
        for x, y, z in zip(self.Transactions["产品名称"], self.Transactions["日期"], self.Transactions["发生金额"]):
            if x in Names:
                Profit.loc[min([a for a in self.Fridays if a >= y]), x] += z
        Profit = Profit[[x for x in Profit.columns if Strategy.get(x) != "货币基金"]]
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0}).cumsum()
        Profit = Profit.T.sort_values(by=max(self.Fridays), ascending=False).T
        return Profit

    @property
    def Fund_NV(self) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        Scales: pandas.DataFrame = self.Holdings_Scales.loc[self.Fridays]
        Profit = Scales.diff()
        Names = Profit.columns.tolist()
        for x, y, z in zip(self.Transactions["产品名称"], self.Transactions["日期"], self.Transactions["发生金额"]):
            if x in Names:
                Profit.loc[min([a for a in self.Fridays if a >= y]), x] += z
        Profit = Profit[[x for x in Profit.columns if Strategy.get(x) != "货币基金"]]
        Profit = Profit / Scales.shift()
        # for date in Profit.index[1:]:
        #     Profit.loc[date] /= Scales.loc[max([a for a in self.Fridays if a <= date])]
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit: pandas.DataFrame = numpy.exp(numpy.log(Profit + 1).cumsum()).ffill()
        Profit = Profit.T.sort_values(by=max(self.Fridays), ascending=False).T.round(4)
        return Profit

    def Fund_Proportion_by_Strategy(self, strategy):
        result = self.Fund_Proportion.copy()
        Strategy = self.__get_strategies()
        return result[
            [x for x, y in Strategy.items() if y == strategy and x in result.columns]
        ].T.sort_values(by=max(self.Fridays)).T

    def Fund_Profit_by_Strategy(self, strategy) -> pandas.DataFrame:
        result = self.Fund_Profit.copy()
        Strategy = self.__get_strategies()
        return result[
            [x for x, y in Strategy.items() if y == strategy and x in result.columns]
        ].T.sort_values(by=max(self.Fridays), ascending=False).T

    def Fund_Profit_by_Strategy_dollar(self, strategy) -> pandas.DataFrame:
        result = self.Fund_Profit_dollar.copy()
        Strategy = self.__get_strategies()
        return result[
            [x for x, y in Strategy.items() if y == strategy and x in result.columns]
        ].T.sort_values(by=max(self.Fridays), ascending=False).T

    def Fund_Profit_Cumsum_by_Strategy(self, strategy) -> pandas.DataFrame:
        result = self.Fund_Profit_Cumsum.copy()
        Strategy = self.__get_strategies()
        return result[
            [x for x, y in Strategy.items() if y == strategy and x in result.columns]
        ].T.sort_values(by=max(self.Fridays), ascending=False).T

    def Fund_Profit_Cumsum_by_Strategy_dollar(self, strategy) -> pandas.DataFrame:
        result = self.Fund_Profit_Cumsum_dollar.copy()
        Strategy = self.__get_strategies()
        return result[
            [x for x, y in Strategy.items() if y == strategy and x in result.columns]
        ].T.sort_values(by=max(self.Fridays), ascending=False).T

    def Fund_NV_by_Strategy(self, strategy) -> pandas.DataFrame:
        result = self.Fund_NV.copy()
        Strategy = self.__get_strategies()
        return result[
            [x for x, y in Strategy.items() if y == strategy and x in result.columns]
        ].T.sort_values(by=max(self.Fridays), ascending=False).T

    @property
    def Pct_Change_Plot(self) -> line_plot:
        return line_plot(
            (self.Pct_Change * 100).round(2),
            LineStyleOpts=opts.LineStyleOpts(width=2, color="red"),
            ItemStyleOpts=opts.ItemStyleOpts(color="red")
        )

    @property
    def Product_Risk_Index(self) -> RiskIndex:
        return RiskIndex(pandas.DataFrame({"anv": self.Adjusted_Value}).loc[self.Fridays])

    def Page_Output(self, **kwargs) -> page:
        Net_Value = self.Net_Value_Set.to_dict()
        Net_Value.update({"税费前净值（归一）": self.Adjust_Value_without_Fee(fee_ratio=kwargs.get("fee_ratio", 0.0004))})
        charts = [
            line_plot(
                pandas.DataFrame(Net_Value).loc[self.Fridays],
                LegendOpts=opts.LegendOpts(selected_mode="single"),
                TitleOpts=opts.TitleOpts(title="单位净值")
            ),
            line_plot(
                (self.Scale.loc[self.Fridays] / 10000).round(2),
                LegendOpts=opts.LegendOpts(is_show=False),
                TitleOpts=opts.TitleOpts(title="资产规模", subtitle="单位：万元"),
                AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5),
                YaxisOpts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    min_=0
                )
            ),
            line_plot(
                (self.Strategy_Proportion.loc[self.Fridays] * 100).round(2),
                TitleOpts=opts.TitleOpts(title="策略比重", subtitle="单位：%"),
                Stack="1",
                AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5),
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            bar_plot(
                (self.Strategy_Profit * 100).round(4),
                TitleOpts=opts.TitleOpts(title="策略收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ).overlap(self.Pct_Change_Plot),
            bar_plot(
                (self.Strategy_Profit_Cumsum * 100).round(4),
                TitleOpts=opts.TitleOpts(title="策略累计收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            line_plot(
                self.Strategy_NV.round(4),
                TitleOpts=opts.TitleOpts(title="策略单位净值"),
            ),

            line_plot(
                (self.Fund_Proportion.loc[self.Fridays] * 100).round(2),
                TitleOpts=opts.TitleOpts(title="子基金比重", subtitle="单位：%"),
                Stack="1",
                AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5),
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            bar_plot(
                (self.Fund_Profit * 100).round(4),
                TitleOpts=opts.TitleOpts(title="子基金收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ).overlap(self.Pct_Change_Plot),
            bar_plot(
                (self.Fund_Profit_Cumsum * 100).round(4),
                TitleOpts=opts.TitleOpts(title="子基金累计收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            line_plot(
                self.Fund_NV.round(4),
                TitleOpts=opts.TitleOpts(title="子基金单位净值"),
            )
        ]
        for Strategy in set(self.__get_strategies().values()):
            if Strategy != "货币基金":
                charts += [
                    line_plot(
                        (self.Fund_Proportion_by_Strategy(Strategy) * 100).round(2),
                        TitleOpts=opts.TitleOpts(title="%s 子基金比重" % Strategy, subtitle="单位：%"),
                        Stack="1",
                        AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5)
                    ),
                    bar_plot(
                        (self.Fund_Profit_by_Strategy(Strategy) * 100).round(4),
                        TitleOpts=opts.TitleOpts(title="%s 子基金收益贡献" % Strategy, subtitle="单位：%"),
                        Stack="1"
                    ),
                    bar_plot(
                        (self.Fund_Profit_Cumsum_by_Strategy(Strategy) * 100).round(4),
                        TitleOpts=opts.TitleOpts(title="%s 子基金累计收益贡献" % Strategy, subtitle="单位：%"),
                        Stack="1"
                    ),
                    line_plot(
                        self.Fund_NV_by_Strategy(Strategy).round(4),
                        TitleOpts=opts.TitleOpts(title="%s 子基金单位净值" % Strategy)
                    )
                ]
        result = page(charts)
        result.page_title = "%s " % kwargs.get("Code")
        return result


class balance_sheet_fetch:
    def __init__(self, code: typing.Union[str, None] = None, name: typing.Union[str, None] = None, **kwargs):
        self.__code = code
        self.__name = self.__name_change(name)
        self.__Mongo_Client = Mongo_Client()
        self.__DB_Email = self.__Mongo_Client["CBS数据"]["投研部邮箱"]
        self.__Email_Client = imaplib.IMAP4_SSL("imap.qiye.163.com", 993)
        self.__Email_Client.login(Configs["TYB_Email"]["username"], Configs["TYB_Email"]["password"])
        self.__localize_route = kwargs.get("download_path")

    @property
    def __email_record(self):
        data = pandas.DataFrame(
            [
                x for x in self.__DB_Email.find(
                {
                    "$and": [
                        {"主题": {"$regex": self.__name}},
                        {"主题": {"$regex": "估值表"}}
                    ]
                },
                {"_id": 0, "序号": 1, "附件": 1, "发件时间": 1, "文件夹": 1}
            )
            ]
        ).sort_values(by=["发件时间"], ascending=False)
        data: pandas.DataFrame = data.loc[
            [
                x for x in data.index
                if sum(
                [
                    y.__contains__(self.__code) and (y.__contains__("估值表") or y.__contains__("估值报表")) for y in
                    data["附件"][x] if isinstance(y, str)
                ]
            )
            ]
        ]
        data["附件"] = [",".join(x) for x in data["附件"]]
        data["估值表日期"] = [self.__extract_date(x) for x in data["附件"]]
        return data.drop(columns=["发件时间"]).drop_duplicates()

    @staticmethod
    def __name_change(name: str):
        return name.replace(
            "私募", ""
        ).replace(
            "证券", ""
        ).replace(
            "投资", ""
        ).replace(
            "基金", ""
        )

    def __extract_date(self, filename: str):
        filename = filename.replace(self.__name, "").replace(self.__code, "")
        date = "".join([x for x in filename.split(".")[0] if 48 <= ord(x) <= 57])
        return pandas.to_datetime(date).date()

    def fetch_attachment(self, folder, order):
        self.__Email_Client.select(folder)
        _, data = self.__Email_Client.fetch(str(order), "(RFC822)")
        if data[0]:
            try:
                msg_content = data[0][-1].decode(chardet.detect(data[0][-1])['encoding'])
            except:
                try:
                    msg_content = data[0][-1].decode("ISO-8859-1")
                except:
                    msg_content = data[0].decode("ISO-8859-1")
            msg = email.parser.Parser().parsestr(msg_content)
            for item in msg.walk():
                file_name = item.get_param("name")
                if file_name and ("估值表" in decode_str(file_name) or "估值报表" in decode_str(file_name)):
                    h = email.header.Header(file_name)
                    dh = email.header.decode_header(h)
                    filename = dh[0][0]
                    if dh[0][1]:
                        filename = decode_str(str(filename, dh[0][1]))
                        content = item.get_payload(decode=True)
                        self.__insert_balance_sheet(content, filename, self.__extract_date(filename))
                        if isinstance(self.__localize_route, str) and self.__localize_route:
                            with open(
                                    os.path.join(self.__localize_route.replace("/", "\\"), filename),
                                    mode="wb"
                            ) as file:
                                file.write(content)
                        print("---已下载--- ==> %s" % filename)
                        return content

    def get(self, **kwargs):
        start = pandas.to_datetime(kwargs.get("start", "20000101")).date()
        end = pandas.to_datetime(kwargs.get("end", datetime.date.today())).date()
        downloaded = pandas.DataFrame(
            [
                x for x in self.__Mongo_Client["CBS数据"]["产品估值表"].find(
                {
                    "产品代码": self.__code,
                    "$and": [
                        {"日期": {"$gte": pandas.to_datetime(start)}},
                        {"日期": {"$lte": pandas.to_datetime(end)}}
                    ]
                }
            )
            ]
        )
        to_download = self.__email_record.copy()
        to_download = to_download[
            (to_download["估值表日期"] <= end) & (to_download["估值表日期"] >= start)
            ]
        to_download = to_download.loc[
            [
                x for x in to_download.index
                if pandas.to_datetime(to_download.loc[x, "估值表日期"]) not in downloaded["日期"].tolist()
            ]
        ] if len(downloaded) else to_download
        to_download = to_download.sort_values(by=["文件夹", "序号"]).reset_index(drop=True)
        if len(to_download):
            print(to_download)
        return [
            self.fetch_attachment(x, y) for x, y, z in zip(
                to_download["文件夹"], to_download["序号"], to_download["附件"]
            )
        ] + (downloaded["文件内容"].tolist() if len(downloaded) else [])

    def delete(self, start):
        self.__Mongo_Client["CBS数据"]["产品估值表"].delete_many(
            filter={
                "产品代码": self.__code,
                "日期": {"$gte": pandas.to_datetime(start)}
            }
        )

    def __insert_balance_sheet(
            self,
            content: bytes,
            filename: str,
            date: typing.Union[str, datetime.date, datetime.datetime]
    ):
        Collection = self.__Mongo_Client["CBS数据"]["产品估值表"]
        if Collection.find_one(
                {
                    "文件名称": filename,
                    "日期": pandas.to_datetime(date),
                    "产品代码": self.__code
                }
        ):
            Collection.update_one(
                {
                    "文件名称": filename,
                    "日期": pandas.to_datetime(date),
                    "产品代码": self.__code
                },
                {
                    "$set": {"文件内容": content}
                }
            )
        else:
            Collection.insert_one(
                {
                    "产品代码": self.__code,
                    "日期": pandas.to_datetime(date),
                    "文件名称": filename,
                    "文件内容": content
                }
            )


class Analysis_Results(balance_sheet_analysis):
    __fetch: balance_sheet_fetch
    Code: str
    Name: str
    start_date: typing.Union[str, datetime.date, datetime.datetime]
    end_date: typing.Union[str, datetime.date, datetime.datetime]
    PNL_Cumsum: pandas.DataFrame

    def __init__(self, code, name, **kwargs):
        self.Code = code
        self.Name = name
        self.Grade = "%s份额" % kwargs.get('grade', "总")
        self.start_date = kwargs.get("start", pandas.to_datetime("20200101"))
        self.end_date = kwargs.get("end", datetime.date.today())
        self.__fetch = balance_sheet_fetch(self.Code, self.Name)
        self.platform = kwargs.get("platform", "")
        os.makedirs(os.path.join("outputs", self.Code), exist_ok=True)
        print(" ----- 读取估值表中 ----- ")
        super().__init__(
            balance_sheets=[
                read_balance_sheet(x) for x in self.__fetch.get(start=self.start_date, end=self.end_date)
            ],
            Strategy_File_Route=os.path.join("outputs", self.Code, "子基金策略.xlsx"),
            Transactions=os.path.join("outputs", self.Code, "申赎记录.xlsx"),
            name=name,
            code=code,
            Grade=kwargs.get('grade', "总"),
            index_category=kwargs.get("index_category", 2),
            platform=kwargs.get("platform", "")
        )
        self.initial_proportion = kwargs.get(
            "initial_proportion",
            {x: 1 / len(self.Strategy_Basic_Index.columns) for x in self.Strategy_Basic_Index.columns}
        )
        if not isinstance(self.initial_proportion, dict):
            raise TypeError("初始权重请以字典格式输入")
        if self.platform != "web":
            self.set_PNL()

    def set_PNL(self):
        self.PNL_Cumsum = self.__PNL_Cumsum()

    @property
    def Beta_PNL(self) -> pandas.DataFrame:
        result: pandas.DataFrame = (
                self.Strategy_Basic_Index.pct_change() * pandas.Series(self.initial_proportion)
        ).T.dropna(how="all").T.fillna(0)
        result = result.rename(columns={x: "%s-BETA" % x for x in result.columns})
        return result

    @property
    def Alpha1_PNL(self) -> pandas.DataFrame:
        proportion = self.Strategy_Proportion.shift()
        proportion = pandas.DataFrame(
            {
                x: proportion[x].to_dict() if x in proportion.columns.tolist() else {} for x in self.initial_proportion.keys()
            }
        ).fillna(0)
        result = (self.Strategy_Basic_Index.pct_change() * (
                proportion - pandas.Series(self.initial_proportion)
        )).T.dropna(how="all").T.fillna(0)
        result = result.rename(columns={x: "%s-ALPHA1" % x for x in result.columns})
        return result

    @property
    def Alpha2_PNL(self) -> pandas.DataFrame:
        Beta = self.Beta_PNL.copy()
        Beta = Beta.rename(columns={x: x.split("-")[0] for x in Beta.columns})
        Alpha1 = self.Alpha1_PNL.copy()
        Alpha1 = Alpha1.rename(columns={x: x.split("-")[0] for x in Alpha1.columns})
        result = (
                self.Strategy_Profit -
                Beta -
                Alpha1
        ).T.dropna(how="all").T.fillna(0)
        result = result.rename(columns={x: "%s-ALPHA2" % x for x in result.columns})
        return result

    @property
    def PNL(self) -> pandas.DataFrame:
        return pandas.concat(
            [self.Beta_PNL, self.Alpha1_PNL, self.Alpha2_PNL, self.Strategy_Profit["现金"]], axis=1
        ).loc[self.Fridays]

    def __PNL_Cumsum(self) -> pandas.DataFrame:
        result = self.PNL.copy()
        result = ((result.T.sum() + 1).shift().cumprod().fillna(1) * result.T).T.cumsum()
        return result

    @property
    def Beta_PNL_Cumsum(self) -> pandas.DataFrame:
        result = self.PNL_Cumsum.copy()
        return result[[x for x in result.columns if x.__contains__("BETA")]]

    @property
    def Alpha1_PNL_Cumsum(self) -> pandas.DataFrame:
        result = self.PNL_Cumsum.copy()
        return result[[x for x in result.columns if x.__contains__("ALPHA1")]]

    @property
    def Alpha2_PNL_Cumsum(self) -> pandas.DataFrame:
        result = self.PNL_Cumsum.copy()
        return result[[x for x in result.columns if x.__contains__("ALPHA2")]]

    @property
    def __Proportion_Bias(self) -> pandas.DataFrame:
        propose_scale = pandas.DataFrame(
            {name: self.Scale * prop for name, prop in self.initial_proportion.items()}
        )
        return (self.Strategy_Scale / propose_scale.loc[self.Fridays]).T.dropna(how="all").T - 1

    @property
    def Comparable_Alpha1(self) -> pandas.DataFrame:
        return (self.Strategy_Basic_Index.pct_change() * self.__Proportion_Bias).T.dropna(how="all").T

    @property
    def Comparable_Alpha1_Cumsum(self) -> pandas.DataFrame:
        result = self.Comparable_Alpha1.copy()
        result = ((result.T.sum() + 1).shift().cumprod().fillna(1) * result.T).T.cumsum()
        return result

    @property
    def Comparable_Alpha2(self) -> pandas.DataFrame:
        result = (self.Strategy_NV.pct_change() + 1) / (self.Strategy_Basic_Index.pct_change() + 1) - 1
        return result.T.dropna(how="all").T.fillna(0)

    @property
    def Comparable_Alpha2_Cumsum(self) -> pandas.DataFrame:
        result = self.Comparable_Alpha2.copy()
        result = ((result.T.sum() + 1).shift().cumprod().fillna(1) * result.T).T.cumsum()
        return result

    def Data_Output(self, **kwargs):
        NV = self.Net_Value_Set.copy()
        NV["费前净值"] = self.Adjust_Value_without_Fee(fee_ratio=kwargs.get("fee_ratio", 0.0004))
        return {
            "单位净值": NV,
            "资产规模": self.Scale.rename("资产规模"),
            "策略比重": self.Strategy_Proportion.copy(),
            "策略收益贡献": self.Strategy_Profit.copy(),
            "策略收益贡献细分": self.PNL.copy(),
            "策略累计收益贡献": self.Strategy_Profit_Cumsum.copy(),
            "策略累计收益贡献细分": self.PNL_Cumsum.copy(),
            "策略单位净值": self.Strategy_NV.copy(),
            "子基金比重": self.Fund_Proportion.copy(),
            "子基金收益贡献": self.Fund_Profit.copy(),
            "子基金累计收益贡献": self.Fund_Profit_Cumsum.copy(),
            "Comparable Alpha1": self.Comparable_Alpha1,
            "Comparable Alpha1 Cumsum": self.Comparable_Alpha1_Cumsum,
            "Comparable Alpha2": self.Comparable_Alpha2,
            "Comparable Alpha2 Cumsum": self.Comparable_Alpha2_Cumsum,
        }

    @property
    def Risk_Index_Table(self) -> comp_table:
        RI = self.Product_Risk_Index
        content = {
            "统计区间": "%s-%s" % (self.Start.strftime("%Y%m%d"), self.End.strftime("%Y%m%d")),
            "区间复权净值": "%1.4f" % RI.Table.sort_index()["anv"].tolist()[-1],
            "年化收益率": "%1.2f%%" % (RI.Annual_Return().to_dict().get("anv") * 100),
            "年化波动率": "%1.2f%%" % (RI.Annual_Volatility().to_dict().get("anv") * 100),
            "最大回撤": "%1.2f%%" % (RI.Maximum_Drawdown().to_dict().get("anv") * 100),
            "夏普率": "%1.2f" % RI.Sharpe_Ratio().to_dict().get("anv"),
            "索提诺比率": "%1.2f" % RI.Sortino_Ratio().to_dict().get("anv"),
            "卡玛比率": "%1.2f" % RI.Calmar_Ratio().to_dict().get("anv"),
            "周胜率": "%1.2f%%" % (RI.Success().to_dict().get("anv") * 100)
        }
        return comp_table(
            table=pandas.DataFrame(
                {
                    self.Name: content
                }
            ).rename_axis(columns="产品名称").loc[[x for x in content.keys()]],
            title="产品概况"
        )

    def Page_Output(self, **kwargs) -> page:
        Net_Value = self.Net_Value_Set.to_dict()
        Net_Value.update({"税费前净值（归一）": self.Adjust_Value_without_Fee(fee_ratio=kwargs.get("fee_ratio", 0.0004))})
        PNL = self.PNL.copy()
        PNL_Cumsum = self.PNL_Cumsum.copy()

        ADNV_Plot = line_plot(
            ((pandas.DataFrame({"税费前收益": Net_Value["税费前净值（归一）"]}) - 1) * 100).round(4),
            LineStyleOpts=opts.LineStyleOpts(width=2, color="red"),
            ItemStyleOpts=opts.ItemStyleOpts(color="red")
        )
        charts = [
            self.Risk_Index_Table,
            line_plot(
                pandas.DataFrame(Net_Value).loc[self.Fridays].round(4),
                LegendOpts=opts.LegendOpts(selected_mode="single"),
                TitleOpts=opts.TitleOpts(title="单位净值")
            ),
            line_plot(
                (self.Scale.loc[self.Fridays] / 10000).round(2),
                LegendOpts=opts.LegendOpts(is_show=False),
                TitleOpts=opts.TitleOpts(title="资产规模", subtitle="单位：万元"),
                AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5),
                YaxisOpts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    min_=0
                )
            ),
            line_plot(
                (self.Strategy_Proportion.loc[self.Fridays] * 100).round(2),
                TitleOpts=opts.TitleOpts(title="策略比重", subtitle="单位：%"),
                Stack="1",
                AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5),
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            line_plot(
                self.Strategy_NV.round(4),
                TitleOpts=opts.TitleOpts(title="策略单位净值"),
            ),
            bar_plot(
                (self.Strategy_Profit * 100).round(4),
                TitleOpts=opts.TitleOpts(title="策略收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ).overlap(self.Pct_Change_Plot),
            bar_plot(
                (self.Strategy_Profit_Cumsum * 100).round(4),
                TitleOpts=opts.TitleOpts(title="策略累计收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ).overlap(ADNV_Plot),
            bar_plot(
                (PNL * 100).round(4),
                TitleOpts=opts.TitleOpts(title="策略收益贡献细分", subtitle="单位：%"),
                Stack="1",
                YaxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ).overlap(self.Pct_Change_Plot),
            bar_plot(
                (PNL_Cumsum * 100).round(4),
                TitleOpts=opts.TitleOpts(title="策略累计收益贡献细分", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                ),
                LegendOpts=opts.LegendOpts(
                    type_="scroll",
                    pos_top="bottom",
                    selected_map={x: False for x in PNL_Cumsum.columns}
                ),
                ToolboxOpts=opts.ToolboxOpts(
                    feature=opts.ToolBoxFeatureOpts(
                        restore=opts.ToolBoxFeatureRestoreOpts(),
                        data_view=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                        data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                        save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                            background_color="white"
                        )
                    )
                )
            ).overlap(ADNV_Plot),
            line_plot(
                (pandas.DataFrame(
                    {
                        "BETA": self.Beta_PNL_Cumsum.T.sum(),
                        "ALPHA1": self.Alpha1_PNL_Cumsum.T.sum(),
                        "ALPHA2": self.Alpha2_PNL_Cumsum.T.sum()
                    }
                ) * 100).round(4),
                TitleOpts=opts.TitleOpts(
                    title="Beta/Alpha1/Alpha2 收益曲线"
                ),
                YaxisOpts=opts.AxisOpts(
                    is_scale=True,
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            comp_table(
                table=(pandas.DataFrame(
                    {
                        "母基金收益贡献": {
                            "BETA": self.Beta_PNL_Cumsum.iloc[-1].sum(),
                            "ALPHA1": self.Alpha1_PNL_Cumsum.iloc[-1].sum(),
                            "ALPHA2": self.Alpha2_PNL_Cumsum.iloc[-1].sum(),
                        }
                    }
                ).T.rename_axis(columns="单位：%")*100).round(2),
                title="期末收益拆解统计",
                subtitle="统计周期：%s - %s" % (self.start_date, self.end_date)
            ),
            line_plot(
                self.strategy_index(grade=kwargs.get("index_category", 2)).round(4),
                TitleOpts=opts.TitleOpts(title="策略基准指数"),
                YaxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    is_scale=True
                )
            ),
            line_plot(
                (self.Fund_Proportion.loc[self.Fridays] * 100).round(2),
                TitleOpts=opts.TitleOpts(title="子基金比重", subtitle="单位：%"),
                Stack="1",
                AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5),
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            bar_plot(
                (self.Fund_Profit * 100).round(4),
                TitleOpts=opts.TitleOpts(title="子基金收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ).overlap(self.Pct_Change_Plot),
            bar_plot(
                (self.Fund_Profit_Cumsum * 100).round(4),
                TitleOpts=opts.TitleOpts(title="子基金累计收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            line_plot(
                self.Fund_NV.round(4),
                TitleOpts=opts.TitleOpts(title="子基金单位净值"),
            )
        ]
        for Strategy in self.Strategy_Scale.columns:
            if Strategy != "货币基金" and Strategy != "现金":
                charts += [
                    line_plot(
                        (self.Fund_Proportion_by_Strategy(Strategy) * 100).round(2),
                        TitleOpts=opts.TitleOpts(title="%s 子基金比重" % Strategy, subtitle="单位：%"),
                        Stack="1",
                        AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5)
                    ),
                    bar_plot(
                        (self.Fund_Profit_by_Strategy(Strategy) * 100).round(4),
                        TitleOpts=opts.TitleOpts(title="%s 子基金收益贡献" % Strategy, subtitle="单位：%"),
                        Stack="1"
                    ),
                    bar_plot(
                        (self.Fund_Profit_Cumsum_by_Strategy(Strategy) * 100).round(4),
                        TitleOpts=opts.TitleOpts(title="%s 子基金累计收益贡献" % Strategy, subtitle="单位：%"),
                        Stack="1"
                    ),
                    line_plot(
                        self.Fund_NV_by_Strategy(Strategy).round(4),
                        TitleOpts=opts.TitleOpts(title="%s 子基金单位净值" % Strategy)
                    )
                ]
        result = page(charts)
        result.page_title = "%s 业绩分析" % self.Code
        if kwargs.get("output"):
            result.render(os.path.join("outputs", "FOF_Analysis", self.Code, "%s 业绩分析.html" % self.Code))
            with pandas.ExcelWriter(os.path.join("outputs", "FOF_Analysis", self.Code, "数据.xlsx"), mode="w") as ExcelWriter:
                for x, y in self.Data_Output(fee_ratio=kwargs.get("fee_ratio", 0.0004)).items():
                    y.to_excel(ExcelWriter, sheet_name=x)
        return result
