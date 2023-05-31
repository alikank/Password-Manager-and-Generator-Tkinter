import random
import tkinter as tk
from tkinter import messagebox
import sqlite3

aktif = False
#database
baglanti = sqlite3.connect("sifre.db")
cursor = baglanti.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sifre(id INTEGER PRIMARY KEY AUTOINCREMENT,site varchar(80),sifre varchar(255))")

ana = tk.Tk()
ana.geometry("500x500")
ana.resizable(width="false", height="false")
ana.title("Şifre Yöneticisi v1")

global_liste = 0

class Sifre:
    def __init__(self):
        self.bolge1 = tk.Frame(ana,padx=15,pady=15,relief="ridge")
        self.bolge1.pack(side="top",anchor="center")
        self.bolge2 = tk.Frame(ana,padx=15,pady=15,relief="ridge")
        self.bolge2.pack(side="top",anchor="center")
        self.bolge3 = tk.Frame(ana,padx=15,pady=15,relief="ridge")
        self.bolge3.pack(side="top",anchor="center")

        self.lbl1 = tk.Label(self.bolge1,text="Hane : ",font="Calibri").grid(row=0,column=0)

        self.hanent = tk.Entry(self.bolge1,font="Calibri",width = 15)
        self.hanent.grid(row=0,column=1)

        self.uret = tk.Button(self.bolge1,text="RASTGELE ŞİFRE ÜRET",font="Verdana 10 bold",command=self.sifre_uret,width=25,height=3,bg='#45b592',fg='#ffffff',bd=0)
        self.uret.grid(row=1,column=0,columnspan=2,pady=10)
        
        self.deger=""
        self.lbl2 = tk.Label(self.bolge2,text="",font="Calibri 10",pady=10,anchor="center")
        self.lbl2.grid(row=2,column=0)

        self.listbutton = tk.Button(ana,text="Kaydedilmiş Şifreleri Görüntüle",anchor="center",border=1,relief="raised",fg="#45b592",command=lambda:Liste())
        self.listbutton.pack(side="bottom",fill="x")
        

    def sifre_uret(self):
        try:
            self.hane = int(self.hanent.get())
            self.sifre = ""
            karakterler = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ?.!#@0123456789"
            for i in range(self.hane):
                cek = random.randint(0,len(karakterler)-1)
                self.sifre += str(karakterler[cek])
            self.lbl2.config(text="Üretilen Şifre : \n"+self.sifre) 

            self.kopyala = tk.Button(self.bolge2,text="Kopyala",font="Verdana 12 bold",command=lambda:(ana.clipboard_clear(),ana.clipboard_append(self.sifre),ana.update()))
            self.kopyala.grid(row=3,column=0,columnspan=2)

            self.lbl3 = tk.Label(self.bolge3,text="Website : ",font="Verdana 10",pady=15).grid(row=0,column=0)
            self.webent = tk.Entry(self.bolge3,font="Calibri",width = 16)
            self.webent.grid(row=0,column=1)

            self.kaydet = tk.Button(self.bolge3,text="Şifreyi Kaydet",font="Verdana 12 bold",pady=10,width=15,bg='#45b592',fg='#ffffff',bd=0,command=self.dbkaydet)
            self.kaydet.grid(row=1,column=0,columnspan=2,rowspan=2)
        except:
            messagebox.showerror("Hata Oluştu!", "Girilen hane tam sayı olmalı.")


    def dbkaydet(self):
        cursor.execute("INSERT INTO sifre(site,sifre) VALUES (?,?)",(self.webent.get(),self.sifre))
        try:
            baglanti.commit()
            messagebox.showinfo("Başarıyla Eklendi !", "Şifre başarıyla eklendi !")
        except:
            messagebox.showerror("Hata Oluştu!", "Veritabanı bağlantısında hata var.")
        finally:
            global aktif
            if aktif:
                global_liste.pencerekapat()
                Liste()
                



class Liste:
    def __init__(self):
            global aktif, global_liste
            global_liste = self
            if(not aktif):
                aktif = True
                self.ek = tk.Tk()
                self.ek.geometry("780x1000+350+0")
                self.ek.resizable(width="false", height="false")
                self.ek.title("Şifre Yöneticisi v1 (Şifre Listesi)")
                self.ek.protocol("WM_DELETE_WINDOW", self.pencerekapat)
                self.scrollbar = tk.Scrollbar(self.ek)
                self.scrollbar.pack(side="right", fill="y")
                self.liste = tk.Listbox(self.ek,selectmode="multiple",width=100,height=70,selectbackground="blue")
                self.liste.pack(side="left",fill="y")
                self.liste.config(yscrollcommand=self.scrollbar.set)
                self.scrollbar.config(command=self.liste.yview)
                self.sifrelistele()
                self.ek.mainloop()


    def sifrelistele(self):
        cursor.execute("SELECT * FROM sifre")
        sifreler = cursor.fetchall()      
        for i in range(len(sifreler)):
            for j in range(len(sifreler[0])):
                if(j==0): # id alanını daralt
                    self.e = tk.Entry(self.liste, width=3,font=('Arial', 10))
                elif(j==1): # website alanını daralt
                    self.e = tk.Entry(self.liste, width=15,font=('Arial', 10))
                else: # şifre alanını genişlet
                    self.e = tk.Entry(self.liste, width=55,font=('Arial', 12))
                self.e.grid(row=i, column=j)
                self.e.insert("end", sifreler[i][j])
            self.button = tk.Button(self.liste, text="SİL",anchor="center",width=15,bg='#45b592',fg='#ffffff',bd=0,command=lambda id=sifreler[i][0]: self.sil(id))   
            self.button.grid(row=i,column=j+2,columnspan=2) 

    def sil(self,id):
        self.id = id
        cursor.execute("DELETE FROM sifre where id=?",(self.id,))
        try:
            baglanti.commit()
            messagebox.showinfo("Başarıyla Silindi !", "İlgili Kayıt Başarıyla Silindi !")
        except: 
            messagebox.showerror("Hata Oluştu!", "Veritabanı bağlantısında hata var.")
        finally:
            self.pencerekapat() # tabloyu güncelle   
            Liste()
                                

    def pencerekapat(self):
        global aktif
        aktif = False
        self.ek.destroy()
                

class Main:
    Sifre()
    ana.mainloop()


Main()    
     



