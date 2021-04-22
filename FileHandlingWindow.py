import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import math
import time

from DigitalSignatureRSALib import *

class FileHandlingWindow:
    def __init__(self,parent):
        self.parent = parent
        self.window = tk.Toplevel(self.parent)
        self.window.title("File Sign/Verify")
        
        self.file = ""
        self.key = ""
        self.e_key = ""
        self.d_key = ""
        self.n_key = ""

        # Define elements
        self.file_label = tk.Label(master=self.window,text="File : " + self.file,width=50)
        self.file_label.grid(row=0,column=0,columnspan=2,sticky="we",padx=120,pady=2)
        self.key_label = tk.Label(master=self.window,text="Key : " + self.key,width=50)
        self.key_label.grid(row=1,column=0,columnspan=2,sticky="we",padx=120,pady=2)

        self.e_key_label = tk.Label(master=self.window,text="e: ")
        self.e_key_label.grid(row=3,column=0,columnspan=2,padx=120,pady=2)
        self.e_key_entry = tk.Text(master=self.window,width=10,height=1)
        self.e_key_entry.grid(row=3,column=1,padx=120,pady=2)

        self.d_key_label = tk.Label(master=self.window,text="d: ")
        self.d_key_label.grid(row=4,column=0,columnspan=2,padx=120,pady=2)
        self.d_key_entry = tk.Text(master=self.window,width=10,height=1)
        self.d_key_entry.grid(row=4,column=1,padx=120,pady=2)

        self.n_key_label = tk.Label(master=self.window,text="n: ")
        self.n_key_label.grid(row=5,column=0,columnspan=2,padx=120,pady=2)
        self.n_key_entry = tk.Text(master=self.window,width=10,height=1)
        self.n_key_entry.grid(row=5,column=1,padx=120,pady=2)
        
        # Button list
        tk.Button(master=self.window,text="Choose File",width=20,command=self.ChooseFile).grid(row=6,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Choose Public Key",width=20,command=self.ChoosePublicKey).grid(row=7,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Choose Private Key",width=20,command=self.ChoosePrivateKey).grid(row=8,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Encrypt and Save",width=20,command=self.SaveEncryptedFile).grid(row=9,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Decrypt and Save",width=20,command=self.SaveDecryptedFile).grid(row=10,column=0,columnspan=2,pady=2)
        tk.Button(master=self.window,text="Unselect File",width=20,command=self.UnselectFile).grid(row=11,column=0,columnspan=2,pady=2)
        
    def ChooseFile(self):
        # Take filename
        filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select  file",
            filetypes = [("All files","*.*")],
        )
        
        if (filename!=""):
            self.file_label["text"] = "File : " + filename
            self.file = filename

    def ChoosePublicKey(self):
        public_filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select public key file",
            filetypes = [("Public key files (.pub)","*.pub")]
        )
        
        if (public_filename!=""):
            public_file = open(public_filename,"r")
            content_pub = public_file.read()
            
            e_pub = int(content_pub[0:(content_pub.find(' ')+1)])
            n_pub = int(content_pub[(content_pub.find(' ')+1):])
            
            public_file.close()
            
            self.e_key_entry.delete("1.0",tk.END)
            self.e_key_entry.insert("1.0",e_pub)
            self.d_key_entry.delete("1.0",tk.END)
            self.n_key_entry.delete("1.0",tk.END)
            self.n_key_entry.insert("1.0",n_pub)
            
            self.key_label["text"] = "Key : " + "Loaded"
            self.key = "Loaded"
            
        return "break"
        
    def ChoosePrivateKey(self):
        private_filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select private key file",
            filetypes = [("Private key files (.pri)","*.pri")]
        )
        
        if (private_filename!=""):
            private_file = open(private_filename,"r")
            content_pri = private_file.read()
            
            d_pri = int(content_pri[0:(content_pri.find(' ')+1)])
            n_pri = int(content_pri[(content_pri.find(' '))+1:])
            
            private_file.close()
            
            self.e_key_entry.delete("1.0",tk.END)
            self.d_key_entry.delete("1.0",tk.END)
            self.d_key_entry.insert("1.0",d_pri)
            self.n_key_entry.delete("1.0",tk.END)
            self.n_key_entry.insert("1.0",n_pri)
            
            self.key_label["text"] = "Key : " + "Loaded"
            self.key = "Loaded"
        
        return "break"
                
    def SaveEncryptedFile(self):
        # buka file di self.file 
        if (self.file==""):
            mb.showinfo(title="Alert",message="Please choose a file")
        else:
            #encrypt
            e = self.e_key_entry.get("1.0",tk.END)[:-1]
            #d = self.d_key_entry.get("1.0",tk.END)[:-1]
            n = self.n_key_entry.get("1.0",tk.END)[:-1]
            
            if (len(e)==0 or len(n)==0):
                mb.showinfo(title="Alert",message="Please insert e and n")
            else: 
                e = int(e)
                #d = int(d)
                n = int(n)
                
                start_time = time.time()
                
                # baca file per byte lalu simpan menjadi array of integer (byte)
                plaintext_byteintarray = OpenFileAsByteIntArray(self.file)

                #print (plaintext_byteintarray)
                
                # encrypt
                size = 1
                ciphertext_hexstr = RSAEncrypt(plaintext_byteintarray,e,n,size)
                ciphertext_byteintarray = HexStringToByteIntArray(ciphertext_hexstr)
                #print(ciphertext_hexstr)
                #print(ciphertext_byteintarray)

                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # save
                filename = fd.asksaveasfilename(
                    initialdir = "/",
                    title = "Save file",
                    filetypes = [("All files","*.*")],
                    defaultextension = [("All files","*.*")]
                )
                if (filename!=""):
                    # save hasil enkripsi per byte
                    output_file = open(filename, "wb")
                        
                    for byteint in ciphertext_byteintarray:
                        output_file.write(byteint.to_bytes(1,byteorder='little'))
                     
                    output_file.close()
                    
                    mb.showinfo(title="Alert",message="Process finished in "+str(elapsed_time)+" s and "+str(len(ciphertext_byteintarray))+" bytes")
        
    def SaveDecryptedFile(self):
        # buka file di self.file 
        if (self.file==""):
            mb.showinfo(title="Alert",message="Please choose a file")
        else:
            # decrypt
            #e = self.e_key_entry.get("1.0",tk.END)[:-1]
            d = self.d_key_entry.get("1.0",tk.END)[:-1]
            n = self.n_key_entry.get("1.0",tk.END)[:-1]

            if (len(d)==0 or len(n)==0):
                mb.showinfo(title="Alert",message="Please insert d and n")
            else:            
                #e = int(e)
                d = int(d)
                n = int(n)
            
                start_time = time.time()
            
                # baca file per byte lalu simpan menjadi array of integer (byte)
                ciphertext_byteintarray = OpenFileAsByteIntArray(self.file)
                ciphertext_hexstr = ByteIntArrayToHexString(ciphertext_byteintarray)
                #print(ciphertext_hexstr)
                #print(ciphertext_byteintarray)
                
                # decrypt
                plaintext_byteintarray = RSADecrypt(ciphertext_hexstr,d,n)
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                #print(plaintext_byteintarray)

                # save
                filename = fd.asksaveasfilename(
                    initialdir = "/",
                    title = "Save file",
                    filetypes = [("All files","*.*")],
                    defaultextension = [("All files","*.*")]
                )
                if (filename!=""):
                    # save hasil enkripsi per byte
                    output_file = open(filename, "wb")
                    
                    for byteint in plaintext_byteintarray:
                        output_file.write(byteint.to_bytes(1,byteorder='little'))
                    
                    output_file.close()
                    
                    mb.showinfo(title="Alert",message="Process finished in "+str(elapsed_time)+" s and "+str(len(plaintext_byteintarray))+" bytes")
    
    def UnselectFile(self):
        self.file = ""
        self.file_label["text"] = "File : " + self.file
