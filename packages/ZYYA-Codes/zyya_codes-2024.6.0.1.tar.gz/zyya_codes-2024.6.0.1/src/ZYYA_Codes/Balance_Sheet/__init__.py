# -*- coding: utf-8 -*-
import datetime
import pandas
import _io
import typing
import warnings
from ZYYA_Codes.utils import Mongo_Client

warnings.filterwarnings("ignore")

__all__ = ['read_balance_sheet']
_Standard = pandas.DataFrame(
    [x for x in Mongo_Client()["CBS数据"]["估值表准则"].find({}, {"_id": 0})]
)
_Cash = _Standard[
    (_Standard["科目名称"].str.contains("货币"))
    &
    (pandas.Series({x: len(y.split(".")) == 2 for x, y in _Standard["科目代码"].to_dict().items()}))
    &
    (~_Standard["科目代码"].str.contains("1109"))
    ]
_Cash.iloc[-1] = {"科目代码": "1203.05"}


class read_balance_sheet:
    def __init__(
            self,
            io: typing.Union[str, bytes, _io.TextIOWrapper, _io.BufferedReader]
    ) -> None:
        self.File = io
        self.Original_Table = pandas.read_excel(io)
        self.Date = self.__find_date()
        self.Table = self.read_table()

    def read_table(self) -> pandas.DataFrame:
        table = pandas.read_excel(self.File)
        i, j = 0, 0
        while "科目代码" not in table.iloc[i].tolist():
            i += 1
        while "科目代码" != table.iloc[i, j]:
            j += 1
        table = pandas.read_excel(self.File, header=i + 1, index_col=j, na_filter="")
        table.index = [str(x) for x in table.index]
        table["成本-本币"] = table["成本-本币" if "成本-本币" in table.columns else "成本"]
        table["市值-本币"] = table["市值-本币" if "市值-本币" in table.columns else "市值"]
        return table.loc[
            [x for x in table.index if not (x == "科目代码" or x == "")]
        ].fillna("").replace({" ", ""})

    def __find_date(self) -> datetime.date:
        table = self.Original_Table.T.dropna(how="all").T
        x = [y for y in table.iloc[:, 0].tolist() if str(y).__contains__("日期")][0]
        return pandas.to_datetime("".join([y for y in x if 48 <= ord(y) <= 57])).date()

    @staticmethod
    def __change_header(table: pandas.DataFrame) -> pandas.DataFrame:
        table["科目名称"] = ["".join(x.split(" ")) if isinstance(x, str) else x for x in table["科目名称"]]
        table["数量"] = table["数量"].astype(float) if len(table) else table["数量"]
        table["成本-本币"] = table["成本-本币" if "成本-本币" in table.columns else "成本"].astype(float)
        table["市值-本币"] = table[
            "市值-本币" if "市值-本币" in table.columns else "市值"
        ].astype(float)
        return table

    @staticmethod
    def __change_fund_name(name: str) -> str:
        head = name[: -4]
        tail = name[-4:]
        if sum([48 <= ord(x) <= 57 for x in tail]) != 4:
            while 48 <= ord(tail[-1]) <= 57:
                tail = tail[:-1]
        return head + tail

    @property
    def Private_Funds(self) -> pandas.DataFrame:
        table = self.Table[self.Table["停牌信息"] != ""]
        table = table.loc[[x for x in table.index if x.__contains__("1108") or x.__contains__("1109")]]
        table = table.loc[[x for x in table.index if x[: 4] == "1108" or x[: 4] == "1109"]]
        if len(table):
            table = self.__change_header(table)
            table["科目名称"] = [self.__change_fund_name(x) for x in table["科目名称"]]
            table = table.pivot_table(index="科目名称", values=["数量", "成本-本币", "市值-本币"], aggfunc="sum")
            table["单位成本"] = table["成本-本币"] / table["数量"]
        return table

    @property
    def Derivatives(self) -> pandas.DataFrame:
        table = self.Table[self.Table["停牌信息"] != ""]
        table = table.loc[[x for x in table.index if x.__contains__("3102")]]
        table = table.loc[[x for x in table.index if x[: 4] == "3102"]]
        table = self.__change_header(table)
        return table

    @property
    def Stocks(self) -> pandas.DataFrame:
        table = self.Table[self.Table["停牌信息"] != ""]
        table = table.loc[[x for x in table.index if x.__contains__("1102")]]
        table = table.loc[[x for x in table.index if x[: 4] == "1102"]]
        table = self.__change_header(table)
        return table

    @property
    def ETFs(self) -> pandas.DataFrame:
        table = self.Table[self.Table["停牌信息"] != ""]
        table = table.loc[[x for x in table.index if x.__contains__("1105")]]
        table = table.loc[[x for x in table.index if x[: 4] == "1105"]]
        table = self.__change_header(table)
        table = table.loc[
            [
                x for x in table.index
                if not (
                    x[:4] + "." + x[4:6] in _Cash["科目代码"].tolist() or ".".join(x.split(".")[:2]) in _Cash[
                "科目代码"].tolist()
            )
            ]
        ]
        return table

    @property
    def Shares(self) -> typing.Union[int, float]:
        return self.Table["数量"]["实收资本"]

    @property
    def Hierachical_Shares(self) -> typing.Dict[str, typing.Union[int, float]]:
        location = 0
        while self.Table.index[location] != "实收资本":
            location += 1
        data = self.Table["数量"][
            [x for x in self.Table.index if
             x.__contains__("实收资本") and self.Table.index.tolist().index(x) >= location]
        ]
        return {"总份额" if x == 0 else "%s份额" % chr(x + 64): data.iloc[x] for x in range(len(data))}

    @property
    def Scale(self) -> typing.Union[int, float]:
        return self.Table[
            "市值-本币" if "市值-本币" in self.Table.columns else "市值"
        ][
            [x for x in self.Table.index if x.__contains__("资产净值")][0]
        ]

    @property
    def Hierachical_Scale(self):
        data = self.Table[
            "市值-本币" if "市值-本币" in self.Table.columns else "市值"
        ][
            [x for x in self.Table.index if x.__contains__("资产净值")]
        ]
        return {"总份额" if x == 0 else "%s份额" % chr(x + 64): data.iloc[x] for x in range(len(data))}

    @property
    def Net_Value(self) -> float:
        return round(self.Scale / self.Shares, 8)

    @property
    def Hierachical_Net_Value(self) -> typing.Dict[str, typing.Union[int, float]]:
        return (
                pandas.Series(self.Hierachical_Scale) / pandas.Series(self.Hierachical_Shares)
        ).round(8).to_dict()

    @property
    def Accumulated_Value(self) -> float:
        return float(self.Table.loc[[x for x in self.Table.index if x.__contains__("累计单位净值")][0], "科目名称"])

    @property
    def Hierachical_Accumulated_Value(self) -> typing.Dict[str, typing.Union[int, float]]:
        data = self.Table["科目名称"][
            [x for x in self.Table.index if x.__contains__("累计单位净值")]
        ].astype(float)
        return {"总份额" if x == 0 else "%s份额" % chr(x + 64): data.iloc[x] for x in range(len(data))}

    @staticmethod
    def __find_dp(number: typing.Union[int, float]) -> int:
        n = 0
        while round(number, n) != number:
            n += 1
        return n

    @property
    def Properties(self) -> pandas.DataFrame:
        table = self.Table[(self.Table["停牌信息"] != "") & (self.Table["停牌信息"] != " ")]
        table = self.__change_header(table)
        table["科目名称"] = [self.__change_fund_name(x) if x.__contains__("基金") else x for x in table["科目名称"]]
        table = table[(~table["科目名称"].astype("str").str.contains("货币"))]
        table = table.loc[
            [
                x for x in table.index
                if not (
                    x[:4] + "." + x[4:6] in _Cash["科目代码"].tolist() or ".".join(x.split(".")[:2]) in _Cash[
                "科目代码"].tolist()
            )
            ]
        ]
        if len(table):
            table = self.__change_header(table)
            table["科目名称"] = [self.__change_fund_name(x) for x in table["科目名称"]]
            table = table.pivot_table(index="科目名称", values=["数量", "成本-本币", "市值-本币"], aggfunc="sum")
            table["单位成本"] = table["成本-本币"] / table["数量"]
        return table

    @property
    def Cash(self) -> typing.Union[int, float]:
        result = {
            "银行存款": float(
                self.Table.replace("", float("nan"))["市值-本币"]["1002"]) if "1002" in self.Table.index else 0,
            "结算备付金": float(
                self.Table.replace("", float("nan"))["市值-本币"]["1021"]) if "1021" in self.Table.index else 0,
            "存出保证金": float(
                self.Table.replace("", float("nan"))["市值-本币"]["1031"]) if "1031" in self.Table.index else 0,
            "衍生品交收资金": float(
                self.Table.replace("", float("nan"))["市值-本币"]["3003"]) if "3003" in self.Table.index else 0,
            "逆回购": float(
                self.Table.replace("", float("nan"))["市值-本币"]["1202"]) if "1202" in self.Table.index else 0,
            "货币基金": sum(
                [
                    float(self.Table.replace("", float("nan"))["市值-本币"][x]) for x in self.Table.index
                    if (
                        ((x[:4] + "." + x[4:6] in _Cash["科目代码"].tolist()) and len(x) == 6)
                        or
                        ((".".join(x.split(".")[:2]) in _Cash["科目代码"].tolist()) and len(x) == 7)
                        or
                        (str(self.Table["科目名称"][x]).__contains__("货币") and self.Table["停牌信息"][x] != "")
                )
                ]
            )
        }
        return sum([x for x in result.values()])

    @property
    def Dividends(self) -> pandas.DataFrame:
        table = self.Table.loc[[x for x in self.Table.index if len(x) > 10 and x[:4] == "1203"]]
        table = self.__change_header(table.replace({"": float("nan")}))
        if len(table):
            table["科目名称"] = [self.__change_fund_name(x) for x in table["科目名称"]]
            return table.groupby("科目名称")["市值-本币"].sum()
        else:
            return pandas.DataFrame({"市值-本币": {}})["市值-本币"]

    @property
    def Liability(self):
        return (
                float(
                    (self.Table["市值-本币"]["2331"] if self.Table["市值-本币"]["2331"] else 0)
                    if "2331" in self.Table.index else 0) +
                float(
                    (self.Table["市值-本币"]["2206.01"] if self.Table["市值-本币"]["2206.01"] else 0)
                    if "2206.01" in self.Table.index else 0) +
                float(
                    (self.Table["市值-本币"]["2207"] if self.Table["市值-本币"]["2207"] else 0)
                    if "2207" in self.Table.index else 0) +
                float(
                    (self.Table["市值-本币"]["2211"] if self.Table["市值-本币"]["2211"] else 0)
                    if "2211" in self.Table.index else 0)
        )

    @property
    def Tax(self):
        return self.Table["市值-本币"]["2331"] if "2331" in self.Table.index else 0
