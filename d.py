import math

chr_list1 = "13579AbCdEfGhIjKlMnOpQrStUvW$%^&*"
chr_list2 = "02468aBcDeFgHiJkLmNoPqRsTuVw~.!@#"
const_keys = "()_+=-{[]}|:;<>?,XxzZyY"


def str_merge(bl, el):
    mlen = min(len(bl), len(el))
    rem = bl[mlen:] if mlen < len(bl) else el[mlen:]
    merge = ""
    for i in range(mlen):
        merge += bl[i] + el[i]
    merge += rem
    return merge


def decrypt(enc):
    ol = enc[::2]
    el = enc[1::2]
    enc = str_merge(el, ol)
    mid = math.ceil(len(enc) / 2)
    fl = enc[:mid]
    ll = enc[mid:]
    enc = str_merge(fl, ll)
    for i in range(len(enc)):
        idx = chr_list2.find(enc[i])
        if idx != -1:
            enc = enc[:i] + chr_list1[idx] + enc[i + 1 :]

    content = ""
    enc_chr = ""
    for char in enc:
        enc_chr += char
        if char in const_keys:
            key_base = const_keys.find(enc_chr[-1]) + 0xB
            enc_chr = enc_chr[::-1][1:]
            dec = 0
            for i in range(len(enc_chr)):
                num = chr_list1.find(enc_chr[i])
                dec += num * (key_base**i)
            content += chr(dec)
            enc_chr = ""
    return content


if __name__ == '__main__':
	enc = '39o{9B{GB4KUgaf=85-DACN2f;VC3wx56Jf54;5B|5yPKb97049<27xkyM6iC9J]AH]12Lf9V]Cz6b:2I10an-Tf70}1'
	print(decrypt(enc))

# print(str_merge("123", "456"))
