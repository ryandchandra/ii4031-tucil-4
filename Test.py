
from DigitalSignatureRSALib import *

# initializing string
str = "A<ds>10acdf468</ds>"
D = "10acdf468"


A, B = GetDocAndSign(str)
print(A)
print(B)

str2 = hex(B)
C = str2[2:len(str2)]
print(str2)
print(C==D)

