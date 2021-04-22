import math
import hashlib

def StringToByteIntArray(string):
    # Mengubah string menjadi array of integer (byte) sesuai dengan ascii/utf-8
    # Input : string
    # Output : array of integer (byte) dari string
    byteint_array = []
    
    for char in string:
        byteint_array.append(ord(char))
        
    return byteint_array

def ByteIntArrayToString (byteint_array):
    # Mengubah string menjadi array of integer (byte) sesuai dengan ascii/utf-8
    # Input : array of integer (byte) 
    # Output : string
    string = "".join([chr(value) for value in byteint_array])
        
    return string

def OpenFileAsByteIntArray(filename):
    # Membuka file dengan nama filename per byte lalu menyimpannya menjadi array of integer (byte)
    # Input : filename
    # Output : array of integer (byte) dari isi file
    
    # Buka file
    input_file = open(filename,"rb")
    
    # Baca isi file per byte hingga habis
    byteint_array = []
    byte = input_file.read(1)
    while (byte):
        # Ubah byte tersebut menjadi integer yang sesuai lalu masukkan ke array
        byteint = int.from_bytes(byte,byteorder='little')
        byteint_array.append(byteint)
        byte = input_file.read(1)
        
    # Tutup file
    input_file.close()
        
    return byteint_array
        
def GetDocAndSign(mixed_document):
    # Mengambil document dan signature dari document (text) yang signature tergabung dengan document
    # Input : document yang tergabung dengan signature
    # Output : document (string) dan signature (int) (jika ada), -1,-1 jika tidak ada signature
    
    if (mixed_document[-5:]=="</ds>"): # Cek apakah bagian paling akhir document adalah closing tag
        ds_index = mixed_document.rfind("<ds>") # Cari opening tag juga
        if (ds_index!=-1): # Bila opening tag ditemukan, ambil signaturenya
            try:
                hex_sign = mixed_document[ds_index+4:-5]
                sign = int(hex_sign,16)
                return mixed_document[:ds_index],sign
            except ValueError:
                return -1,-1
        else:
            return -1,-1
    else:
        return -1,-1

def GetSignature(bytes_document,d,n):
    # Digital sign
    # Input :   Document to be signed in bytes format, private key (d,n)
    # Output :  Encrypted Hash Value (using RSA) --> Signature in string of hex

    # Hitung nilai Hash
    hash_value = hashlib.sha1(bytes_document)
    hash_value = hash_value.hexdigest()
    hash_value = int(hash_value,16)
    
    # RSA encrypt using private key d
    signature = (hash_value**d)%n
    
    signature_hex = hex(signature)
    signature_hexstr = signature_hex[2:len(signature_hex)]

    return signature_hexstr.upper()
    
def VerifySignature(bytes_document,signature_hexstr,e,n):
    # Verify signature
    # Input : Document to be verified in bytes format, signature in string of hex, public key (e,n)
    # Output : True if signature is verified, False otherwise
    
    try:
        hash_value_fromsign = int(signature_hexstr,16)
        hash_value_fromsign = (hash_value_fromsign**e)%n # RSA decrypt using public key e
    except ValueError:
        return False
    
    hash_value_fromdoc = hashlib.sha1(bytes_document)
    hash_value_fromdoc = hash_value_fromdoc.hexdigest()
    hash_value_fromdoc = int(hash_value_fromdoc,16)%n
    
    return hash_value_fromdoc == hash_value_fromsign