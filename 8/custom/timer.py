from time import sleep

def timer(before, waitFrequency: int, interval: int) -> int:
    for i in range(1, int(waitFrequency)+1):
        sleep(interval)
        # print(f"{before + i} seconds")
    return int(waitFrequency)