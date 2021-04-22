import math

def StringToByteIntArray(string):
    # Mengubah string menjadi array of integer (byte) sesuai dengan ascii/utf-8
    # Input : string
    # Output : array of integer (byte) dari string
    byteint_array = []
    
    for char in string:
        byteint_array.append(ord(char))
        
    return byteint_array
    
def HexStringToByteIntArray(hexstring):
    # Mengubah string heksadesimal menjadi array of integer(byte)
    # Input : string hexadecimal
    # Output : array of integer (byte) dari string
    byteint_array = []
    
    i = 0
    while (i<len(hexstring)):
        if (i==len(hexstring)-1): # Jika panjang string hex ganjil, tambahkan 0
            byteint_array.append(int(hexstring[i]+"0",16))
            i = i + 1
        else: # Pasangkan setiap dua digit hexadecimal menjadi satu byte
            byteint_array.append(int(hexstring[i:i+2],16))
            i = i + 2
        
    return byteint_array

def ByteIntArrayToHexString(byteint_array):
    # Mengubah string heksadesimal menjadi array of integer(byte)
    # Input : string hexadecimal
    # Output : array of integer (byte) dari string
    
    hexstring = ""
    for byte in byteint_array:
        cipher_hex = str(hex(byte))[2:].upper()
        if (len(cipher_hex)==1):
            cipher_hex = '0'+cipher_hex
        hexstring = hexstring + cipher_hex

    return hexstring

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
    
def BlockByteIntArray(byteint_array,size):
    # Membagi byte int array menjadi blok-blok dengan size tertentu
    # Input : array of int (byte)
    #         block size (dalam byte)
    # Output :  array dengan elemen masing-masing blok
    
    if (size==1): # Jika size 1 byte, sama saja seperti array awal
        return byteint_array
    else:
        blocked_byteintarray = []
        i = 0
        while (i<len(byteint_array)):
            # Siapkan block (dalam string)
            block = ""
            
            # Ambil byte sebanyak size
            for j in range(size):
                if ((i+j)<len(byteint_array)):
                    # Tambahkan leading zero ke blok tersebut
                    if (byteint_array[i+j]<10):
                        block += "00" + str(byteint_array[i+j])
                    elif (byteint_array[i+j]<100):
                        block += "0" + str(byteint_array[i+j])
                    else:
                        block += str(byteint_array[i+j])
                else:
                    # Byte sudah habis tetapi masih ada blok yang belum penuh, tambahkan dengan null character
                    block += str(ord('\0'))
                
            # next element
            i = i + size
            blocked_byteintarray.append(int(block))
            
        return blocked_byteintarray
        
def BlockCiphertext(ciphertext,n):
    # Membagi ciphertext dengan panjang blok sesuai ceil(16 log n)
    # Input : ciphertext panjang dalam digit hexadecimal
    # Output : array ciphertext per blok sesuai ceil(16 log n)
    
    # Siapkan parameter
    block_size = math.ceil(math.log(n,16))
    
    # Siapkan ciphertext menjadi string
    ciphertext_string = str(ciphertext)
    
    # Buat blok ciphertext
    ciphertext_block = []
    i = 0
    while (i<len(ciphertext_string)):
        block = ""
        for j in range(block_size):
            if ((i+j)<len(ciphertext_string)):
                block += ciphertext_string[i+j]
            else:
                block += "0"
        
        i = i + block_size
        ciphertext_block.append(int(block,16))

    return ciphertext_block
    
def RSAEncrypt(plaintext_byteintarray,e,n,size):
    # RSA Encrypt
    # Input :   plaintext_byteintarray (byte in array)
    #           key (e,n)
    #           block size
    # Output :  ciphertext string (in hex)

    # Bagi plaintext menjadi block sesuai dengan block size
    plaintext_blocks = BlockByteIntArray(plaintext_byteintarray,size)
    
    # Siapkan parameter block size ciphertext
    ciphertext_blocksize = math.ceil(math.log(n,16))

    # Buat ciphertext (dalam bentuk string hexadecimal agar leading zero tidak hilang)
    ciphertext_hexstr = ""
    for block in plaintext_blocks:
        # Hitung hasil enkripsi dari blok plaintext
        cipher_block = (block**e)%n
        
        # Ubah menjadi string hexadecimal
        cipher_hex = str(hex(cipher_block))[2:].upper()
        
        # Tambahkan leading zero
        if (len(cipher_hex)<ciphertext_blocksize):
            leading_zero = "0" * (ciphertext_blocksize-len(cipher_hex))
            cipher_hex = leading_zero + cipher_hex

        # Masukkan ke string hexadecimal
        ciphertext_hexstr += cipher_hex
    
    return ciphertext_hexstr
    
def RSADecrypt(ciphertext_hexstr,d,n):
    # RSA Decrypt
    # Input :   ciphertext_hexstr (string of hexadecimal)
    #           key (d,n)
    # Output :  plaintext (byte in array)

    # Ubah ciphertext (string hex) menjadi block (of int)
    ciphertext_blocks = BlockCiphertext(ciphertext_hexstr,n)

    # Buat plaintext (dalam bentuk array of integer (byte))
    plaintext_byteintarray = []
    for block in ciphertext_blocks:
        # Hitung hasil dekripsi dari blok ciphertext
        plaintext_block = (block**d)%n
        
        # Ubah menjadi string lalu cetak leading zero agar string menjadi kelipatan 3 digit
        plaintext_blockstr = str(plaintext_block)
        if (len(plaintext_blockstr)%3!=0):
            leading_zero = "0" * (3-len(plaintext_blockstr)%3)
            plaintext_blockstr = leading_zero + plaintext_blockstr
            
        # Ambil setiap 3 digit lalu ubah menjadi byte, masukkan ke array
        i = 0
        while (i<len(plaintext_blockstr)):
            num = plaintext_blockstr[i:i+3]
            plaintext_byteintarray.append(int(num))
            i = i + 3
            
    return plaintext_byteintarray