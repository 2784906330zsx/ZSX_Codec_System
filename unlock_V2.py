# coding: utf-8
digits1 = "0123456789abcdefghijklmnopqrstuvwxyz"
digits2 = "~!@#$%^&*()-+=][}{|:;<>,.?"


def convert(number, base):
    decimal_result = 0
    power = 0

    try:
        for digit in reversed(number):
            decimal_result += digits1.index(digit) * (base**power)
            power += 1
    except ValueError:
        return ""
    except IndexError:
        return ""

    return str(decimal_result)


def unlock(src):
    if src[0] in digits2:
        return ""

    if src[-1] not in digits1[10:]:
        return ""
    else:
        num1 = digits1.index(src[-1]) + 1

    count = 0
    for i in src:
        if i in digits1:
            count += 1
        else:
            break

    str1 = src[0:count]
    num2 = int(convert(str1, num1)) - 88
    str2 = src[-1 - num2 : -1]
    str3 = src[count : -1 - num2][::-1]

    result = ""
    temp_str = ""
    count = 0
    str4 = ""

    try:
        for index, i in enumerate(str3):
            if index == len(str3) - 1:
                break
            elif i in digits1 and str3[index + 1] not in digits2:
                temp_str += i
            elif i in digits1 and str3[index + 1] in digits2:
                temp_str += i
                str4 = convert(temp_str, digits1.index(str2[count]) + 1)
                if str4 != "":
                    result += chr(int(str4))
                else:
                    return ""

                count += 1
                temp_str = ""
    except ValueError:
        return ""
    except IndexError:
        return ""

    return result
