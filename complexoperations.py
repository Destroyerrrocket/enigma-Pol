def mcm(x, y):
    if x > y:
        mayor = x
    else:
        mayor = y
    while (True):
        if ((mayor % x == 0) and (mayor % y == 0)):
            mcm = mayor
            break
        mayor += 1
    return mcm


def mcd(a, b):
    if b == 0:
        return a
    return mcd(b, a % b)


def mcd2(a, b):
    while 1:
        r = a % b
        if not r:
            break
        a = b
        b = r
    return b


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def invmod(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
