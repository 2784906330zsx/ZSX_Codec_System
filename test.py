import lock_V2
import unlock_V2
import lock_V3
import unlock_V3
import d

str1 = "abcdefg"
for i in range(100):
    result1 = lock_V3.lock(str1)
    result2 = lock_V2.lock(str1)

    print(i)
    print("V3加密: " + result1)
    print("V3解密: " + d.decrypt(result1))
    # print("V2加密: " + result2)
    # print("V2解密: " + unlock_V2.unlock(result2) + "\n")
