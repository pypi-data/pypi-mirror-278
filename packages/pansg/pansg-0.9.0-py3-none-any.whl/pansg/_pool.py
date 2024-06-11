# pool.py
import logging
from multiprocessing import Pool

def parallel_process(tasks, num_processes):
    with Pool(processes=num_processes) as pool:
        pool.starmap(process_task, tasks)


def process_task(func, *args):
    try:
        return func(*args)
    except Exception as e:
        logging.error(f"Task failed with exception: {e}")
        return f"Task failed with exception: {e}"


if __name__ == "__main__":
    # 示例代码，可以在运行 pool.py 时测试
    sample_tasks = [1, 2, 3, 4, 5]  # 示例任务列表
    parallel_process(sample_tasks)
