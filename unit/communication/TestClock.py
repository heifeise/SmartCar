from Clock import Clock
tim = Clock()
tim.start(1)
i = 0
while True:
    if tim.is_stop():
        i += 1
        print(i)
        tim.start(1)
