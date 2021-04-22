# Dimodifikasi dari program pada tugas sebelumnya

import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import math

from Components import *
from FileHandlingWindow import *
from GenerateKeyWindow import *

from DigitalSignatureRSALib import *

class GUI:
    def __init__(self,parent):
        #--- init ---#
        self.parent = parent
        self.parent.title("Kriptografi RSA")
        
        #--- separate sign ---#
        self.sep_sign = tk.IntVar(value=1)
        
        #--- define grid ---#
        self.parent.columnconfigure([0,1,2,3],weight=1)
        self.parent.rowconfigure([0,1,2,3],weight=1,minsize=100)
        
        #--- title ---#
        self.title_frame = tk.Frame()
        tk.Label(master=self.title_frame,text="Digital Signature",font=("Arial",20)).pack()
        tk.Label(master=self.title_frame,text="Program tanda tangan digital dan verifikasi").pack()
        self.title_frame.grid(row=0,column=0,columnspan=2)
        
        #--- info key frame ---#
        self.key_e = -1
        self.key_d = -1
        self.key_n = -1
        self.key_list_frame = SubjectFrame("Key")
        self.key_list_frame.frame.grid(row=0,column=2)
        
        #--- key frame ---#
        key_button_list = ["Generate Key","Choose Public Key","Choose Private Key","Clear Key"]
        self.key_frame = ButtonListFrame(
            title = "Key Management",
            labels = key_button_list,
            width = 25
        )
        self.key_frame.button_list[0].bind("<Button-1>",self.GenerateKey)
        self.key_frame.button_list[1].bind("<Button-1>",lambda event,type="public": self.ChooseKeyFile(event,type))
        self.key_frame.button_list[2].bind("<Button-1>",lambda event,type="private": self.ChooseKeyFile(event,type))
        self.key_frame.button_list[3].bind("<Button-1>",lambda event: self.ClearKey(event))
        self.key_frame.frame.grid(row=1,column=2)
        
        #--- document ---#
        self.document = TextFrame(
            title="Document",
            width=60,
            height=10
        )
        self.document.frame.grid(row=1,column=0,columnspan=2)
        
        #--- button frame ---#
        self.button_frame = tk.Frame()
        
        #--- encrypt button ---#
        self.encrypt_button = tk.Button(master=self.button_frame,text="Sign Document",command=self.Encrypt,width=25)
        self.encrypt_button.pack(padx=2,pady=2)

        #--- decrypt button ---#
        self.decrypt_button = tk.Button(master=self.button_frame,text="Verify Signature",command=self.Decrypt,width=25)
        self.decrypt_button.pack(padx=2,pady=2)
        
        #--- check box ---#
        self.sep_sign_check = tk.Checkbutton(master=self.button_frame,text="Separate sign and document",variable=self.sep_sign,command=self.ChangeMode)
        self.sep_sign_check.pack(padx=2,pady=2)
        
        self.button_frame.grid(row=2,column=0,columnspan=2)
        
        #--- signature ---#
        self.signature = TextFrame(
            title="Signature",
            width=60,
            height=4
        )
        self.signature.frame.grid(row=3,column=0,columnspan=2)
        
        #--- file frame ---#
        file_method_list = ["Open Doc+Sign from File","Open Document from File","Open Signature from File","Save Doc+Sign from File","Save Document to File","Save Signature to File","File Sign and Verify"]
        self.file_frame = ButtonListFrame(
            title = "File",
            labels = file_method_list,
            width = 25
        )
        self.file_frame.button_list[0].bind("<Button-1>",lambda event,text="docsign": self.OpenFileText(event,text))
        self.file_frame.button_list[1].bind("<Button-1>",lambda event,text="document": self.OpenFileText(event,text))
        self.file_frame.button_list[2].bind("<Button-1>",lambda event,text="signature": self.OpenFileText(event,text))
        self.file_frame.button_list[3].bind("<Button-1>",lambda event,text="docsign": self.SaveFileText(event,text))
        self.file_frame.button_list[4].bind("<Button-1>",lambda event,text="document": self.SaveFileText(event,text))
        self.file_frame.button_list[5].bind("<Button-1>",lambda event,text="signature": self.SaveFileText(event,text))
        self.file_frame.button_list[6].bind("<Button-1>",self.SignFileWindow)
        self.file_frame.frame.grid(row=2,column=2,rowspan=2)  
        
    def ChangeMode(self):
        # Change mode in accordance to separate sign checkbox on self.sep_sign_check
        # Access via self.sep_sign variable (type: tk.IntVar) -> use .get() to access
        if (self.sep_sign.get()==1):
            self.signature.entry["state"]=tk.NORMAL
            self.signature.entry["bg"]="white"
        elif (self.sep_sign.get()==0):
            self.signature.entry.delete("1.0",tk.END)
            self.signature.entry["state"]=tk.DISABLED
            self.signature.entry["bg"]="light grey"
                
    def Encrypt(self):
        # Event handler when encrypt button is pressed
        # Encrypt document and key
        
        # Take the document and key from the field
        mix_doc = self.document.entry.get("1.0",tk.END)[:-1]
        document, sign = GetDocAndSign(mix_doc)
        if (sign==-1):
            document = mix_doc
            
        # Check for validity
        if (len(document)==0): # Empty document
            mb.showinfo(title="Alert",message="Please insert document")
        elif (sign!=-1):
            mb.showinfo(title="Alert",message="The document has been signed")
        else:    
            # Encrypt
            e = self.key_e 
            n = self.key_n
            state_sep_sign = self.sep_sign.get()   

            if (e==-1 or n==-1):
                mb.showinfo(title="Alert",message="Please choose key first")
            else:
                start_time = time.time()
                
                signature_hexstr = GetSignature(document,e,n,1)

                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # Insert into signature field
                if (state_sep_sign==1):
                    self.signature.entry.delete("1.0",tk.END)
                    self.signature.entry.insert("1.0",signature_hexstr)
                else:
                    self.document.entry.delete("1.0",tk.END)
                    self.document.entry.insert("1.0","<ds>" + signature_hexstr + "</ds>")
                    self.document.entry.insert("1.0",document)
                    
                mb.showinfo(title="Alert",message="Process finished in " + str(elapsed_time) + "s")
            
    def Decrypt(self):
        # Event handler when decrypt button is pressed
        # Decrypt signature and key
        
        # Take the signature and key from the field
        state_sep_sign = self.sep_sign.get()
        if (state_sep_sign==1):
            document = self.document.entry.get("1.0",tk.END)[:-1]
            signature = self.signature.entry.get("1.0",tk.END)[:-1]
            if ((len(document)==0) or (len(signature)==0)):
                data_available = 0  
            else:
                data_available = 1
        else:
            mix_doc = self.document.entry.get("1.0",tk.END)[:-1]
            document, signature = GetDocAndSign(mix_doc)
            if ((document==-1) or (signature==-1)):
                data_available = 0
            else:
                data_available = 1

        # Check for validity
        if (data_available == 0):
            mb.showinfo(title="Alert",message="Please insert document and/or signature")
        else:
            # Decrypt
            d = self.key_d 
            n = self.key_n
            
            if (d==-1 or n==-1):
                mb.showinfo(title="Alert",message="Please choose key first")
            else:            
                # Decrypt
                start_time = time.time()
                
                hash_value_byteintarray_fromsign = RSADecrypt(signature,d,n)
                hash_value_byteintarray_fromdoc = hashlib.sha1(document.encode())
                hash_value_byteintarray_fromdoc = hash_value_byteintarray_fromdoc.hexdigest()
                hash_value_byteintarray_fromdoc = StringToByteIntArray(hash_value_byteintarray_fromdoc)
                Verified = hash_value_byteintarray_fromdoc == hash_value_byteintarray_fromsign
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                if (Verified):
                    mb.showinfo(title="Verification",message="Signature is verified")
                else :
                    mb.showinfo(title="Verification",message="Signature is not verified")
                
                mb.showinfo(title="Alert",message="Process finished in " + str(elapsed_time) + "s")
        
    def GenerateKey(self,event):
        # Membuka window baru untuk membuat key baru
        key_window = GenerateKeyWindow(self.parent)
        key_window.window.grab_set()
        
        return "break"
        
    def ChooseKeyFile(self,event,type):
        if (type=="public"): # File public key
            public_filename = fd.askopenfilename(
                initialdir = "/",
                title = "Select public key file",
                filetypes = [("Public key files (.pub)","*.pub")]
            )
            
            if (public_filename!=""):
                # Baca file
                public_file = open(public_filename,"r")
                content_pub = public_file.read()
                
                # Ambil nilai e dan n
                d_pub = int(content_pub[0:(content_pub.find(' ')+1)])
                n_pub = int(content_pub[(content_pub.find(' ')+1):])
                
                public_file.close()

                # Masukkan isi file
                if (self.key_n==-1 or self.key_e==-1): # Jika n Alice belum diset (key Alice belum diset), atau baru e dan n Alice yang diset, masukkan e dan n langsung
                    self.key_d = d_pub
                    self.key_n = n_pub
                    self.key_list_frame.UpdateKey(self.key_e,self.key_d,self.key_n)
                elif (self.key_e!=-1 and self.key_n==n_pub): # Jika d dan n Alice sudah diset dan sesuai dengan n baru
                    if (math.gcd(d_pub,self.key_e)==1):
                        self.key_d = d_pub
                        self.key_n = n_pub
                        self.key_list_frame.UpdateKey(self.key_e,self.key_d,self.key_n)
                    else:
                        mb.showinfo(title="Alert",message="Ada kesalahan pada key, silakan cek lagi.")
                else:
                    mb.showinfo(title="Alert",message="Ada kesalahan pada key, silakan cek lagi.")
        
        elif (type=="private"):
            private_filename = fd.askopenfilename(
                initialdir = "/",
                title = "Select private key file",
                filetypes = [("Private key files (.pri)","*.pri")]
            )
            
            if (private_filename!=""):
                private_file = open(private_filename,"r")
                content_pri = private_file.read()
                
                e_pri = int(content_pri[0:(content_pri.find(' ')+1)])
                n_pri = int(content_pri[(content_pri.find(' ')+1):])
                
                private_file.close()
                
                if (self.key_n==-1 or self.key_d==-1): # Jika n Alice belum diset (key Alice belum diset), atau baru e dan n Alice yang diset, masukkan e dan n langsung
                    self.key_e = e_pri
                    self.key_n = n_pri
                    self.key_list_frame.UpdateKey(self.key_e,self.key_d,self.key_n)
                elif (self.key_d!=-1 and self.key_n==n_pri): # Jika d dan n Alice sudah diset dan sesuai dengan n baru
                    if (math.gcd(e_pri,self.key_d)==1):
                        self.key_e = e_pri
                        self.key_n = n_pri
                        self.key_list_frame.UpdateKey(self.key_e,self.key_d,self.key_n)
                    else:
                        mb.showinfo(title="Alert",message="Ada kesalahan pada key, silakan cek lagi.")
                else:
                    mb.showinfo(title="Alert",message="Ada kesalahan pada key, silakan cek lagi.")
                            
        return "break"
        
    def ClearKey(self,event):
        # Event handler when key is cleared
        # Set all key to -1 and update the view
        self.key_e = -1
        self.key_d = -1
        self.key_n = -1
        self.key_list_frame.UpdateKey("-1","-1","-1")
        
    def OpenFileText(self,event,text):
        # Open file using open file dialog
        
        # Take filename
        filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select " + text + " file",
            filetypes = [("Text files (.txt)","*.txt"),("All files","*.*")]
        )
        
        if (filename!=""): # If filename is chosen
            content = OpenFileAsByteIntArray(filename)
            content_bytes = bytes(content)
            
            if (text=="document"): # For document, insert to document field
                self.document.entry.delete("1.0",tk.END)
                self.document.entry.insert("1.0",content_bytes)
            elif (text=="signature"): # For signature, insert to signature field
                self.signature.entry.delete("1.0",tk.END)
                self.signature.entry.insert("1.0",content_bytes)
            elif (text=="docsign"):
                self.document.entry.delete("1.0",tk.END)
                self.document.entry.insert("1.0",content_bytes)
                self.signature.entry.delete("1.0",tk.END)
                self.sep_sign_check.deselect()
                self.signature.entry.delete("1.0",tk.END)
                self.signature.entry["state"]=tk.DISABLED
                self.signature.entry["bg"]="light grey"
        
        return "break"
        
    def SaveFileText(self,event,text):
        # Save file using save file dialog
        
        # Take filename
        filename = fd.asksaveasfilename(
            initialdir = "/",
            title = "Select " + text + " file",
            filetypes = [("Text files (.txt)","*.txt"),("All files","*.*")],
            defaultextension = [("Text files (.txt)","*.txt"),("All files","*.*")]
        )
        
        if (filename!=""): # If file name is chosen
            file = open(filename,"wb")
            if (text=="document"): # For document, insert the document
                document = self.document.entry.get("1.0",tk.END)[:-1]
                document_byteintarray = StringToByteIntArray(document)
                for byteint in document_byteintarray:
                    file.write(byteint.to_bytes(1,byteorder='little'))
            elif (text=="signature"): # For signature, insert the signature
                signature = self.signature.entry.get("1.0",tk.END)[:-1]
                signature_byteintarray = StringToByteIntArray(signature)
                for byteint in signature_byteintarray:
                    file.write(byteint.to_bytes(1,byteorder='little'))
            elif (text=="docsign"):
                pass
                
            file.close()
        
        return "break"
        
    def SignFileWindow(self,event):
        # Create new window for file encrypt/decrypt
        # Components : label, key entry, and buttons
        file_window = FileHandlingWindow(self.parent)
        file_window.window.grab_set()
        
        return "break"