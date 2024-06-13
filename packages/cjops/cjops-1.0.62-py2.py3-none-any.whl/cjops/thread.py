import concurrent.futures
from functools import partial

def run_thread_pool(func, items, workers=5, **kwargs):
    """
    使用线程池执行指定的函数，支持传递参数和设置线程数。

    Args:
        func (callable): 要执行的函数。
        items (iterable): 函数的输入数据。
        workers (int): 线程数，默认为 5。
        **kwargs: 传递给函数的关键字参数。

    Returns:
        list: 所有线程执行的结果的列表。
    """
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        # 使用 partial 函数将固定参数传递给 func
        worker = partial(func, **kwargs)
        # 获取每个线程执行的结果，统一处理
        futures = [executor.submit(worker, item) for item in items]
        for future in concurrent.futures.as_completed(futures):
            try:
                future_result = future.result()
                if future_result:
                    # 判断数据类型，如果是List则extend
                    if isinstance(future_result, list):
                        results.extend(future_result)
                    else:
                        results.append(future_result)
            except Exception as e:
                print(f"An error occurred: {e}")
    return results

if __name__ == '__main__':
    # 多线程执行案例
    def shuangshu(item, **kwargs):
        key = kwargs.get("key", "")
        return str(int(item) * 2) + f'==={key}'

    items = [n for n in range(10)]

    res = run_thread_pool(shuangshu, items, key="123")
    print(res)