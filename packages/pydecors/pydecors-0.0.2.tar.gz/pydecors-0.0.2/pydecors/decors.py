import random
import time
from functools import wraps

from loguru import logger


def forever(interval=60, errback=None):
    """永远在运行"""

    def outer(func):
        def inner(*args, **kwargs):
            while True:
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    logger.error('{}  ==>  {}出现异常了  ==>  {}秒后继续启动'.format(e, func.__name__, interval))
                    if errback:
                        errback(e, *args, **kwargs)
                else:
                    logger.info('{}正常结束了 ==> {}秒后继续启动'.format(func.__name__, interval))
                finally:
                    time.sleep(interval)

        return inner

    return outer


def safe(func):
    """异常时返回False"""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error('{}  ==>  {}'.format(e, func.__name__))
            return False

    return inner


def retry(times=5, rest=2):
    """重试（当函数异常时，触发重试，重试全部失败时返回False）"""

    def outer(func):
        def inner(*args, **kwargs):
            for i in range(times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error('{}  ==>  {}'.format(e, func.__name__))
                    time.sleep(rest)
            logger.error('重试全部失败  ==>  {}'.format(func.__name__))
            return False

        return inner

    return outer


def min_work(seconds: int):
    """最少运行多少秒"""

    def outer(func):
        begin = time.time()

        @wraps(func)
        def inner(*args, **kwargs):
            result = None
            while True:
                if time.time() - begin > seconds:
                    return result
                result = func(*args, **kwargs)

        return inner

    return outer


def timer(func):
    """计时器（输出函数的执行时间）"""

    @wraps(func)
    def inner(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        logger.info('{}耗时{:.4f}秒'.format(func.__name__, t2 - t1))
        return result

    return inner


def defer(func):
    """延迟1-2秒后调用"""

    @wraps(func)
    def inner(*args, **kwargs):
        time.sleep(random.uniform(1, 2))
        return func(*args, **kwargs)

    return inner
