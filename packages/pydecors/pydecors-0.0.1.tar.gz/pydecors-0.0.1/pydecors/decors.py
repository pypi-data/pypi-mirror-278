import random
import time
from functools import wraps

from loguru import logger


def min_work(seconds: int):
    """最少运行多少秒"""

    def _min_work(func):
        begin = time.time()

        @wraps(func)
        def __min_work(*args, **kwargs):
            result = None
            while True:
                if time.time() - begin > seconds:
                    return result
                result = func(*args, **kwargs)

        return __min_work

    return _min_work


def timer(func):
    """计时器（输出函数的执行时间）"""

    @wraps(func)
    def _timer(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        logger.info('耗时{:.4f}秒<{}>'.format(t2 - t1, func.__name__))
        return result

    return _timer


def defer(func):
    """延迟调用"""

    @wraps(func)
    def _defer(*args, **kwargs):
        time.sleep(random.uniform(1, 2))
        return func(*args, **kwargs)

    return _defer
