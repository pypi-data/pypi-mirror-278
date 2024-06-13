"""
工具库
"""

import asyncio
import time
import datetime
import calendar
import os
import platform
import json
import random
import re
import hashlib
import base64
from functools import wraps
from typing import Callable
from threading import Timer
import urllib.parse as url
from urllib.parse import (
    urljoin,
    urlparse,
    urlunparse,
    urlencode,
    urlsplit,
    urlunsplit,
    unquote,
    unquote_plus,
    unwrap,
    quote,
    parse_qs,
    parse_qsl,
)
import httpx
from loguru import logger
from faker import Faker
from rich import print, print_json, inspect
from rich.console import Console, Group
from rich.progress import Progress, track
from rich.padding import Padding
from rich.columns import Columns
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.status import Status
from rich.table import Table
from rich.pretty import pprint
from bs4 import BeautifulSoup, element
import html2text
from parsel import Selector
from dateutil.parser import parse as timeparse

if platform.machine() != "aarch64":
    from dateparser import parse as timeparse2
else:
    timeparse2 = None


__all__ = [
    "async_httpx",
    "asyncio",
    "base64_decode",
    "base64_encode",
    "bs_get_text",
    "bs_get_text2",
    "bs_html",
    "console",
    "clear",
    "Columns",
    "connect_to_mongodb",
    "date_next",
    "fake",
    "fromtimestamp",
    "get_proxies",
    "Group",
    "hashlib",
    "html2md",
    "inspect",
    "httpx",
    "listdir",
    "logger",
    "load_ipython_extension",
    "Markdown",
    "md5",
    "mongodb",
    "mongo_tongji",
    "now",
    "os",
    "oss2_find_file",
    "Panel",
    "parse_qs",
    "parse_qsl",
    "Padding",
    "pdf2text",
    "pprint",
    "print",
    "print_json",
    "print_exception",
    "printx",
    "Progress",
    "quote",
    "randint",
    "random",
    "re",
    "read_json",
    "retry",
    "Rule",
    "send_bot",
    "sleep",
    "sleep_progress",
    "Status",
    "Selector",
    "Table",
    "text2png",
    "time_next",
    "timeit",
    "timeparse",
    "timestamp",
    "to_excel",
    "to_json",
    "to_async",
    "today",
    "tongji_content",
    "track",
    "ua",
    "unquote",
    "unquote_plus",
    "unwrap",
    "url",
    "urlencode",
    "urljoin",
    "urlparse",
    "urlsplit",
    "urlunsplit",
    "urlunparse",
    "wait",
]

if timeparse2:
    __all__.append("timeparse2")

NON_BREAKING_ELEMENTS = [
    "a",
    "abbr",
    "acronym",
    "audio",
    "b",
    "bdi",
    "bdo",
    "big",
    "button",
    "canvas",
    "cite",
    "code",
    "data",
    "datalist",
    "del",
    "dfn",
    "em",
    "embed",
    "font",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "label",
    "map",
    "mark",
    "meter",
    "noscript",
    "object",
    "output",
    "picture",
    "progress",
    "q",
    "ruby",
    "s",
    "samp",
    "script",
    "select",
    "slot",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "svg",
    "template",
    "textarea",
    "time",
    "u",
    "tt",
    "var",
    "video",
    "wbr",
]
BLOCK_TAGS = [
    "p",
    "div",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "table",
    "tr",
    "thead",
    "tbody",
    "tfoot",
    "form",
]

fake = Faker()
fake.zh = Faker("zh")  # type: ignore
console = Console()
print_exception = console.print_exception


def to_async(func: Callable) -> Callable:
    """
    同步函数转异步，装饰器或直接调用

    func: 函数
    """

    @wraps(func)
    def async_func(*args, **kwargs):
        return asyncio.to_thread(func, *args, **kwargs)

    return async_func


class async_httpx:
    """
    简化httpx异步调用
    """

    get = to_async(httpx.get)
    post = to_async(httpx.post)
    put = to_async(httpx.put)
    head = to_async(httpx.head)
    patch = to_async(httpx.patch)
    delete = to_async(httpx.delete)
    options = to_async(httpx.options)


