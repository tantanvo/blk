import struct, binascii, os, codecs, random, hashlib

'''
1. Số thập lục phân (dạng số này thực hành hầu như hơn 90%)
Gôm 16 chữ số: 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f (0 -> 15)
Mỗi chữ số thể hiện 4 bit, 2 số là 8 bit = 1 byte
Số thập lục phân ít nhất phải có 2 chữ số: 0a = 10; ff =255, và phải liền cặp
'''
'''
2. Big Endian / Litte Endian
'''
print('-------Big Endian / Little Endian-----------')
string = 'abcd' # 1 con số thập lục phân dạng chuỗi (sử dụng cho cách 1)
string_hex = binascii.unhexlify(string)# chuyển sang dạng byte_hex (sử dụng cho cách 2)

# Big Endian (theo thứ tự ab trước rồi đến cd)
# Cách 1
big_endian1 = int(string[:2],16)*2**0 + int(string[2:4],16)*2**8 # kq 52651
print('Big Endian',big_endian1)
# Cách 2
big_endian2 = struct.unpack('H', string_hex)[0] # kq 52651
print('Big Endian',big_endian2)


# Little Endian (theo thứ tự cd trước rồi đến ab)
# Cách 1
little_endian1 = int(string[2:4],16)*2**0 + int(string[:2],16)*2**8 # kq 43981
print('Little Endian',little_endian1)
# Cách 2
little_endian2 = struct.unpack('!H', string_hex)[0] # kq 43981
print('Little Endian',little_endian2)

# Các ngôn ngữ lập trình mặc định sử dụng little endian
# chỉ cần nhập 0xabcd là sẽ tính ra kq 43981
print('---------Big Endian / Little Endian-------------')
'''
3. Biến số (VarInt)

- Nếu 1 byte đầu tiên nhỏ hơn fd(hay 252) thì giá trị chính nó là số lượng byte tiếp theo cần xử lý
    VD: 04abcdef0123456789........ -> 1 byte đầu tiên là 04 < fd => lấy 4 byte tiếp theo để xử lý là abcdef01
- Nếu 1 byte đầu tiên = fd(hay 253) thì giá trị 2 byte tiếp theo là số lượng byte cần xử lý
    VD: fd0401cdef0123456789........-> 2 byte tiếp theo 0401(hay 260) là số lượng byte cần xử lý
- Nếu 1 byte đầu tiên là fe (hay 254) thì giá trị 4 byte tiếp theo là số lượng byte cần xử lý
- Nếu 1 byte đầu tiên là ff (hay 255) thì giá trị 8 byte tiếp theo là số lương byte cần xử lý
Thông thường số lượng byte cần xử lý nằm trong khoảng khoảng 1 -> 2 byte
'''
print('---------VarInt-------------')
string_varint='fcabcdef0123456789'# tiếp tục là các con số thập lục phân rất dài sẽ được xử lý
value=int(string_varint[:2], 16)*2**0 # lấy 2 kí tự đầu tiên hay 1 byte đầu tiên xem giá trị bao nhiêu
if value<0xfd: 
    print(value) # chính nó
if value==0xfd: # bỏ 1 byte dau tien, lay 2 byte tiep theo (abcd)
    print(struct.unpack('H', binascii.unhexlify(string_varint[2:6]))[0])
if value==0xfe: # bỏ 1 byte dau tien, lay 4 byte tiep theo (abcdef01)
    print(struct.unpack('I', binascii.unhexlify(string_varint[2:10]))[0])
if value==0xff: # bỏ 1 byte dau tien, lay 8 byte tiep theo (abcdef0123456789)
    print(struct.unpack('Q', binascii.unhexlify(string_varint[2:18]))[0])
print('---------VarInt-------------')

'''
4. Số ngẫu nhiên (Random number)
Chọn một ngôn ngữ lập trình làm việc này (ở đây mình sử dụng Python) 
'''
print('---------Random number-------------')
# cách 1
random_1 = codecs.encode(os.urandom(32), 'hex').decode()
print('Hexadecimal:',random_1)
print('Decimal:',int(random_1, 16))
# cách 2
random_2 = random.SystemRandom().randint(0x0, 2**255)
print("Hexadecimal: {0:x}".format(random_2))
print('Decimal:',random_2)
print('---------Random number-------------')

'''
5. Hàm băm (Hash Function)
- Hàm băm(hash) mang tính chất 1 chiều không thể đảo ngược lại
- Các loại hàm băm thường sử dụng là ripemd160, sha256, sha512
'''
print('---------Hash-------------')
# Băm chuỗi
string_hash = 'abcdef'
str_byte = binascii.unhexlify(string_hash)

str_hash160 = hashlib.new('ripemd160', str_byte).hexdigest()
print('Ripemd160',str_hash160)
str_hash256 = hashlib.sha256(str_byte).hexdigest()
print('Sha256',str_hash256)
str_hash512 = hashlib.sha512(str_byte).hexdigest()
print('Sha512',str_hash512)
# Băm số
num = 255
num_byte = struct.pack('B', num)
num_hash160 = hashlib.new('ripemd160', num_byte).hexdigest()
print('Ripemd160',num_hash160)
num_hash256 = hashlib.sha256(num_byte).hexdigest()
print('Sha256',num_hash256)
num_hash512 = hashlib.sha512(num_byte).hexdigest()
print('Sha512',num_hash512)
print('---------Hash-------------')
