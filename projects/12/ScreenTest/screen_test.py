# def drawLine(x1: int, y1: int, x2: int, y2: int):
#     a = 0
#     b = 0
#     dx = x2 - x1
#     dy = y2 - y1
#     print(a, b, dx, dy)
#     while a <= dx and b <= dy:
#         print(x1 + a, y1 + b)
#         if (a/dx) < (b/dy):
#             a += 1
#         else:
#             b += 1


def drawLineUp(x1: int, y1: int, x2: int, y2: int):
    a = 0
    b = 0
    dx = x2 - x1
    dy = y2 - y1
    adyMinusbdx = 0
    print(a, b, dx, dy)
    while a <= dx and b <= dy:
        print(x1 + a, y1 + b)
        if adyMinusbdx < 0:
            a += 1
            adyMinusbdx += dy
        else:
            b += 1
            adyMinusbdx -= dx


def drawLineDown(x1: int, y1: int, x2: int, y2: int):
    a = 0
    b = 0
    dx = x2 - x1
    dy = y2 - y1
    adyMinusbdx = 0
    print(a, b, dx, dy)
    while a <= dx and b >= dy:
        print(x1 + a, y1 + b)
        if adyMinusbdx < 0:
            a += 1
            adyMinusbdx -= dy
        else:
            b -= 1
            adyMinusbdx -= dx


drawLineDown(163,35,178,20)
# print()
# drawLineDown(10, 10, 14, 4)