def bs_html(
    markup: str = "",
    features: str = "lxml",
    builder=None,
    parse_only=None,
    from_encoding=None,
    exclude_encodings=None,
    element_classes=None,
):
    """
    使用 BeautifulSoup 解析网页

    markup: 网页源码
    features: 默认使用 lxml 解析
    """
    return BeautifulSoup(
        markup=markup,
        features=features,
        builder=builder,
        parse_only=parse_only,
        from_encoding=from_encoding,
        exclude_encodings=exclude_encodings,
        element_classes=element_classes,
    )


def load_ipython_extension(ip=None):
    from rich.pretty import install
    from rich.traceback import install as tr_install

    install()
    tr_install()


def bs_get_text(
    soup,
    strip_tags: list = ["style", "script", "code"],
) -> str:
    """
    基于 BeautifulSoup 提取网页文本v1

    soup: BeautifulSoup 对象或html文本
    strip_tags: 需要删除的节点
    """
    if isinstance(soup, str):
        soup = bs_html(soup)
    for node in soup(strip_tags):
        node.extract()
    for node in soup.find_all():
        if node.name not in NON_BREAKING_ELEMENTS:
            node.append("\n") if node.name == "br" else node.append("\n\n")
    return (
        re.sub("\n\n+", "\n\n", soup.get_text())
        .strip()
        .replace("\xa0", " ")
        .replace("\u3000", " ")
    )


def bs_get_text2(
    soup,
    strip_tags: list = ["style", "script", "code"],
):
    """
    基于 BeautifulSoup 提取网页文本v2

    soup: BeautifulSoup 对象或html文本
    """
    if isinstance(soup, str):
        soup = bs_html(soup)
    for node in soup(strip_tags):
        node.extract()

    def traverse(node):
        if isinstance(node, element.NavigableString):
            if node.strip():
                yield node.strip()
        else:
            if node.name in BLOCK_TAGS:
                yield "\n"
            for child in node.children:
                yield from traverse(child)
            if node.name in BLOCK_TAGS:
                yield "\n"

    parsed = "".join(traverse(soup)).strip().replace("\xa0", " ").replace("\u3000", " ")
    return parsed


def base64_encode(string: bytes | str):
    """
    base64编码
    """
    if isinstance(string, str):
        string = string.encode()
    return base64.b64encode(string).decode()


def base64_decode(string: bytes | str):
    """
    base64解码
    """
    if isinstance(string, str):
        string = string.encode()
    return base64.b64decode(string).decode()


def mongodb(
    host,
    database,
    port: int | None = None,
):
    """
    连接 MongoDB

    host: mongo 链接
    database: 数据库名称
    port: mongo 端口

    host 有密码格式: "mongodb://username:password@192.168.0.1:27017/"
    host 无密码格式: "mongodb://192.168.0.1:27017/"
    """
    from pymongo import MongoClient

    try:
        # 连接到 MongoDB
        client = MongoClient(host, port)
        db = client[database]
        db.list_collection_names()
        logger.success(f"MongoDB 成功连接到 {database}")
        return db
    except Exception as e:
        logger.error("MongoDB 连接失败:", str(e))
        return None


connect_to_mongodb = mongodb


def mongo_tongji(
    mongodb,
    prefix: str = "",
    tongji_collection: str = "tongji",
) -> dict:
    """
    统计 mongodb 每个集合的`文档数量`

    mongodb: mongo 库
    prefix: mongo 表前缀, 默认空字符串可以获取所有表, 字段名称例如 `统计_20240101`。
    tongji_collection: 统计表名称，默认为 tongji
    """

    tongji = mongodb[tongji_collection]
    key = prefix if prefix else f"统计_{now(7)}"
    collection_count_dict = {
        **(
            tongji.find_one({"key": key}).get("count")
            if tongji.find_one({"key": key})
            else {}
        ),
        **(
            {
                i: mongodb[i].estimated_document_count()
                for i in mongodb.list_collection_names()
                if i.startswith(prefix)
            }
        ),
    }
    tongji.update_one(
        {"key": prefix if prefix else f"统计_{now(7)}"},
        {"$set": {"count": collection_count_dict}},
        upsert=True,
    )
    return dict(sorted(collection_count_dict.items()))


