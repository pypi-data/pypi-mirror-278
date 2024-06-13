# -*- coding: utf-8 -*-
import datetime
import pandas
import typing
import chinese_calendar
import os
import configparser
import warnings
import pymongo
import imaplib
import imapclient.imap_utf7
import email.parser
import email.header
import chardet
import pytz
import requests
from ZYYA_Codes.utils.cons import *


def to_date(
        x: typing.Union[str, datetime.date, datetime.datetime,]
) -> datetime.date:
    """
    将任何格式的时间转化为日期
    :param x: 任何格式的时间
    :return: 日期
    """
    return pandas.to_datetime(x).date()


def to_datetime_localize(
        x: typing.Union[str, datetime.date, datetime.datetime,],
        timezone="Asia/Shanghai"
) -> datetime.date:
    """
    将任何格式的时间转化为日期
    :param timezone:
    :param x: 任何格式的时间
    :return: 日期
    """
    return pandas.to_datetime(x).astimezone(pytz.timezone(timezone))


def decode_str(str_in: str) -> str:
    """
    用于解析邮件中的文本
    :param str_in: 邮件内容
    :return: 可读文字
    """
    value, charset = email.header.decode_header(str_in)[0]
    if charset:
        try:
            value = value.decode(charset)
        except:
            value = value.decode("gbk")
    return value


def get_fridays(
        start: typing.Union[str, datetime.date, datetime.datetime,],
        end: typing.Union[str, datetime.date, datetime.datetime,]
) -> typing.List[datetime.date]:
    """
    获取给定时间段内每周的最后一个交易日
    :param start: 起始日期
    :param end: 终止日期
    :return:
    """
    from ZYYA_Codes.market_data_api import tushare_pro_api
    start = pandas.to_datetime(start).date()
    end = pandas.to_datetime(end).date()
    Calendar = tushare_pro_api.query("trade_cal", start_date=start.strftime("%Y%m%d"), end_date=end.strftime("%Y%m%d"))
    Calendar = [x.date() for x in Calendar[Calendar["is_open"] == 1]["cal_date"].astype("datetime64[ns]")]
    Calendar.sort()
    for date in Calendar.copy():
        if (date + datetime.timedelta(days=1) in Calendar
                or date + datetime.timedelta(days=2) in Calendar):
            Calendar.remove(date)
    Calendar.sort()
    return Calendar


def get_fridays_old(
        start: typing.Union[str, datetime.date, datetime.datetime,],
        end: typing.Union[str, datetime.date, datetime.datetime,]
) -> typing.List[datetime.date]:
    """
    获取给定时间段内每周的最后一个交易日
    :param start: 起始日期
    :param end: 终止日期
    :return:
    """
    Calendar = chinese_calendar.get_workdays(to_date(start), to_date(end))
    for date in Calendar.copy():
        if datetime.datetime.weekday(date) > 4:
            Calendar.remove(date)
    Calendar.sort()
    for date in Calendar.copy():
        if (date + datetime.timedelta(days=1) in Calendar
                or date + datetime.timedelta(days=2) in Calendar
                or chinese_calendar.is_workday(date + datetime.timedelta(days=1))):
            Calendar.remove(date)
    Calendar.sort()
    return Calendar


