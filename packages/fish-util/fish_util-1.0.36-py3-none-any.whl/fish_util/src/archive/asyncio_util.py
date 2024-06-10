import asyncio


def block_func(x, y):
    # 模拟一个阻塞的函数，例如进行网络请求或IO操作
    import time

    time.sleep(2)
    return x * y


async def get_block_result(func, *args):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, func, *args)
    print(result)
    return result


# asyncio.run(get_block_result(block_func, 1, 2))

#     # result = await asyncio_util.get_block_result(asyncio_util.block_func, x, y)
#     result = block_func(task)
#     results.append(result)
#     # result = await asyncio_util.get_block_result(block_func, task)
# result = loop.run_until_complete()
# result = await asyncio.gather(*coros)
# print(f"Result of celery task: {result}")
# time.sleep(1)
# result = block_func(task)
# result = await asyncio_util.get_block_result(block_func, task)

# loop = asyncio.get_event_loop()
#     coros = []
#     results = []
#     for _ in range(2):
#         task = app_celery.send_mail.delay(f"email-{x}")
#         coro = loop.run_in_executor(None, block_func, task)
#         # coros.append(coro)
#         result = await coro
#         results.append(result)
#     return {"results": results}

# def block_func(task):
#     result = task.get(timeout=10)  # 如果10秒内没有结果，则抛出异常
#     return result
