# Test.py ini cuma buat aku ngecek2, nanti hapus aja filenya kalo udah final

from GenerateKeyLib import *
from random import randint
import tkinter.filedialog as fd
from RSALib import *

A = StringToByteIntArray('Aku Kamu Dia')
print(A)
B = RSAEncrypt(A, 107, 253, 1)
print (B)

C = HexStringToByteIntArray(B)
print (C)

C = [84, 4, 80, 84, 6, 87, 0, 2, 224, 13, 230, 215, 57, 198, 215, 0, 0, 1, 0, 16, 0, 0, 0, 1]
print(C)
D = ""
for byte in C:
    cipher_hex = str(hex(byte))[2:].upper()
    if (len(cipher_hex)==1):
        cipher_hex = '0'+cipher_hex
    D = D + cipher_hex
    print (cipher_hex)
print(D)

E = RSADecrypt(D,209,2183) 
print(E)