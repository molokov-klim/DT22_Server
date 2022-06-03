from datetime import datetime
import threading

# datetime object containing current date and time
now = datetime.now()

dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)

def hello():
    print("hello, world")
    hello_time = datetime.now()
    hello_time_string = hello_time.strftime("%d/%m/%Y %H:%M:%S")
    print("hello_time =", hello_time_string)
    hello0 = hello_time_string.split()[0]
    hello1 = hello_time_string.split()[1]
    print(hello0)
    print(hello1)

t = threading.Timer(5.0, hello)
t.start()  # after 5 seconds, "hello, world" will be printed
