# coding=utf-8

"""
@fileName       :   simple_pref_test.py
@data           :   2024/4/19
@author         :   jiangmenggui@hosonsoft.com
"""
import functools
import json
import math
import os.path
import queue
import random
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from inspect import isfunction
from pathlib import Path
from typing import NamedTuple, Callable

from . import logger
from .color import Color
from .console_table import ConsoleTable
from .decorators import catch_exception

data: queue.Queue["TaskResult"] = queue.Queue()
start_time = time.time()
end_time: float | None = None


class TaskResult(NamedTuple):
    name: str
    start: float
    end: float
    message: str = ""
    success: bool = True

    @property
    def use_time(self):
        return self.end - self.start


def task(name: str | Callable = '', weight=1, recode_result=True):
    """
    测试任务
    :param name: 任务名称 或 任务函数
    :param weight: 任务执行权重
    :param recode_result: 是否记录结果
    :return:
    """
    if isinstance(name, Callable):
        task_name = name.__name__

        @functools.wraps(name)
        def inner(*args, **kwargs):
            t1 = time.time()
            try:
                name(*args, **kwargs)
                t2 = time.time()
                if recode_result:
                    data.put(TaskResult(name=task_name, start=t1, end=t2))
            except AssertionError as e:
                t2 = time.time()
                if recode_result:
                    data.put(TaskResult(name=task_name, start=t1, end=t2, message=f'断言失败：{str(e)}', success=False))
                logger.error(f'{task_name}失败：{str(e)}', stacklevel=2)
            except Exception as e:
                t2 = time.time()
                if recode_result:
                    data.put(TaskResult(
                        name=task_name, start=t1, end=t2, message=f'{e.__class__.__name__}: {str(e)}', success=False
                    ))
                logger.exception(f'{task_name}错误：{e}', stacklevel=2)

        inner.is_task = True
        inner.weight = 1
        inner.name = task_name
        return inner
    if not isinstance(weight, int) or weight < 0:
        raise ValueError("任务权重（weight参数）必须为大于0的整数")

    def outer(func):
        task_name = name or func.__name__

        @functools.wraps(func)
        def inner(*args, **kwargs):
            t1 = time.time()
            try:
                func(*args, **kwargs)
                t2 = time.time()
                if recode_result:
                    data.put(TaskResult(name=task_name, start=t1, end=t2))
            except AssertionError as e:
                t2 = time.time()
                if recode_result:
                    data.put(TaskResult(name=task_name, start=t1, end=t2, message=f'断言失败：{str(e)}', success=False))
                logger.error(f'{task_name}失败：{str(e)}', stacklevel=2)
            except Exception as e:
                t2 = time.time()
                if recode_result:
                    data.put(TaskResult(
                        name=task_name, start=t1, end=t2, message=f'{e.__class__.__name__}: {str(e)}', success=False
                    ))
                logger.exception(f'{task_name}错误：{e}', stacklevel=2)

        inner.is_task = True
        inner.weight = weight
        inner.name = task_name
        return inner

    return outer


# 只是用来标记task，不会记录最终的执行耗时结果
mark_task = functools.partial(task, recode_result=False)


def show_result():
    result: dict[str, dict] = {}
    rps: dict[str, dict[str, int]] = {
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)): defaultdict(int) for i in
        range(int(start_time), int(end_time) + 1)}
    qps: dict[str, dict[str, int]] = {
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)): defaultdict(int) for i in
        range(int(start_time), int(end_time) + 1)}
    response: dict[str, dict[str, list]] = {
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)): defaultdict(list) for i in
        range(int(start_time), int(end_time) + 1)}
    while not data.empty():
        row = data.get()
        t1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row.start))
        t2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row.end))
        # logger.info(f'{t1=}, {t2=}')
        if t2 not in rps:
            rps[t2] = defaultdict(int)
        if t1 not in qps:
            qps[t1] = defaultdict(int)

        if t2 not in response:
            response[t2] = defaultdict(list)
        qps[t1][row.name] += 1
        response[t2][row.name].append(row.use_time)
        if row.success:
            rps[t2][row.name + '(成功)'] += 1
        else:
            rps[t2][row.name + '(失败)'] += 1
        if row.name not in result:
            result[row.name] = {
                "NAME": row.name,
                "START_TIME": row.start,
                "END_TIME": row.end,
                "USE_TIME": [row.use_time],
                "SUCCESS": int(bool(row.success))
            }
        else:
            result[row.name]['START_TIME'] = min(result[row.name]['START_TIME'], row.start)
            result[row.name]['END_TIME'] = max(result[row.name]['END_TIME'], row.end)
            result[row.name]['USE_TIME'].append(row.use_time)
            result[row.name]['SUCCESS'] += int(bool(row.success))
    table_data = []
    for value in result.values():
        use_time = sorted(value["USE_TIME"])
        table_data.append({
            "任务名称": value['NAME'],
            "执行次数": len(use_time),
            "错误次数": len(use_time) - value['SUCCESS'],
            "成功率": f"{value['SUCCESS'] / len(use_time):.4%}",
            "中位数响应": f"{int(use_time[int(len(use_time) * 0.5)] * 1000)}ms",
            "90%响应": f"{int(use_time[int(len(use_time) * 0.9)] * 1000)}ms",
            "95%响应": f"{int(use_time[int(len(use_time) * 0.95)] * 1000)}ms",
            "平均响应": f"{int(sum(value['USE_TIME']) * 1000 / len(value['USE_TIME']))}ms",
            "最小响应": f"{int(use_time[0] * 1000)}ms",
            "最大响应": f"{int(use_time[-1] * 1000)}ms",
            "吞吐量（RPS）": f'{value["SUCCESS"] / (end_time - start_time):.2f}/s'
        })
    table = ConsoleTable(table_data, caption="性能测试结果")
    print(table)
    return table, table_data, rps, qps, response


