import time

m = time.localtime(time.time())
H = int(m.tm_hour)
print(H)