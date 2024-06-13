import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

def fn():
    i = 0
    for j in range(131072):
        i += j
    t = time.time()
    time.sleep(0.02)
    drift = (time.time() - t) - 0.02
    print("\ndrift", drift)
    return drift

with ThreadPoolExecutor(max_workers=128) as e:
    f = [e.submit(fn) for _ in range(512)]
    c, _ = wait(f, timeout=None, return_when=ALL_COMPLETED)
    r = [x.result() for x in c]
    print("avg", sum(r) / len(r))
