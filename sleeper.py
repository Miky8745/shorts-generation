import datetime
import time

def sleepUntil(hour, minute):
    t = datetime.datetime.today()
    future = datetime.datetime(t.year, t.month, t.day, hour, minute)
    if t.timestamp() > future.timestamp():
        future += datetime.timedelta(days=1)

    time_to_sleep = (future-t).total_seconds()

    print(f"Sleeping until {hour}:{minute}, the program will be waiting for {time_to_sleep} seconds")
    time.sleep(time_to_sleep)

if __name__ == "__main__":
    sleepUntil(14, 41)
    print("hello")