class TaskNotFoundError(ValueError): ...


class PrefRunner:
    """
    测试性能
    :param modules: 测试模块
    :param virtual_users: 虚拟用户数
    :param user_add_interval: 用户增加间隔
    :param run_seconds: 测试时间
    :param pre_task: 每秒执行的任务数量，和virtual_users参数互斥，该参数不为空时，则按照每秒执行的任务数量来执行
    :param save_result_directory: 保存结果目录，默认在当前目录下的simple_pref_test_result目录
    """

    def __init__(
            self,
            __name: str,
            *modules,
            has_main_module=True,
            virtual_users=10,
            user_add_interval=0.1,
            pre_task: float | int = None,
            run_seconds=10,
            save_result_directory='./simple_pref_test_result',
    ):
        self.name = __name
        self.tasks = []
        if has_main_module:
            modules = (*modules, sys.modules['__main__'])
        for module in modules:
            for v in module.__dict__.values():
                if isfunction(v) and getattr(v, 'is_task', False):
                    self.tasks.extend((v for _ in range(getattr(v, 'weight', 1))))
        if not self.tasks:
            raise TaskNotFoundError('没有识别到测试任务！')
        self.run_seconds = run_seconds
        self.user_add_interval = user_add_interval
        self.virtual_users = virtual_users
        self.save_result_directory = os.path.abspath(save_result_directory)

        self.pool = ThreadPoolExecutor(1000)
        self._start_time = 0
        self.pre_task = pre_task
        self.running = True

    def run_task(self, *args, **kwargs):
        if self.pre_task:
            if self.pre_task >= 1:
                self._run_task_with_pre_task(*args, **kwargs)
            elif 0 < self.pre_task < 1:
                self._run_task_with_pre_task_2(*args, **kwargs)
            else:
                raise ValueError(f'pre_task参数必须>0（实际为{self.pre_task}）')
        else:
            self._run_task_with_virtual_users(*args, **kwargs)

    def _run_task_with_virtual_users(self, *args, **kwargs):
        def run(*args, **kwargs):  # noqa
            while time.time() - self._start_time < self.run_seconds and self.running:
                random.choice(self.tasks)(*args, **kwargs)

        for _ in range(self.virtual_users):
            self.pool.submit(run, *args, **kwargs)
            time.sleep(self.user_add_interval)

    def _run_task_with_pre_task(self, *args, **kwargs):

        def run(*args, **kwargs):  # noqa
            random.choice(self.tasks)(*args, **kwargs)

        def submit(k):
            for _ in range(k):
                self.pool.submit(run, *args, **kwargs)

        x, y = divmod(self.pre_task, 9)
        ts = [x] * 9
        exe_status = [False] * 9
        for i in range(y):
            ts[i] += 1
        pre_second = int(time.time() * 10)
        while True:
            now = time.time()
            if now - self._start_time >= self.run_seconds or not self.running:
                break
            now = int(now * 10)
            index = now - pre_second
            if index >= 10:
                pre_second = now
                exe_status = [False] * 9
                submit(ts[0])
                exe_status[0] = True
            elif index < 0:
                raise ValueError('时钟回拨，无法选择任务！')
            else:
                for i in range(index):
                    if exe_status[i]:
                        continue
                    submit(ts[i])
                    exe_status[i] = True

    def _run_task_with_pre_task_2(self, *args, **kwargs):  # pre_task小于1的时候表示每次等待事件必须超过1秒
        interval = math.ceil(1 / self.pre_task)

        def run(*args, **kwargs):  # noqa
            random.choice(self.tasks)(*args, **kwargs)

        while time.time() - self._start_time < self.run_seconds and self.running:
            self.pool.submit(run, *args, **kwargs)
            time.sleep(interval)

    @catch_exception()
    def start(self, *args, **kwargs, ):
        global start_time
        global end_time
        start_time = self._start_time = time.time()
        start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._start_time))
        print(f"开始测试：{Color.green(self.name)}")
        if self.pre_task:
            print(
                f"{Color.yellow('==========测试任务启动参数==========')}\n"
                f"   {Color.thin_magenta('每秒任务数')} : {self.pre_task}\n"
                f"     {Color.thin_magenta('运行时间')} : {self.run_seconds}s\n"
                f"     {Color.thin_magenta('任务总数')} : {len(set(self.tasks))}\n"
                f"     {Color.thin_magenta('启动时间')} : {start_time_str}\n"
                f"{Color.yellow('====================================')}\n"
            )
        else:
            print(
                f"{Color.yellow('==========测试任务启动参数==========')}\n"
                f"   {Color.thin_magenta('并发线程数')} : {self.virtual_users}\n"
                f" {Color.thin_magenta('线程启动间隔')} : {self.user_add_interval}s\n"
                f"     {Color.thin_magenta('运行时间')} : {self.run_seconds}s\n"
                f"     {Color.thin_magenta('任务总数')} : {len(set(self.tasks))}\n"
                f"     {Color.thin_magenta('启动时间')} : {start_time_str}\n"
                f"{Color.yellow('====================================')}\n"
            )
        try:
            self.run_task(*args, **kwargs)
            self.pool.shutdown(wait=True)
        finally:
            end_time = time.time()
            table, table_data, rps, qps, response = show_result()
            end_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            end_str = f'\n{Color.green("测试完成！")}[完成时间{Color.thin_cyan(end_time_str)}]'
            print('\n' + end_str)
            self._save(table_data, rps, qps, response)

    def _save_html(self, file, table, rps, qps, response):

        def init_tps_data(tps):
            tps = sorted(tps.items())
            keys = set()
            for _, v in tps:
                for k in v:
                    keys.add(k)
            values = {k: [] for k in keys}
            for _, v in tps:
                for k in keys:
                    values[k].append(v.get(k, 0))
            return json.dumps({
                'keys': [k.split(' ')[1] for k, v in tps],
                "values": [{"name": k, "data": v} for k, v in values.items()]
            }, ensure_ascii=False)

        def init_response_data(response):
            response = sorted(response.items())
            keys = set()
            for _, v in response:
                for k in v:
                    keys.add(k)
            values = {k: [] for k in keys}
            for _, v in response:
                for k in keys:
                    v_ = v.get(k, [0])
                    values[k].append(int(sum(v_) / len(v_) * 1000))
            return json.dumps({
                'keys': [k.split(' ')[1] for k, v in response],
                "values": [{"name": k, "data": v} for k, v in values.items()]
            }, ensure_ascii=False)

        def init_table_data(table_data):
            return {"header": list(table_data[0].keys()), "rows": [list(row.values()) for row in table_data]}

        from jinja2 import Environment, FileSystemLoader, select_autoescape

        # 创建一个环境，指定模板文件所在的路径
        env = Environment(
            loader=FileSystemLoader(Path(__file__).parent),
            autoescape=select_autoescape(['html', 'xml'])
        )
        if self.pre_task:
            run_arguments = [
                f"每秒任务数 : {self.virtual_users}"
            ]
        else:
            run_arguments = [
                f"并发线程数 : {self.virtual_users}",
                f"线程启动间隔 : {self.user_add_interval}s"
            ]
        with open(Path(__file__).parent / 'echart.js', 'r', encoding='u8') as f:
            echart_js = f.read()

        template = env.get_template('result.html')
        context = {
            "echartJs": echart_js,
            "title": self.name,
            'arguments': [
                *run_arguments,
                f"运行时间 : {self.run_seconds}s",
                f"任务总数 : {len(set(self.tasks))}",
                f"启动时间 : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}",
                f"结束时间 : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}"],
            "table": init_table_data(table),
            "rpsData": init_tps_data(rps),
            "qpsData": init_tps_data(qps),
            "responseData": init_response_data(response)
        }
        with open(file, 'w', encoding='u8') as f:
            f.write(template.render(context))

    def _save(self, table, rps, qps, response):
        if not os.path.exists(self.save_result_directory):
            os.mkdir(self.save_result_directory)
        file = os.path.join(self.save_result_directory, f'{self.name}_{time.strftime("%Y%m%d%H%M%S")}')
        self._save_html(file + '.html', table, rps, qps, response)
        print(f'\n结果已保存至：{Color.thin_blue(file + ".html")}')


if __name__ == '__main__':
    print(math.ceil(3 / 10))
