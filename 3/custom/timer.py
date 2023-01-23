from time import sleep

def timer(before, waitFrequency, interval):
    for i in range(1, waitFrequency+1):
        sleep(interval)
        print(f"{before + i} seconds")
    return waitFrequency