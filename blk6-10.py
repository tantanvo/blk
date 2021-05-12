import base64, hashlib, ast
import Crypto
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

'''
6.1. Mã hóa/Giải mã bằng khóa đối xứng
- A muốn gửi 1 tài liệu đến B, cả 2 sẽ tạo ra một khóa chung
+ Tài liệu thô của A + Khóa chung  -> Mã hóa ->  Tài liệu mã hóa -> gửi đến B
+ B nhận tài liệu mã hóa  + Khóa chung -> Giải mã -> Tài liệu thô
'''

p = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
unp = lambda s: s[0:s[-1]]

class aes:
    def __init__(self):
        pass

    def ent(self, doc, key):
        raw_doc = p(doc)
        key = hashlib.sha256(key.encode('utf-8')).digest()
        rand_byte = Random.new().read(AES.block_size)
        coded = AES.new(key, AES.MODE_CBC, rand_byte)
        return base64.b64encode(rand_byte + coded.encrypt(raw_doc.encode('utf-8')))

    def det(self, doc_ent, key):
        doc_ent = base64.b64decode(doc_ent)
        key = hashlib.sha256(key.encode('utf-8')).digest()
        rand_byte = doc_ent[:16]
        coded = AES.new(key, AES.MODE_CBC, rand_byte)
        return unp(coded.decrypt(doc_ent[16:]))

alg = aes()

key = "63756843836583645936548364836"

# A
doc_raw1 = "Chao em!"
docA1 = alg.ent(doc_raw1, key)
print('Khóa đối xứng - Mã hóa:',docA1.decode('utf-8'))

# B
docB1 = alg.det(docA1, key)
print('Khóa đối xứng - Giải mã:',docB1.decode('utf-8'))

'''
6.2. Mã hóa/Giải mã bằng khóa bất đối xứng
- A muốn gửi tài liêu đến B, B tạo ra khóa 1, từ khóa 1 tạo ra khóa 2
và cho A biết khóa 2 này
+ Tài liệu thô của A + Khóa 2 -> Mã hóa ->  Tài liệu mã hóa -> gửi đến B
+ B nhận tài liệu mã hóa +  Khóa 1 + tài liệu mã hóa -> Giải mã -> Tài liệu thô
'''

create = Random.new().read
# B tạo cặp khóa 1 private key, 1 public key
privateKey = RSA.generate(1024, create) # private key
publicKey = privateKey.publickey() # public key

# A
doc_raw2 = "Em chao anh!"
encryptor = PKCS1_OAEP.new(publicKey)
docA2 = encryptor.encrypt(doc_raw2.encode('utf-8'))
print('Khóa bất đối xứng - Mã hóa:',docA2)

# B
decryptor = PKCS1_OAEP.new(privateKey)
docB2 = decryptor.decrypt(ast.literal_eval(str(docA2)))
print('Khóa bất đối xứng - Giải mã:',docB2.decode('utf-8'))

'''
7. Modulo
VD: Thực hiện phép chia lấy dư
0 % 5 = 0      5 % 5 = 0     10 % 5 = 0     15 % 5 = 0
1 % 5 = 1      6 % 5 = 1     11 % 5 = 1     16 % 5 = 1
2 % 5 = 2      7 % 5 = 2     12 % 5 = 2     17 % 5 = 2
3 % 5 = 3      8 % 5 = 3     13 % 5 = 3     18 % 5 = 3
4 % 5 = 4      9 % 5 = 4     14 % 5 = 4     19 % 5 = 4
Số bị chia 5 gọi là modulo
0 -> 4 gọi là nhóm tuần hoàn
Nếu gọi n là các số chia, p là modulo 5
thì n % p = {0,.....p-1}

8. Logarith
VD: 2^x = 4 => x = log2(4) gọi là log cơ số 2 của 4

9. Nhóm tuần hoàn của Logarith % modulo (modulo là 1 số nguyên tố)
Giả sử ta có:
x = log2(4) % 7 <=> 2^x % 7 = 4

Để tìm được x thỏa mãn phương trình ta phải thử từng số mũ
2^0 % 7 = 4 -> ko thỏa mãn
2^1 % 7 = 4 -> ko thỏa mãn
2^2 % 7 = 4 -> thỏa mãn (1)
2^3 % 7 = 4 -> ko thỏa mãn
2^4 % 7 = 4 -> ko thõa mãn
2^5 % 7 = 4 -> thỏa mãn (2)
=> x = 2 và x = 5
Nếu tiếp tục ta sẽ còn tìm được giá trị khác của x thỏa mãn phương trình

Xét bảng ví dụ sau:
cơ số (b)    b^1%7  b^2%7  b^3%7  b^4%7  b^5%7  b^6%7 
   1           1      1      1      1      1      1
   2           2      4      1      2      4      1
   3           3      2      6      4      5      1
   4           4      2      1      4      2      1
   5           5      4      6      2      3      1
   6           6      1      6      1      6      1
Chú ý: tại cơ số 3 và 5 ta có kết quả là các con số 1,2,3,4,5,6
gọi là nhóm tuần hoàn của logarith và modulo (với modulo là 1 số nguyên tố)
=> để tim số mũ là bao nhiêu để có kết quả là 1, ta phải thử từng số mũ cho
đến khi = 6 thì thỏa mãn
Trong blockchain người ta sử dụng cơ số và số nguyên tố rất lớn 256 bit
khoảng 77 - 78 chữ số thập phân, và để tìm được số mũ thỏa mãn
thì máy tính phải thử từng số mũ -> một việc làm bất khả thi
Sẽ khám phá nó trong phần Đường cong Ê líp

10. Trao đổi khóa Diffie-Hellman
'''
print('----------------------Trao đổi khóa------------------------------')
# A và B thống nhất sử dụng cơ số là 3 và số nguyên tố 17
b  = 3
p = 17

privkeyA  = 15 # A tạo cho mình một khóa riêng là 15 (< 17)
privkeyB = 13 # B tạo cho mình một khóa riêng là 13 (< 17)

pubkeyA = (b**15) % 17 # A tính toán khóa công khai của mình
pubkeyB = (b**13) % 17 # B tính toán khóa công khai của mình

#A, B gửi pubkey cho nhau

secretkeyA = (pubkeyB ** privkeyA) % p # A tính toán khóa bí mật
print('Secret Key A:', secretkeyA)# 10
secretkeyB = (pubkeyA ** privkeyB) % p # B tính toán khóa bí mật
print('Secret Key B:', secretkeyB)# 10
print(secretkeyA == secretkeyB)# True
'''
Nếu C nhìn thấy pubkey của A và B và giả sử đoán đúng cơ số là 3 và số nguyên tố 17
thì rất khó để C tính được privkey của A và B vì:
privkey = logb(pubkey)% p hay b^privkey % p = pubkey
'''
