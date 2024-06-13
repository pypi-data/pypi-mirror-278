# -*- coding: utf-8 -*-
from ZYYA_Codes.utils import Mongo_Client, GESHANG_NetValue, get_fridays
import typing
import numpy
import pandas

__all__ = ["net_value_fetch", "basic_index"]


class net_value_fetch:
    # Name_Index = {"931190.CSI": {"产品名称": "信用债AA+", "一级策略": "固收", "二级策略": "信用债", "三级策略": ""}}
    __Client = Mongo_Client()
    Name_List = pandas.DataFrame(
        [x for x in __Client["CBS数据"]["策略基准成分"].find({}, {"_id": 0})]
    ).set_index("产品名称").sort_values(by=["一级策略", "二级策略", "三级策略"]).T.to_dict()
    data: typing.Dict[str, pandas.Series] = {}

    def get_nv(self):
        self.data = {
            x: GESHANG_NetValue(self.Name_List[x]["代码"]) for x in self.Name_List
            if not print(self.Name_List[x]["一级策略"], x, self.Name_List[x]["代码"])
        }
        left = [x for x, y in self.data.items() if not (isinstance(y, pandas.Series) or self.Name_List[x]["代码"])]
        print("----- 从CBS获取数据中 -----")
        for name in left:
            print(self.Name_List[name]["一级策略"], name, self.Name_List[name]["代码"])
            nv = pandas.DataFrame(
                [
                    x for x in self.__Client["CBS数据"]["产品净值"].find(
                        {"产品名称": {"$regex": name}},
                        {"净值日期": 1, "复权净值": 1, "_id": 0}
                    )
                ]
            ).rename(columns={"净值日期": "日期"}).set_index("日期")["复权净值"]
            self.data.update({name: nv})

    @property
    def NV_Table(self) -> pandas.DataFrame:
        nvs = {x: pandas.DataFrame(y).reset_index() for x, y in self.data.items() if isinstance(y, pandas.Series)}
        for name, sheet in nvs.items():
            sheet["产品名称"] = name
            sheet["一级策略"] = self.Name_List[name]["一级策略"]
            sheet["二级策略"] = self.Name_List[name]["二级策略"]
            sheet["三级策略"] = self.Name_List[name]["三级策略"]
            sheet["私募公司"] = self.Name_List[name]["私募公司"]
            nvs[name] = sheet
        # from WindPy import w
        # w.start()
        # wind_data = w.wsd([x for x in self.Name_Index.keys()], "close", beginTime="20201231")
        # wind_data = {
        #     wind_data.Codes[x]: pandas.DataFrame(
        #         {"复权净值": wind_data.Data[x]}, index=wind_data.Times
        #     ).rename_axis("日期").reset_index()
        #     for x in range(len(wind_data.Codes))
        # }
        # for code, table in wind_data.items():
        #     table["产品名称"] = self.Name_Index[code]["产品名称"]
        #     table["一级策略"] = self.Name_Index[code]["一级策略"]
        #     table["二级策略"] = self.Name_Index[code]["二级策略"]
        #     table["三级策略"] = self.Name_Index[code]["三级策略"]
        #     table["私募公司"] = ""
        #     table["日期"] = table["日期"].astype("datetime64[ns]")
        #     nvs.update({code: table})
        return pandas.concat([x for x in nvs.values()], ignore_index=True).reset_index(drop=True)

    def insert_net_values(self):
        downloaded = pandas.DataFrame(
            [x for x in self.__Client["CBS数据"]["策略基准净值"].find({}, {"产品名称": 1, "日期": 1, "_id": 0})]
        ).values.tolist()
        to_insert = self.NV_Table.copy()
        to_insert = to_insert.loc[
            [x for x in to_insert.index if not [to_insert["日期"][x], to_insert["产品名称"][x]] in downloaded]
        ]
        if len(to_insert):
            self.__Client["CBS数据"]["策略基准净值"].insert_many([x for x in to_insert.T.to_dict().values()])


class basic_index:
    Client = Mongo_Client()
    __NV_Table = pandas.DataFrame(
        [x for x in Client["CBS数据"]["策略基准净值"].find({}, {"_id": 0})]
    )
    __NV_Table["日期"] = [pandas.to_datetime(x).date() for x in __NV_Table["日期"]]

    def __init__(self, **kwargs):
        self.Start = pandas.to_datetime(kwargs.get("start", self.__NV_Table["日期"].min())).date()
        self.End = pandas.to_datetime(kwargs.get("end", self.__NV_Table["日期"].max())).date()

    @property
    def __Net_Value(self) -> pandas.DataFrame:
        table = self.__NV_Table.pivot_table(index="日期", columns="产品名称", values="复权净值")
        fridays = get_fridays(start=self.Start, end=self.End)
        return table.loc[fridays]

    def strategy_index(self, **kwargs) -> pandas.DataFrame:
        num_dict = {"1": "一级策略", "2": "二级策略", "3": "三级策略"}
        grade = str(kwargs.get("grade", 2))
        strategy_dict = self.__NV_Table.groupby(num_dict[grade])["产品名称"].agg(lambda x: list(set(x))).to_dict()
        pct_change = self.__Net_Value.pct_change().fillna(0)
        strategy_pct_change = pandas.DataFrame(
            {x: pct_change[y].T.mean() - 0.01 * 7 / 365 for x, y in strategy_dict.items()}
        )
        result = numpy.exp(numpy.log(strategy_pct_change + 1).cumsum())
        return result - (result - 1) * (result > 1).astype(int) * 0.2
