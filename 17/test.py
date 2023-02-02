import time
n_blocks = 1_000_000_000  # _000

start_time = time.time()

for i in range(n_blocks):
    if i % 100_000_000 == 0:
        print(f'{i:,}', 'time passed', time.time() - start_time)

print('time passed', time.time() - start_time)