def set_configs(**kwargs) -> None:
    """
    设置全局参数
    """
    path = os.path.expanduser("~")
    configfile_path = os.path.join(path, CONFIG_FILENAME)
    config = configparser.ConfigParser()
    config.read(configfile_path, encoding="utf-8")
    data: typing.Dict[str, dict] = {x: {y: z for y, z in config[x].items()} for x in config.sections()}

    Company_ip = kwargs.get("Company_ip", None)
    Tushare_token = kwargs.get("Tushare_token", None)
    MongoDB_port = kwargs.get("MongoDB_port", None)
    MongoDB_username = kwargs.get("MongoDB_username", None)
    MongoDB_password = kwargs.get("MongoDB_password", None)
    GeShang_cookies = kwargs.get("GeShang_cookies")

    def email_info(info) -> typing.Union[typing.Dict[str, str], None]:
        if isinstance(info, dict):
            username = info.get("username", None)
            password = info.get("password", None)
            if username and password:
                return {
                    "username": str(username),
                    "password": str(password),
                }
            else:
                raise ValueError("账户名或密码缺失，请重新输入")
        elif not info:
            return None
        else:
            raise TypeError("邮箱账号密码输入格式有误")

    TYB_email = email_info(kwargs.get("tyb_email_info"))
    YYB_email = email_info(kwargs.get("yyb_email_info"))

    data.update(
        {
            "tushare_token": {
                "token": Tushare_token
            },
            "Company_Info": {
                "host": Company_ip,
                "domain": COMPANY_DOMAIN
            },
            "YYB_Email": YYB_email,
            "TYB_Email": TYB_email,
            "MongoDB": {
                "host": Company_ip,
                "port": MongoDB_port,
                "username": MongoDB_username,
                "password": MongoDB_password
            },
            "GeShang": {"cookies": GeShang_cookies}
        }
    )
    for section, pairs in data.items():
        if section not in config.sections() and pairs:
            config.add_section(section)
        if pairs and isinstance(pairs, dict):
            for key, value in pairs.items():
                if value and isinstance(value, typing.Union[str]):
                    config.set(section, key, value)
                    print(section, key, value)
                elif value and not isinstance(value, typing.Union[str]):
                    warnings.warn("'%s==%s==%s' 参数未被录入， 请输入文本格式再次尝试" % (section, key, value))

    file = open(configfile_path, mode="w", encoding="utf-8")
    config.write(file)
    file.close()


def get_configs() -> typing.Dict[str, typing.Dict[str, str]]:
    """
    查看全局参数
    """
    path = os.path.expanduser("~")
    configfile_path = os.path.join(path, CONFIG_FILENAME)
    config = configparser.ConfigParser()
    config.read(configfile_path, encoding="utf-8")
    return {x: {y: z for y, z in config[x].items()} for x in config.sections()}


def Mongo_Client() -> pymongo.MongoClient:
    """连接MongoDB客户端"""
    _config = get_configs()
    return pymongo.MongoClient(
        host=_config.get("MongoDB", {}).get("host", None),
        port=int(_config.get("MongoDB", {}).get("port", None)),
        username=_config.get("MongoDB", {}).get("username", None),
        password=_config.get("MongoDB", {}).get("password", None),
    )


