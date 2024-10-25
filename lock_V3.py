# coding: utf-8
import random

digits1 = "02468aBcDeFgHiJkLmNoPqRsTuVw~.!@#"
digits2 = "13579AbCdEfGhIjKlMnOpQrStUvW$%^&*"
digits3 = "**********()_+=-{[]}|:;<>?,XxzZyY"
digits_set = {0: digits1, 1: digits2}
flag = 0


def convert(number, base):
    global flag
    result = ""

    while number > 0:
        remainder = number % base
        result = digits_set[flag % 2][remainder] + result
        number //= base

    flag += 1
    return result


# 分组交换
def confuse1(src):
    result = "".join([src[i + 1] + src[i] for i in range(0, len(src) - 1, 2)])
    if len(src) % 2 != 0:
        result += src[-1]
    return result


# 整组交换
def confuse2(src):
    odd_chars = src[::2]
    even_chars = src[1::2]
    return odd_chars + even_chars


def lock(src):
    result = ""

    for i in src:
        random_num = random.randint(11, 33)
        temp_str = convert(ord(i), random_num) + digits3[random_num - 1]
        result += temp_str

    result = confuse1(confuse2(result))
    return result

print(lock("请在这里加密“8964”"))