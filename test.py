from datetime import datetime
import threading

# datetime object containing current date and time
# now = datetime.now()
#
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# print("start program date and time =", dt_string)
#
# def hello():
#     hello_time = datetime.now()
#     hello_time_string = hello_time.strftime("%d/%m/%Y %H:%M:%S")
#     print("hello_time =", hello_time_string)
#     hello0 = hello_time_string.split()[0]
#     hello1 = hello_time_string.split()[1]
#     print(hello0)
#     print(hello1)
#
# t = threading.Timer(5.0, hello)
# t.start()  # after 5 seconds, "hello, world" will be printed
#
#
#
dict = {}
dict['key'] = ['value1', 'value2', 'value3']
dict['key2'] = ['value1', 'value2']

x = 'value3'

for key, value in dict.items():
    print(key)
    print(value)
    for item in value:
        print(item)
        if item==x:
            print('pizdec')

print(dict)









