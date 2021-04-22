import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as fd
import tkinter.messagebox as mb

from GenerateKeyLib import *

class GenerateKeyWindow:
    def __init__(self,parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Generate Key")
        
        self.title_label = tk.Label(master=self.window,text="Please insert two prime numbers",width=50)
        self.title_label.grid(row=0,column=0,columnspan=2,padx=2,pady=2)
        
        self.info_label = tk.Label(master=self.window,text="Non prime numbers will be converted to nearest prime number",width=50)
        self.info_label.grid(row=1,column=0,columnspan=2,padx=2,pady=2)
        
        self.p_label = tk.Label(master=self.window,text="p: ")
        self.p_label.grid(row=2,column=0,padx=2,pady=2)
        
        self.p_entry = tk.Text(master=self.window,width=30,height=2)
        self.p_entry.grid(row=2,column=1,padx=2,pady=2)
        
        self.q_label = tk.Label(master=self.window,text="q: ")
        self.q_label.grid(row=3,column=0,padx=2,pady=2)
        
        self.q_entry = tk.Text(master=self.window,width=30,height=2)
        self.q_entry.grid(row=3,column=1,padx=2,pady=2)
        
        self.generate_button = tk.Button(master=self.window,text="Generate Key",width=25,command=self.GenerateKey)
        self.generate_button.grid(row=4,column=0,columnspan=2,padx=2,pady=2)
        
        self.randomize_button_8 = tk.Button(master=self.window,text="Randomize Number (8 bit)",width=25,command=lambda size=8: self.RandomizeKey(size))
        self.randomize_button_8.grid(row=5,column=0,columnspan=2,padx=2,pady=2)
        
        self.randomize_button_16 = tk.Button(master=self.window,text="Randomize Number (16 bit)",width=25,command=lambda size=16: self.RandomizeKey(size))
        self.randomize_button_16.grid(row=6,column=0,columnspan=2,padx=2,pady=2)
        
        self.alert = tk.Label(master=self.window,text="Large number may take a long time to process. Please wait a bit.")
        self.alert.grid(row=9,column=0,columnspan=2,padx=2,pady=2)
        
    def GenerateKey(self):
        # Validation
        p = self.p_entry.get("1.0",tk.END)[:-1]
        q = self.q_entry.get("1.0",tk.END)[:-1]
        
        if (len(p)==0 or len(q)==0):
            mb.showinfo(title="Alert",message="Please insert the numbers")
        else:
            p = int(p)
            q = int(q)

            p = ValidationPrime(p)
            q = ValidationPrime(q)

            # Generate key
            arr = GenerateKey(p, q)
            e = arr[0]
            d = arr[1]
            n = arr[2]

            # Save Key pair to file
            success = False
        
            public_filename = fd.asksaveasfilename(
                initialdir = "/",
                title = "Save public key file",
                filetypes = [("Public key files (.pub)","*.pub")],
                defaultextension = [("Public key files (.pub)","*.pub")]
            )
            
            if (public_filename!=""):
                private_filename = fd.asksaveasfilename(
                    initialdir = public_filename[0:(public_filename.rfind('/')+1)],
                    title = "Save private key file",
                    filetypes = [("Private key files (.pri)","*.pri")],
                    defaultextension = [("Private key files (.pri)","*.pri")]
                )
                
                if (private_filename!=""):
                    success = True 
            
            if (success):
                public_file = open(public_filename,"w")
                
                public_file.write(str(e))
                public_file.write(" ")
                public_file.write(str(n))
                
                public_file.close()
                
                private_file = open(private_filename,"w")
                
                private_file.write(str(d))
                private_file.write(" ")
                private_file.write(str(n))
                
                private_file.close()
                
                mb.showinfo(title="Alert",message="File saved to "+public_filename+" and "+private_filename)
                
                self.window.destroy()
        
        
    def RandomizeKey(self,size):
        # generate key
        out = RandomKey(size)
        p = out[0]
        q = out[1]

        self.p_entry.delete("1.0",tk.END)
        self.p_entry.insert("1.0",p)
        self.q_entry.delete("1.0",tk.END)
        self.q_entry.insert("1.0",q)