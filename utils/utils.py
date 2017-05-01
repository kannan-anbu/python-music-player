

def formatTimeMillis(millis):
    # print(type(millis))
    millis = int(millis)
    sec = millis // 1000000000
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    if h == 0:
        return '%2d:%02d' % (m, s)
    else:
        return '%2d:%02d:%02d' % (h, m, s)


def shuffleList(list):
    if list:
        temp = []
        import random
        while list:
            temp.append(
                list.pop(
                    random.randrange(0, len(list))
                )
            )
        list = temp.copy()
    return list
