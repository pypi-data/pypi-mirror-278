# -*- coding: utf-8 -*-
import datetime
import os
import typing
import flask
import pandas
import pymongo
import chinese_calendar
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from pyecharts.charts import Line
from ZYYA_Codes.FOF_Analysis import Analysis_Results
from ZYYA_Codes.FOF_Analysis.Basic_Index import net_value_fetch
from ZYYA_Codes.utils.functions import Email_Update

CurrentConfig.GLOBAL_ENV = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates", "html"))
)


def latest_trade_day() -> datetime.date:
    now = datetime.datetime.now()
    date = now.date()
    if now.hour < 19:
        date -= datetime.timedelta(days=1)
    while not chinese_calendar.is_workday(date) and now.weekday() > 4:
        date -= datetime.timedelta(days=1)
    return date


class authentication(pymongo.MongoClient):
    def __init__(self, username, password, **kwargs):
        super().__init__(
            host=kwargs.get('host', 'localhost'),
            port=kwargs.get('port', 27017),
            authSource=kwargs.get('authSource', 'admin'),
            username=username,
            password=password
        )

    def is_connected(self):
        try:
            self.server_info()
            return True
        except:
            return False


class BasicServer(flask.Flask):
    Mongo_Client: authentication

    def __init__(self, name, **kwargs):
        super(BasicServer, self).__init__(name, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
        self.secret_key = b"QWERTYUIOP"


class Analysis_Results_R(Analysis_Results):
    def __init__(self, code, name, **kwargs):
        super().__init__(code, name, **kwargs)
        os.makedirs(os.path.join("outputs", "FOF_Analysis", self.Code), exist_ok=True)
        self.strategy_dict = self.get_strategies()

    def get_strategies(self) -> typing.Dict[str, str]:
        fund = set(self.get_all_securities()).union(self.Transactions["产品名称"].tolist())
        stored_dict = pandas.read_excel(
            os.path.join("outputs/FOF_Analysis", self.Code, "子基金策略.xlsx"), index_col=0
        )["细分策略"].to_dict() if "子基金策略.xlsx" in os.listdir(f"outputs/FOF_Analysis/{self.Code}") else {}
        new_dict = {x: stored_dict.get(x, None) for x in fund}
        return new_dict


def fof_routes(self: BasicServer):
    self.Analysis = None

    @self.route("/<user_name>/fof/logout", methods=["GET", "POST"])
    def fof_logout(user_name):
        flask.session.clear()
        return flask.redirect("/")

    @self.route('/<user_name>/fof', methods=['GET', 'POST'])
    def fof_page(user_name, **kwarg):
        if flask.session.get('logged_in') and flask.session.get('username') == user_name:
            if not flask.session.get("fof_list"):
                products = pandas.DataFrame(
                    [
                        x for x in self.Mongo_Client["CBS数据"]["产品净值"].find(
                        {
                            "产品名称": {"$regex": "中邮永安"}
                        },
                        {"产品名称": 1, "产品编号": 1, "_id": 0}
                    )
                    ]
                ).drop_duplicates().dropna().set_index("产品编号").sort_index()
                products = products.loc[[x for x in products.index if not 65 <= ord(x[-1]) <= 122]]
                _products: list = [" ".join([x, y]) for x, y in products["产品名称"].to_dict().items()]
                flask.session["fof_list"] = _products
            else:
                _products = flask.session.get("fof_list")
            msg = ('<div class="form-group">'
                   '<label for="fof" class="col-sm-2 control-label">'
                   '</label>'
                   '<div class="col-sm-8">'
                   '<a style="color: red">%s</a>'
                   '</div>'
                   '</div>' % kwarg.get("msg")) if kwarg.get("msg") else ""
            return Line().render_embed(
                template_name="./fof.html",
                user_name=user_name,
                product_list="\n".join(["<option>%s</option>" % x for x in _products]),
                start_date='<input type="date" value="%s-12-29" name="start_date">' % (
                        datetime.date.today().year - 1
                ),
                end_date='<input type="date" value="%s" name="end_date">' % datetime.date.today().strftime(
                    "%Y-%m-%d"
                ),
                msg=msg,
            )
        else:
            return flask.redirect("/")

    @self.route("/<user_name>/fof_analysis", methods=["GET", "POST"])
    def fof_analysis(user_name):
        if not flask.request.args.get("fof"):
            return fof_page(user_name, msg="请选择FOF产品名称")
        else:
            fof_code, fof_name = flask.request.args.get("fof").split(" ")
            start_date = datetime.datetime.strptime(flask.request.args.get("start_date"), "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(flask.request.args.get("end_date"), "%Y-%m-%d").date()
            initial_proportion = {
                x: float(flask.request.args.get(x)) / 100 if flask.request.args.get(x) else 1 / 6
                for x in ["指数增强", "市场中性", "另类套利", "主观CTA", "量化CTA", "固收"]
            }
            print(fof_code, fof_name, start_date, end_date, initial_proportion)
            self.Analysis = Analysis_Results_R(
                code=fof_code,
                name=fof_name,
                start=start_date,
                end=end_date,
                platform="web"
            )
            print(self.Analysis.get_all_securities())
            return flask.redirect('/%s/fof/strategy_confirm' % user_name)

    @self.route("/<user_name>/fof/strategy_confirm", methods=["GET", "POST"])
    def strategy_confirm(user_name):
        def options_generate(strategy: str):
            values = '\n'.join(['<option value="" hidden></option>'] + [
                '<option value="%s"%s>%s</option>' % (x, ' selected' if strategy == x else '', x)
                for x in ['主观CTA', '量化CTA', '市场中性', '指数增强', '另类套利', '固收', "货币基金"]
            ])
            return values

        shell = "\n".join([
            '<div class="form-group">',
            '<table border="1" class="table table-bordered">',
            '<thead valign="center" align="center">',
            '<tr align="center">',
            '<td width="150">产品名称</td>',
            '<td width="200">细分策略</td>',
            '</tr>',
            '</thead>',
            '<tbody align="center">',
            '{content}',
            '</tbody>',
            '</table>',
            '</div>', ]
        )

        contents = '\n\n'.join(
            [
                f'<tr>\n<td>{x}</td>\n<td>\n<select style="width: 100%" name="{x}">\n{options_generate(y)}\n</select>\n</td>\n</tr>'
                for x, y in self.Analysis.strategy_dict.items()
            ]
        )

        if flask.session.get('logged_in') and flask.session.get('username') == user_name:
            return flask.render_template("/html/fof_strategy_confirm.html").replace(
                '{components}', shell.format(content=contents)
            )
        else:
            return flask.redirect("/")

    @self.route("/<user_name>/fof/email_update", methods=["GET", "POST"])
    def email_update(user_name):
        if flask.session.get('logged_in') and flask.session.get('username') == user_name:
            Email_Update("tyb")
            return flask.redirect(f"/{user_name}/fof")
        else:
            return flask.redirect("/")

    @self.route("/<user_name>/fof/result_fetch", methods=["GET", "POST"])
    def result_fetch(user_name):
        strategies = pandas.DataFrame(index=list(flask.request.args.keys()))
        strategies["细分策略"] = flask.request.args.copy()
        strategies.to_excel(self.Analysis.Strategy_File_Route)
        self.Analysis.strategy_dict = self.Analysis.get_strategies()
        for x in flask.request.args.values():
            if not x:
                return flask.redirect(f"/{user_name}/fof/strategy_confirm")
        self.Analysis.set_PNL()
        self.Analysis.Page_Output(output=True)
        return flask.redirect(f"/{user_name}/fof/{self.Analysis.Code}")

    @self.route("/<user_name>/fof/<product>", methods=["GET", "POST"])
    def fof_result(user_name, product):
        if flask.session.get('logged_in') and flask.session.get('username') == user_name:
            return flask.send_from_directory(
                f"outputs/FOF_Analysis/{product}",
                f"{product} 业绩分析.html"
            )
        else:
            return flask.redirect("/")

    @self.route("/<user_name>/fof/nv_update", methods=["GET", "POST"])
    def fof_nv_update(user_name):
        index = net_value_fetch()
        index.get_nv()
        index.insert_net_values()
        del self.Analysis
        return flask.redirect("/%s/fof" % user_name)


def daily_data_routes(self: BasicServer):
    @self.route('/<user_name>/daily', methods=['GET', 'POST'])
    def daily(user_name):
        if flask.session.get('logged_in') and flask.session.get('username') == user_name:
            return flask.send_file(f"outputs/Daily_Data/产品与市场情况日报{latest_trade_day().strftime("%Y%m%d")}.pdf")
        else:
            return flask.redirect("/")

    @self.route('/<user_name>/daily/history/<date>', methods=['GET', 'POST'])
    def daily_history(user_name, date):
        if flask.session.get('logged_in') and flask.session.get('username') == user_name:
            return flask.send_file(f"outputs/Daily_Data/产品与市场情况日报{date}.pdf")
        else:
            return flask.redirect("/")


def home_routes(self: BasicServer):
    @self.route('/', methods=["GET", "POST"])
    def login_page():
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        if flask.request.method in ["GET", "HEAD"]:
            return flask.render_template("html/login page.html")
        else:
            self.Mongo_Client = authentication(
                username, password,
                host="122.224.101.242", port=27017, authSource=username
            )
            if self.Mongo_Client.is_connected():
                flask.session['username'] = username
                flask.session['password'] = password
                flask.session['logged_in'] = True
                return flask.redirect("/%s/home" % username)
            else:
                return flask.render_template('html/login page.html')

    @self.route('/<user_name>/home', methods=["GET", "POST"])
    def user_page(user_name):
        if flask.session.get('logged_in') and flask.session.get('username') == user_name:
            return flask.render_template('html/home page.html', user_name=user_name)
        else:
            return flask.redirect("/")

    @self.route('/<user_name>/logout', methods=["GET", "POST"])
    def logout_page(user_name):
        for key in list(flask.session.keys()):
            flask.session.pop(key, None)
        flask.session["logged_in"] = False
        return flask.redirect("/")


def web_assets(self: BasicServer):
    @self.route("/img/<img_name>", methods=['GET', 'POST'])
    def img(img_name):
        return flask.send_from_directory(os.path.join(self.template_folder, "img"), img_name)

    @self.route("/assets/jscodes/<js_name>", methods=['GET', 'POST'])
    def assets_jscodes(js_name):
        if not flask.session.get('logged_in'):
            return flask.redirect("/")
        else:
            return flask.send_from_directory(os.path.join(self.template_folder, "js_code"), js_name)

    @self.route("/assets/jscodes/fonts/<font_name>", methods=['GET', 'POST'])
    def assets_fonts(font_name):
        if not flask.session.get('logged_in'):
            return flask.redirect("/")
        else:
            return flask.send_from_directory(os.path.join(self.template_folder, "font"), font_name)


class Web_Server(BasicServer):
    def __init__(self, name):
        super(Web_Server, self).__init__(name)
        home_routes(self)
        web_assets(self)
        fof_routes(self)
        daily_data_routes(self)


if __name__ == '__main__':
    Web_Server(__name__).run("0.0.0.0", 5000)
