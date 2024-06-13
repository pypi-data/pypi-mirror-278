"""
# 更方便的使用线程池

```
import time

pool = Pool()

@pool.task
def hello():
    time.sleep(5)
    print('hello')

for i in range(10):
    hello()

pool.state() # 查看运行状态
pool.cancel_all() # 全部取消
pool.clear() # 取消并清空任务队列
pool.wait() # 阻塞等待全部完成
```
"""

import multiprocessing
import concurrent.futures
from functools import wraps
import time
from rich.panel import Panel


class Pool:
    """
    线程池
    """

    def __init__(self, n: int = None):
        """
        线程池

        n: 线程数。默认为CPU核心数，可以自定义线程数。
        """
        if n:
            self.n = n
        else:
            self.n = multiprocessing.cpu_count()

        self.threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=self.n)
        self.callbacks = []
        self.results = []

    def run(self, f, *args, **kwargs):
        self.threadpool._max_workers = self.n
        self.threadpool._adjust_thread_count()
        f = self.threadpool.submit(f, *args, **kwargs)
        self.results.append(f)
        return f

    def task(self, f):
        """
        线程池核心函数。
        """

        @wraps(f)
        def do_task(*args, **kwargs):
            result = self.run(f, *args, **kwargs)
            for cb in self.callbacks:
                result.add_done_callback(cb)
            return result

        return do_task

    def callback(self, f):
        """
        通过装饰器增加回调函数，函数需要使用参数 future。

        @pool.callable
        def hello_callback(future):
            print(future.result())
        """
        self.callbacks.append(f)

        @wraps(f)
        def register_callback():
            f()

        return register_callback

    def wait(self, timeout: float = None, return_when: str = "ALL_COMPLETED"):
        """
        阻塞等待 Future 实例完成。

        timeout: 超时秒数
        return_when: 完成标准，共三种，分别为 ALL_COMPLETED、FIRST_COMPLETED、FIRST_EXCEPTION
        """
        return concurrent.futures.wait(
            fs=self.results,
            timeout=timeout,
            return_when=return_when,
        )

    def cancel_all(self):
        """
        全部取消
        """
        for i in self.results:
            i.cancel()
        self.state()

    def clear(self):
        """
        取消任务，并清空任务队列
        """
        self.cancel_all()
        self.results.clear()
        return self.state()

    def state_dict(self):
        """
        返回线程池当前运行状态

        extend: 拓展字段。
        """
        count_all = len(self.results)
        count_done = 0
        count_running = 0
        count_exception = 0
        count_cancelled = 0
        count_other = 0
        for i in self.results:
            if i.done():
                count_done += 1
                if i.cancelled():
                    count_cancelled += 1
                elif i.exception():
                    count_exception += 1
            elif i.running():
                count_running += 1
            else:
                count_other += 1
        count_success = count_done - count_cancelled - count_exception
        state_result = {
            "总任务": count_all,
            "已完成": count_done,
            "成功": count_success,
            "取消": count_cancelled,
            "报错": count_exception,
            "正在运行": count_running,
            "剩余任务": count_other,
        }
        return state_result

    def state(self, extend: dict = None):
        """
        返回线程池当前运行状态, 打印使用 jsz.print 函数.

        extend: 拓展字段。
        """
        state_dict = self.state_dict()
        state_result = (
            f"时间:[green]{time.strftime('%F %T')}[/]\n"
            f"总任务:{state_dict['总任务']}\n"
            f"已完成:{state_dict['已完成']} (成功:{state_dict['成功']} 取消:{state_dict['取消']} 报错:{state_dict['报错']})\n"
            f"正在运行:{state_dict['正在运行']}\n"
            f"剩余任务:{state_dict['剩余任务']}"
        )

        if extend and isinstance(extend, dict):
            state_result += "\n" + "\n".join([f"{i[0]}:{i[1]}" for i in extend.items()])
        return Panel(state_result, expand=False)
