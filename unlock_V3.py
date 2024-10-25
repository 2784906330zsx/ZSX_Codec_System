# coding: utf-8
digits1 = "02468aBcDeFgHiJkLmNoPqRsTuVw~.!@#"
digits2 = "13579AbCdEfGhIjKlMnOpQrStUvW$%^&*"
digits3 = "**********()_+=-{[]}|:;<>?,XxzZyY"

digits_set = {0: digits1, 1: digits2, 2: digits3}


def convert(number, base):
    try:
        choice = 0
        decimal_result = 0
        power = 0

        if number[0] in digits1:
            choice = 0
        else:
            choice = 1

        for digit in reversed(number):
            decimal_result += digits_set[choice].index(digit) * (base**power)
            power += 1

    except ValueError:
        return ""
    except IndexError:
        return ""

    return str(decimal_result)


# 还原整组交换
def restore1(src):
    str1 = ""
    str2 = ""
    result = []
    len1 = 0
    if len(src) % 2 == 0:
        len1 = int(len(src) / 2)
    else:
        len1 = int(len(src) / 2 + 1)

    str1 = src[0:len1]
    str2 = src[len1 : len(src)]

    for i in range(len(str2)):
        result.append(str1[i])
        result.append(str2[i])

    if len(str1) > len(str2):
        result.append(str1[-1])

    return "".join(result)


# 还原分组交换
def restore2(src):
    result = "".join([src[i + 1] + src[i] for i in range(0, len(src) - 1, 2)])
    if len(src) % 2 != 0:
        result += src[-1]
    return result


def unlock(src):
    try:
        src = restore1(restore2(src))
        temp_str = ""
        result = ""

        for i in src:
            if (i in digits1) or (i in digits2):
                temp_str += i
            elif i in digits3:
                result += chr(int(convert(temp_str, digits3.index(i) + 1)))
                temp_str = ""
            else:
                return ""

        return result

    except ValueError:
        return ""
    except IndexError:
        return ""