def Email_Update(username: str, **kwargs) -> None:
    _config = get_configs()
    conn = imaplib.IMAP4_SSL("imap.qiye.163.com", 993)
    Client = Mongo_Client()
    if username == "tyb" and isinstance(username, str):
        print(
            conn.login(
                _config.get("TYB_Email", {}).get("username", None),
                _config.get("TYB_Email", {}).get("password", None),
            )
        )
        run = 1
        Email = Client["CBS数据"]["投研部邮箱"]
    elif username == "yyb" and isinstance(username, str):
        print(
            conn.login(
                _config.get("YYB_Email", {}).get("username", None),
                _config.get("YYB_Email", {}).get("password", None),
            )
        )
        run = 1
        Email = Client["CBS数据"]["运营部邮箱"]
    else:
        run = 0
    while kwargs.get("stoptime", 10) >= run >= 1:
        try:
            for Folder in conn.list()[1]:
                if (imapclient.imap_utf7.decode(Folder).split('"|"')[0].split(' ')[-1].split('"')[1] in
                        kwargs.get("folders", [
                            imapclient.imap_utf7.decode(x).split('"|"')[0].split(' ')[-1].split('"')[1]
                            for x in conn.list()[1]
                        ])
                ):
                    _, mails = conn.select(Folder.decode("utf8").split(" ")[-1].split('"')[1], readonly=True)
                    print(imapclient.imap_utf7.decode(Folder).split('"|"')[0].split(' ')[-1].split('"')[1])
                    if imapclient.imap_utf7.decode(Folder).split('"|"')[0].split(' ')[-1].split('"')[1] not in ["草稿箱",
                                                                                                                "垃圾邮件",
                                                                                                                "已删除"]:
                        Exist = [x["序号"] for x in
                                 Email.find(
                                     {"文件夹":
                                          imapclient.imap_utf7.decode(Folder).split('"|"')[0].split(' ')[-1].split('"')[1]},
                                     {"序号": 1}
                                 )
                                 ]
                        To_fetch = set(list(range(1, int(mails[0].decode('gbk')) + 1)))
                        To_fetch = list(To_fetch.difference(set(Exist)))
                        To_fetch.sort()
                        for index in To_fetch[::-1]:
                            resp, data = conn.fetch(str(index).encode("gbk"), "(RFC822)")
                            try:
                                msg_content = data[0][-1].decode(chardet.detect(data[0][-1])['encoding'])
                            except:
                                try:
                                    msg_content = data[0][-1].decode("ISO-8859-1")
                                except:
                                    msg_content = data[0].decode("ISO-8859-1")
                            msg = email.parser.Parser().parsestr(msg_content)
                            Email.insert_one({"序号": index,
                                              "发件人": decode_str(msg.get("From")) if msg.get("From") else "",
                                              "收件人": decode_str(msg.get("To")) if msg.get("To") else "",
                                              "抄送": decode_str(msg.get("cc")) if msg.get("cc") else "",
                                              "发件时间": to_datetime_localize(
                                                  decode_str(msg.get("date")).split(", ")[-1].split(" (")[0]) if msg.get(
                                                  "date") else "",
                                              "主题": decode_str(msg.get("Subject")) if msg.get("Subject") else "",
                                              "附件": [
                                                  decode_str(item.get_param("name")) for item in msg.walk()
                                                  if
                                                  item.get_param("name") and (type(item.get_param("name")) == str or type(
                                                      item.get_param("name")
                                                  ) == bytes)],
                                              "文件夹":
                                                  imapclient.imap_utf7.decode(Folder).split('"|"')[0].split(' ')[-1].split(
                                                      '"')[
                                                      1]})

                            print("---邮件数据更新中---",
                                  imapclient.imap_utf7.decode(Folder).split('"|"')[0].split(' ')[-1].split('"')[1],
                                  index,
                                  to_datetime_localize(
                                      decode_str(msg.get("date")).split(", ")[-1].split(" (")[0]) if msg.get(
                                      "date") else "",
                                  decode_str(msg.get("Subject")) if msg.get("Subject") else "")
            run = 0
        except:
            print("已运行%1.0f次" % run)
            run += 1


def Trade_Date(start, end):
    Calendar = chinese_calendar.get_workdays(
        pandas.to_datetime(start).date(),
        pandas.to_datetime(end).date()
    )
    for date in Calendar.copy():
        if datetime.datetime.weekday(date) > 4:
            Calendar.remove(date)
    Calendar.sort()
    for date in Calendar.copy():
        if date + datetime.timedelta(days=1) in Calendar:
            Calendar.remove(date)
    return Calendar


def Trade_Date_TS(
        start: typing.Union[str, datetime.date, datetime.datetime],
        end: typing.Union[str, datetime.date, datetime.datetime],
) -> typing.List[datetime.date]:
    from ZYYA_Codes.market_data_api import tushare_pro_api
    start = pandas.to_datetime(start).date()
    end = pandas.to_datetime(end).date()
    Calendar = tushare_pro_api.query("trade_cal", start_date=start.strftime("%Y%m%d"), end_date=end.strftime("%Y%m%d"))
    trade_dates = [x.date() for x in Calendar[Calendar["is_open"] == 1]["cal_date"].astype("datetime64[ns]")]
    trade_dates.sort()
    for date in trade_dates.copy():
        if date + datetime.timedelta(days=1) in trade_dates:
            trade_dates.remove(date)
    return trade_dates


def Email_Client():
    return imaplib.IMAP4_SSL("imap.qiye.163.com", 993)


