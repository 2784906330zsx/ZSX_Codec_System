import random
import lock_V3
from sympy import mod_inverse, isprime


# 生成一个大素数
def generate_large_prime(keysize):
    while True:
        num = random.getrandbits(keysize)
        if isprime(num):
            return num


# 生成密钥对
def generate_keypair(keysize):
    p = generate_large_prime(keysize // 2)  # 生成一个 keysize/2 位的大素数 p
    q = generate_large_prime(keysize // 2)  # 生成一个 keysize/2 位的大素数 q
    n = p * q  # 计算 n = p * q
    phi = (p - 1) * (q - 1)  # 计算欧拉函数 φ(n) = (p-1) * (q-1)

    e = random.randrange(2, phi)  # 选择一个随机的 e, 1 < e < φ(n)
    g = gcd(e, phi)
    while g != 1:  # 确保 e 与 φ(n) 互质
        e = random.randrange(2, phi)
        g = gcd(e, phi)

    d = mod_inverse(e, phi)  # 计算 d, 使得 d ≡ e^(-1) (mod φ(n))

    return ((e, n), (d, n))  # 返回公钥 (e, n) 和私钥 (d, n)


# 计算最大公约数
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# 使用公钥加密
def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]  # 对每个字符进行加密
    return cipher


# 使用私钥解密
def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr(pow(char, key, n)) for char in ciphertext]  # 对每个字符进行解密
    return "".join(plain)


if __name__ == "__main__":
    keysize = 128  # 设置密钥长度

    public, private = generate_keypair(keysize)  # 生成公钥和私钥
    print("公钥:", public)
    print("私钥:", private)

    message = "12345678910"  # 要加密的原文
    print("原文:", message)

    encrypted_msg = encrypt(public, message)  # 使用公钥加密
    print("密文:", encrypted_msg)

    decrypted_msg = decrypt(private, encrypted_msg)  # 使用私钥解密
    print("解密文:", decrypted_msg)
