import time

iterations = 1000000
begin = time.perf_counter()
for i in range(iterations):
    time.perf_counter()
print(f'time.perf_counter() took {time.perf_counter() - begin}')


begin = time.perf_counter()
for i in range(iterations):
    time.time()
print(f'time.time() took {time.perf_counter() - begin}')