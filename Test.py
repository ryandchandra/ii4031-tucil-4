
from DigitalSignatureRSALib import *

# initializing string
str = "GeeksforGeeks"

str2 = GetSignature(str,1,1,1)
print(str2)

str3 = StringToByteIntArray(str2)
print(str3)

str4 = RSAEncrypt(str3,5,3401,1)
print(str4)

