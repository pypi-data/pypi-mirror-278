"""
# jsz

金手指-我的工具库
"""

from .tools import *  # noqa: F403
from .newpool import Pool


pool = Pool()
headers = {
    "connection": "close",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}
