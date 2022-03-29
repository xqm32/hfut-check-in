import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


# 加密方法在页面源代码中
def encryptPassword(key, aes_str):
    aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    padPKCS7 = pad(aes_str.encode('utf-8'), AES.block_size,
                   style='pkcs7')
    encryptAes = aes.encrypt(padPKCS7)
    encryptedText = str(base64.encodebytes(
        encryptAes), encoding='utf-8')
    encryptedTextStr = encryptedText.replace('\n', '')
    return encryptedTextStr
