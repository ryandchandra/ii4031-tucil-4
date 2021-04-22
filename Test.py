
from DigitalSignatureRSALib import *

# initializing string
str = "A<ds>10acdf468</ds>"


A, B = GetDocAndSign(str)
print(A)
print(B)

str2 = hex(B)
str3 = hex(str2)
print(str2)
print(str3)