def GESHANG_NetValue(code: str) -> pandas.Series:
    Referer = GESHANG_PRODUCT_REFERER + code
    headers = {
        "Referer": Referer,
        "Cookie": get_configs()["GeShang"]["cookies"],
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 Safari/537.36'
    }
    payload_i = {
        "product_id": code,
        "index_name": "NH0100.NH",
        "is_excess_returns": "false"
    }
    s = requests.session()
    data = s.post(GESHANG_URL, json=payload_i, headers=headers).json()
    net_value = dict(data).get("result")
    if net_value:
        result = pandas.DataFrame(net_value["netvalue"])
        result["trading_date"] = result["trading_date"].astype("datetime64[ns]")
        result = result[["rehabilitation_nv", "trading_date"]].rename(
            columns={"rehabilitation_nv": "复权净值", "trading_date": "日期"}
        )
        return result.set_index("日期")["复权净值"].astype(float)
    else:
        return None


__all__ = [
    "get_fridays",
    "to_date",
    "to_datetime_localize",
    "Mongo_Client",
    "get_configs",
    "set_configs",
    "Email_Update",
    "Trade_Date",
    "decode_str",
    "GESHANG_NetValue"
]


def Balance_Sheet_Download(**kwargs) -> pandas.DataFrame:
    account = kwargs.get("account", "tyb")
    start = kwargs.get("start", "20231229")
    # Downloaded = pandas.DataFrame(
    #     [x for x in Mongo_Client()["CBS数据"]["产品估值表"].find({}, {"_id": 0, "文件名称": 1})]
    # )
    Emails = pandas.DataFrame(
        [
            x for x in Mongo_Client()["CBS数据"]["投研部邮箱" if account == "tyb" else "运营部邮箱"].find(
                {"发件时间": {"$gte": pandas.to_datetime(start)}}, {"_id": 0}
            )
        ]
    )
    Emails = Emails[Emails["主题"].str.contains("估值表")]
    Emails = Emails.loc[
        [
            x for x in Emails.index
            if sum(
                [
                    y.__contains__("估值表") and y.__contains__("中邮永安") and y.__contains__("S") and y.__contains__("xls")
                    for y in Emails["附件"][x]
                ]
            )
        ]
    ]
    downloaded = [x["文件名称"] for x in Mongo_Client()["CBS数据"]["产品估值表"].find({}, {"_id": 0, "文件名称": 1})]
    IMAP_Client = Email_Client()
    _config = get_configs()
    IMAP_Client.login(
        _config.get("TYB_Email", {}).get("username", None),
        _config.get("TYB_Email", {}).get("password", None),
    )
    for folder, order, attachments in zip(Emails["文件夹"], Emails["序号"], Emails["附件"]):
        print(folder, order, attachments)
        try:
            result = Email_Attachment_Download(IMAP_Client, folder, order)
            if result["文件名称"] in downloaded and result.get("产品代码", None):
                Mongo_Client()["CBS数据"]["产品估值表"].insert_one(Email_Attachment_Download(IMAP_Client, folder, order))
        except:
            IMAP_Client = Email_Client()
            IMAP_Client.login(
                _config.get("TYB_Email", {}).get("username", None),
                _config.get("TYB_Email", {}).get("password", None),
            )
            result = Email_Attachment_Download(IMAP_Client, folder, order)
            if result["文件名称"] in downloaded and result.get("产品代码", None):
                Mongo_Client()["CBS数据"]["产品估值表"].insert_one(Email_Attachment_Download(IMAP_Client, folder, order))
    return Emails


def Email_Attachment_Download(
        email_client: imaplib.IMAP4_SSL,
        folder: str,
        order: int,
):
    email_client.select(folder, readonly=True)
    _, data = email_client.fetch(str(order).encode("utf8"), "(RFC822)")
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
                    result = {"文件名称": filename, "文件内容": content}
                    result.update(name_info_extract(filename))
                    return result


def name_info_extract(name: str):
    S_start = name.find("S")
    code = name[S_start: S_start + 6]
    if code == "SJJ179":
        return {}
    else:
        name = name.replace(code, "")
        ZYYA = name.find("中邮永安")
        JJ = name.find("基金")
        name = name.replace(name[ZYYA: JJ + 2], "").replace("4级", "")
        date = pandas.to_datetime("".join([x for x in name if 48 <= ord(x) < 58])[-8:])
        return {"产品代码": code, "日期": date}
