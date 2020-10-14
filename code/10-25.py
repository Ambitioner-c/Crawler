import random


# 产生随机驻点
def random_xy():
    a_c = random.randint(1, 999)
    b_c = random.randint(a_c + 1, 1000)

    while (2 * a_c >= 1000) or (2 * (b_c - a_c) >= 1000):
        a_c, b_c = random_xy()
    return a_c, b_c


def move(length, num, step, a, b):
    step_1 = 0      # 1驻点物资数量
    step_2 = 0      # 2驻点物资数量
    # a             1驻点位置坐标
    # b             2驻点位置坐标
    c = 0           # 最终物资数量

    # a = 200
    # b = 533

    # print(a, b)
    # 第一站
    # 1驻点存放物资数量（注意第三次为特殊情况）
    step_1 = (1000 - (2 * a)) * 2 + (1000 - a)
    # print('step_1：%s' % step_1)
    # print('b-a:%s' % str(b - a))

    # 第二站
    # 考虑第一站剩余物资的多少，决定第一站到第二站的往返次数
    if step_1 - 2000 >= b - a:

        # 往返5次
        step_2 = (1000 - (2 * (b - a))) * 2 + (step_1 - 2000 - (b - a))
        # print('step_2:%s' % step_2)

        # 终点站
        if step_2 - 1000 >= 1000 - b:
            c1 = b
            c2 = (1000 - (2 * (1000 - b))) * 2 + (step_2 - 1000 - (1000 - b))
            c = max(c1, c2)
            # print('a=%s,b=%s: c=%s' % (a, b, c))
        elif step_2 >= 1000:
            c = b
            # print('a=%s,b=%s: c=%s' % (a, b, c))
        else:
            c = step_2 - b
            # print('a=%s,b=%s: c=%s' % (a, b, c))
    elif step_1 - 1000 >= (b - a):
        # 往返3次
        step_2 = (1000 - (2 * (b - a))) * 1 + (step_1 - 1000 - (b - a))
        # print('step_2:%s' % step_2)

        # 终点站
        if step_2 - 1000 >= 1000 - b:
            c1 = b
            c2 = (1000 - (2 * (1000 - b))) * 2 + (step_2 - 1000 - (1000 - b))
            c = max(c1, c2)
            # print('a=%s,b=%s: c=%s' % (a, b, c))
        elif step_2 >= 1000:
            c = b
            # print('a=%s,b=%s: c=%s' % (a, b, c))
        else:
            c = step_2 - b
            # print('a=%s,b=%s: c=%s' % (a, b, c))
    else:
        c = a
        # print('a=%s,b=%s: c=%s' % (a, b, c))

    return a, b, c


if __name__ == '__main__':
    my_length = 1000  # 总长度
    my_num = 3000  # 出发点总运输数量

    my_step = 2  # 驻点数

    a, b = random_xy()
    x1, y1, z1 = move(my_length, my_num, my_step, a, b)
    print('a=%s,b=%s: c=%s' % (x1, y1, z1))

    x2, y2, z2 = move(my_length, my_num, my_step, x1 + 1, y1)
    print('a=%s,b=%s: c=%s' % (x2, y2, z2))

    x3, y3, z3 = move(my_length, my_num, my_step, x1, y1 + 1)
    print('a=%s,b=%s: c=%s' % (x3, y3, z3))

    compare1 = z2/z1
    compare2 = z3/z1
    print(compare1)
    print(compare2)


