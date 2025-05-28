import random, math

def dec_to_bin(x, *, bits=16):
    if x >= (2**(bits - 1)):
        raise ValueError(f"Input must be less than {2**(bits - 1)}")
    if x < (-(2**(bits - 1))):
        raise ValueError(f"Input must be greater than {-(2**(bits - 1)) - 1}")

    if x < 0:
        out = "1"
        tot = -(2**(bits - 1))
    else:
        out = "0"
        tot = 0
    for i in range(bits - 2, -1, -1):
        if (tot + 2**i) <= x:
            out += "1"
            tot += 2**i
        else:
            out += "0"
    return out

# print(dec_to_bin(47536, bits=18))
# print(dec_to_bin(-18000))
# print(dec_to_bin(14768))
# print(dec_to_bin(-32768))

def bit(x, j):
    print("bit")
    return ((2**j) & x) > 0

def multiply(x, y):
    print("multiply", x, y)
    sum = 0
    xShifted = x
    i = 0
    while i < 16:
        if bit(y, i):
            sum = sum + xShifted
        
        xShifted = xShifted + xShifted
        i = i + 1
    return sum

def pow(a, b):
    print("pow")
    out = 1
    while b > 0:
        out = multiply(out, a)
        b = b - 1
    return out



def pos_divide(x, y):
    if y > x:
        return 0
    q = pos_divide(x, y + y)
    tem = q * y
    if (x - (tem + tem)) < y:
        return q + q
    else:
        return q + q + 1

def divide(x, y):
    negate_output = False

    if x < 0:
        x = - x
        negate_output = True

    if y < 0:
        y = -y
        negate_output = not negate_output
    
    out = pos_divide(x, y)

    if negate_output:
        out = - out
    
    return out

# print(divide(32767, 2))

# def divide(x, y):
#     print("divide")
#     if x < 10:
#         v_base_pow = 0
#     elif x < 100:
#         v_base_pow = 1
#     elif x < 1000:
#         v_base_pow = 2
#     elif x < 10000:
#         v_base_pow = 3
#     else:
#         v_base_pow = 4

#     out = 0

#     while v_base_pow > -1:
#         v_base = pow(10, v_base_pow)
#         v_mult = 0

#         tem = multiply(v_base, multiply(v_mult + 1, y))
#         while tem < x or tem == x:
#             v_mult = v_mult + 1
#             tem = multiply(v_base, multiply(v_mult + 1, y))

#         tem = multiply(v_base, v_mult)
#         out = out + tem
#         x = x - multiply(tem, y)
#         v_base_pow = v_base_pow - 1
    
#     return out


def sqrt(x: int):
    min = 1
    if (x < 10):
        max = x
    else:
        max = divide(x, 2)
    mdpt = divide(max + min, 2)

    while max - min != 1:
        if mdpt*mdpt == x:
            return mdpt
        if mdpt*mdpt < x:
            min = mdpt
        else:
            max = mdpt
        mdpt = divide(max + min, 2)

    return min

print(sqrt(32767))