def clear():
    """
    清屏
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def get_proxies(n: int = 1, httpx: bool = False):
    """
    ## 随机返回代理

    需要先配置环境变量 HTTP_PROXY_DICT,  使用 to_json 将 HTTP_PROXY_DICT 转换成 json

    n: 代理选择，数字或对应的字符串
    """
    http_proxy_dict_str = os.getenv("HTTP_PROXY_DICT", "")
    if not http_proxy_dict_str:
        print("未配置 HTTP_PROXY_DICT")
        raise Exception()
    proxyurl = random.choice(read_json(http_proxy_dict_str).get(str(n)))
    if httpx:
        proxies = {
            "http://": proxyurl,
            "https://": proxyurl,
        }
    else:
        proxies = {
            "http": proxyurl,
            "https": proxyurl,
        }
    return proxies


def listdir(path=None, key=None, reverse: bool = False):
    """
    help(os.listdir)

    path: 目录路径
    key: 排序方式
    reverse: 指定是否反转, 默认否。
    """
    return sorted(
        os.listdir(path),
        key=key,
        reverse=reverse,
    )


def html2md(
    string: str,
    ignore_links: bool = True,
    ignore_images: bool = True,
    ignore_tables: bool = True,
) -> str:
    """
    ## HTML 转 Markdown

    默认忽略链接、忽略图像、忽略表格
    """
    converter = html2text.HTML2Text()
    converter.ignore_links = ignore_links  # 忽略链接
    converter.ignore_images = ignore_images  # 忽略图像
    converter.ignore_tables = ignore_tables  # 忽略表格
    if ignore_tables:
        string = re.sub("<table.*?</table>", "", string)
    content = converter.handle(string)
    return content


def md5(string: bytes | str):
    if isinstance(string, str):
        string = string.encode()
    result = hashlib.md5(string).hexdigest()
    return result


def now(fmt_type: int | None = None, fmt: str | None = None):
    """
    默认返回当前时间, 精度到秒。

    fmt_type: 格式化类型。
    fmt: 通过 strformat 格式化。

    - fmt=None -> datetime.datetime(2024, 1, 18, 11, 44, 57)
    - fmt_type=1 -> "2024-01-18 11:44:57"
    - fmt_type=2 -> 1705549497 # 10位时间戳
    - fmt_type=3 -> 1705555472772 # 13位时间戳
    - fmt_type=4 -> datetime.date(2024, 1, 18)
    - fmt_type=5 -> "2024-01-18"
    - fmt_type=6 -> "2024/01/18"
    - fmt_type=7 -> "20240118"
    """
    if fmt:
        return datetime.datetime.now().strftime(fmt)
    if fmt_type == 1:
        return f"{datetime.datetime.now().replace(microsecond=0)}"
    elif fmt_type == 2:
        return int(time.time())
    elif fmt_type == 3:
        return int(time.time() * 1000)
    elif fmt_type == 4:
        return datetime.date.today()
    elif fmt_type == 5:
        return f"{datetime.date.today()}"
    elif fmt_type == 6:
        return f"{datetime.date.today():%Y/%m/%d}"
    elif fmt_type == 7:
        return f"{datetime.date.today():%Y%m%d}"
    else:
        return datetime.datetime.now().replace(microsecond=0)


def printx(*objects, sep: str = " ", end: str = "\n"):
    """
    增加随机颜色的print
    """
    for i in objects[:-1]:
        print(
            f"[{fake.color()}]{i}[/]" if isinstance(i, str) else i,
            sep=sep,
            end=sep,
        )
    print(
        f"[{fake.color()}]{objects[-1]}[/]"
        if isinstance(objects[-1], str)
        else objects[-1],
        sep=sep,
        end=end,
    )


def timestamp(n: int = 10):
    """
    返回时间戳

    n 可选 10位和13位。
    """
    if n == 13:
        return int(time.time() * 1000)
    return int(time.time())


def today(fmt_type=None):
    """
    返回今天日期

    - fmt=1 -> "2024-01-18"
    - fmt=2 -> "2024/01/18"
    - fmt=3 -> "20240118"
    """
    if not fmt_type:
        return datetime.date.today()
    if fmt_type == 1:
        return f"{datetime.date.today()}"
    elif fmt_type == 2:
        return f"{datetime.date.today():%Y/%m/%d}"
    elif fmt_type == 3:
        return f"{datetime.date.today():%Y%m%d}"


def tongji_content(
    content: str,
    keywords: list[str],
    strict=False,
    to_dict=False,
):
    """
    统计每篇文章中关键词出现次数

    - content: 需要统计的文本。
    - keywords: 需要统计的关键词。
    - strict: 是否严格模式，默认False 忽略大小写, True 不忽略。
    - to_dict: 是否导出为字典格式。
    """
    keyword_tongji_list = []
    for keyword in set(keywords):
        if not strict:
            p1 = content.upper().count(keyword.upper())
        else:
            p1 = content.count(keyword)
        if p1 > 0:
            keyword_tongji_list.append([keyword, p1])
    if to_dict:
        return dict(keyword_tongji_list)
    return [
        f"{k[0]}({k[1]})"
        for k in sorted(
            keyword_tongji_list,
            key=lambda x: x[-1],
            reverse=True,
        )
    ]


def date_next(
    days: int = 0,
    weeks: int = 0,
    date: datetime.date | None = None,
):
    """
    返回下一个的日期, 默认为0, 负数为过去, 正数为未来。
    """
    if not date:
        date = datetime.date.today()
    return date + datetime.timedelta(days=days, weeks=weeks)


def time_next(
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    weeks: int = 0,
    months: int = 0,
    years: int = 0,
    start: tuple | datetime.datetime | None = None,
    fmt: str | None = None,
):
    """
    返回下一个的时间, 默认为0, 负数为过去, 正数为未来。先算月份再算年, 然后依次计算。

    - days: 偏移天数
    - hours: 偏移小时数
    - minutes: 偏移分钟数
    - seconds: 偏移秒数
    - weeks: 偏移周数
    - months: 偏移月数
    - years: 偏移年数
    - start: 开始时间, (2024, 1, 20, 10, 12, 23) 或者 datetime.datetime(2024, 1, 20, 10, 12, 23)
    - fmt: 指定输出格式。
    """
    if start:
        if not isinstance(start, datetime.datetime):
            start = datetime.datetime(*start)
    else:
        start = datetime.datetime.now().replace(microsecond=0)
    if months:
        # 获取下个时间的年份和月份
        next_year = start.year + (start.month == 12)
        next_month = start.month + months
        if next_month > 12:
            next_year += next_month // 12
            next_month = next_month % 12
        if next_month < 1:
            next_year -= abs(next_month) // 12 + 1
            next_month = 12 - abs(next_month) % 12

        # 获取下个时间的最大天数
        next_month_max_day = calendar.monthrange(next_year, next_month)[1]
        start = start.replace(
            year=next_year, month=next_month, day=min(start.day, next_month_max_day)
        )
    if years:
        real_next_year = start.year + 1
        next_month_max_day = calendar.monthrange(real_next_year, start.month)[1]
        start = start.replace(
            year=real_next_year,
            month=start.month,
            day=min(start.day, next_month_max_day),
        )
    results = start + datetime.timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        weeks=weeks,
    )
    if fmt:
        return results.strftime(fmt)
    else:
        return results


def sleep(n: int):
    """
    等待n秒, 模拟阻塞
    """
    return time.sleep(n)


def sleep_progress(n: int = 1, info=None, transient=False):
    """
    等待n秒, 模拟阻塞, 进度条。

    n: 等待秒数
    info: 定制输出信息
    transient: 运行完是否隐藏
    """
    if not info:
        info = f"等待{n}秒"
    for _ in track(range(int(n // 0.02)), info, transient=transient):
        time.sleep(0.02)


def fromtimestamp(t: int | str):
    """
    从时间戳返回 datetime 格式, 自动判断字符串和数字, 不符合格式要求会原样返回。
    """
    _t = t
    if isinstance(t, str) and t.isdigit():
        t = int(t[:10])
    if isinstance(t, (int, float)):
        return datetime.datetime.fromtimestamp(int(str(t)[:10]))
    return _t


def read_json(filepath, encoding="utf-8"):
    """
    JSON 反序列化, 读取 JSON 文件

    path_string: JSON 文件路径或字符串
    """
    if not os.path.isfile(filepath):
        return json.loads(filepath)
    with open(filepath, "r", encoding=encoding) as f:
        q = json.load(f)
    return q


def to_json(
    obj,
    filename=None,
    encoding="utf-8",
    ensure_ascii: bool = False,
    indent: int | None = None,
    separators: tuple | None = None,
):
    """
    JSON 序列化, 将Python 对象写入文件或转换为字符串。

    filename: JSON 文件路径
    indent: 缩进
    ensure_ascii: 默认不转为unicode
    separators: 分隔符, 默认为 (", ", ": ")
    """
    if not filename:
        return json.dumps(
            obj,
            indent=indent,
            ensure_ascii=ensure_ascii,
            separators=separators,
        )
    else:
        with open(filename, "w", encoding=encoding) as f:
            json.dump(
                obj,
                f,
                indent=indent,
                ensure_ascii=ensure_ascii,
                separators=separators,
            )


def to_excel(
    df,  # type: ignore
    path: str,
    mode: str = "w",
    index: bool = False,
    engine: str = "xlsxwriter",
):
    """
    ## 导出 excel

    - df: dataframe 对象, 多个sheet可以通过字典传入, 键为sheet名称。`{"sheet_name1": df1, "sheet_name2": df2}`
    - path: 文件保存路径
    - mode: 默认 `w` 为全新写入; 如果为 `a` 则为插入, 引擎会改为 openpyxl。
    - strings_to_urls: 默认不转换url
    - index: 默认不导出索引
    - engine: 默认引擎使用xlsxwriter, 其他选项有 'auto'、'openpyxl'、'odf'
    """
    import pandas as pd

    df: dict[str, pd.DataFrame] | pd.DataFrame

    if engine == "xlsxwriter":
        engine_kwargs = {"options": {"strings_to_urls": False}}

    if mode == "a":
        engine = "openpyxl"
        engine_kwargs = None

    with pd.ExcelWriter(
        path,
        engine=engine,  # type: ignore
        mode=mode,  # type: ignore
        engine_kwargs=engine_kwargs,
    ) as writer:
        if isinstance(df, dict):
            for sheet in df:
                df.get(sheet).to_excel(writer, index=index, sheet_name=sheet)  # type: ignore
        else:
            df.to_excel(writer, index=index)


def retry(
    num: int = 3,
    log: bool = False,
    show_error: bool = False,
):
    """
    ## 重试

    - num: 默认重试 3 次。
    - log: 默认不展示日志。
    - show_error: 默认不返回错误, 线程池打开可以更好的统计。

    ```python
    import requests

    @retry(5)
    def craw():
        url = "https://www.google.com"
        res = requests.get(url, timeout=2)
        print(res)
    ```
    """

    def wrap(f):
        @wraps(f)
        def func(*args, **kwargs):
            error_list = []
            for i in range(num):
                try:
                    if log:
                        logger.info(f"函数 {f.__name__} | 第 {i+1}/{num} 次运行")
                    return f(*args, **kwargs)
                except Exception as e:
                    error_list.append(e)
                    if log:
                        logger.error(f"运行失败: {e}")
            if show_error:
                raise error_list[-1]

        return func

    return wrap


def send_bot(
    content: str = "测试",
    bot_key: str = "",
    msgtype: str = "markdown",
    filepath: str | None = None,
    mentioned_list: list = [],
):
    """
    企业微信群机器人, 基础的 Mardkown 语法。

    <font color="info">绿色</font>
    <font color="comment">灰色</font>
    <font color="warning">橙红色</font>

    content: 文本
    bot_key: 微信机器人key, 也可以设置环境变量 BOT_KEY 自动读取, 参数权重高于环境变量。
    msgtype: 类型, 包括 markdown, text, file, voice, image
    filepath: 文件路径，非文本类型使用。
    mentioned_list: 提醒用户列表, 填入手机号或 "@all", 仅支持 text 类型。
    """
    if msgtype not in ["markdown", "text", "file", "voice", "image"]:
        raise NameError('类型仅支持 "markdown", "text", "file", "voice", "image"')
    if not bot_key:
        bot_key = os.getenv("BOT_KEY", "")
        if not bot_key:
            print("未全局配置 BOT_KEY，也未填写参数 bot_key")
            raise Exception("请填写 bot_key")
    if "key=" in bot_key:
        raise Exception("bot_key 只需要填入 `key=` 后面的部分")
    if msgtype == "file" or msgtype == "voice":
        file_upload_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={bot_key}&type=file"
        files = {filepath.rsplit(".", 1)[0]: open(filepath, "rb")}  # type: ignore
        resp = httpx.post(file_upload_url, files=files)
        msg = {"media_id": resp.json().get("media_id")}
    elif msgtype == "image":
        content = open(filepath, "rb").read()  # type: ignore
        msg = {"base64": base64_encode(content), "md5": md5(content)}
    elif msgtype == "text":
        msg = {"content": content, "mentioned_mobile_list": mentioned_list}
    else:
        msg = {"content": content}
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={bot_key}"
    json_data = {
        "msgtype": msgtype,
        msgtype: msg,
    }
    response = httpx.post(url, json=json_data)
    return response


def oss2_find_file(bucket, prefix, size1=0, size2=1048576000):
    """
    寻找 oss 文件, 指定 size1 和 size2 可以筛选特定大小的文件。默认单位为 KB。返回值为字典。

    - 可以通过 len 统计文件数量。
    - 可以通过 sum 统计返回值字典的 values 统计文件夹文件的总大小, 单位为KB。

    bucket: oss2.Bucket 对象
    prefix: 文件夹路径, 例如 'etl/atk'
    size1: 文件大小下限,默认0
    size2: 文件大小上限,默认 1000G；如果需要筛选无用pdf, 可以设置上限20。
    """
    import oss2

    if not isinstance(bucket, oss2.Bucket):
        print("bucket 不符合要求")
        return
    d = {}
    for obj in oss2.ObjectIterator(bucket, prefix):
        t = obj.size / 1024
        if size1 < t < size2 and not obj.is_prefix():
            print(f"文件名:{obj.key}  文件大小: {t:.2f} KB")
            d[obj.key] = t
    return d


def pdf2text(filepath):
    """
    从 pdf 提取文本内容

    filepath: 文件路径
    """
    from pypdf import PdfReader

    reader = PdfReader(filepath)
    content = "".join([i.extract_text() for i in reader.pages])
    return content


def randint(a: int, b: int):
    """
    返回随机数, [a, b]前后包含。
    """
    return random.randint(a, b)


def timeit(function):
    """
    计时器

    ```
    @timeit
    def hello():
        time.sleep(5)
    ```
    """

    @wraps(function)
    def func(*args, **kwargs):
        t0 = time.time() * 1000
        result = function(*args, **kwargs)
        print(f"运行 {function.__name__} 耗时: {time.time() * 1000 - t0:.2f} ms")
        return result

    return func


def ua(version_from=101, version_to=125):
    """
    随机ua

    chrome 版本101-125
    """
    return fake.chrome(
        version_from=version_from,
        version_to=version_to,
        build_from=0,
        build_to=0,
    )


def wait(n: int = 0, log: bool = False):
    """
    后台运行, 异步不阻塞。

    n: 等待秒数
    log: 启动后打印日志。

    @wait(2)
    def hello():
        print('运行完毕')
    """

    def wrap(f):
        @wraps(f)
        def func(*args, **kwargs):
            if log:
                logger.info(f"{f.__name__} 函数将于 {n} 秒后运行")
            t = Timer(n, f, args=args, kwargs=kwargs)
            t.start()

        return func

    return wrap


def text2png(
    text,
    output=None,
    font_path=None,
    font_size=40,
    padding=10,
    color=(0, 0, 0),
):
    """
    ## 文字转图片

    text: 文字内容
    output: 图片保存路径, 默认为 output.png
    font_path: 字体文件路径，默认使用文泉驿字体。
    font_size: 字体大小，默认 40 。
    padding: 边距，默认 10 。
    color: 背景颜色，默认白色
    """
    from PIL import Image, ImageDraw, ImageFont

    if not font_path:
        # 默认使用文泉驿字体，字体版权归文泉驿所有。
        font_path = os.path.join(os.path.dirname(__file__), "wqy.ttf")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("无法加载字体文件，请检查路径和文件名。")
        return

    # 计算文本边界框
    dummy_image = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_image)
    text_bbox = draw.textbbox((0, 0), text, font=font)

    # 计算文本宽度和高度，包括填充
    text_width = text_bbox[2] - text_bbox[0] + 2 * padding
    text_height = text_bbox[3] - text_bbox[1] + 2 * padding

    # 创建适当大小的图像
    image = Image.new(
        "RGB",
        (text_width, text_height),
        (255, 255, 255),
    )
    draw = ImageDraw.Draw(image)

    # 计算文本位置
    text_x = padding
    text_y = padding

    # 绘制文本
    draw.text((text_x, text_y), text, font=font, fill=color)

    # 保存图像
    if not output:
        output = "output.png"
    image.save(output)
    print(f"图像已保存为 {output}")
