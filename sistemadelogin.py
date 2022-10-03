from cProfile import label
from calendar import c
from tkinter import *
import sqlite3


con = sqlite3.connect('usuarios.db')
cursor = con.cursor()

sql_create= 'create table usuarios (nome varchar (30), senha varchar (30))'
sql_insert= 'insert into usuarios values (?, ?)'
sql_select= 'select * from usuarios'

'''con.execute('DROP TABLE usuarios')
cursor.execute(sql_create)'''

usuarios = {}

cursor.execute(sql_select)
for x in cursor.fetchall():
    usuarios[x[0]] = x[1]

class Application:
    def __init__(self, master=None):
        self.fontepadrao = ("Arial", "10")
        
        self.container1 = Frame(master)
        self.container1["pady"] = 10
        self.container1.pack()
        
        self.container2 = Frame(master)
        self.container2["padx"] = 20
        self.container2.pack()

        self.container3 = Frame(master)
        self.container3["padx"] = 20
        self.container3["pady"] = 10
        self.container3.pack()

        self.container4 = Frame(master)
        self.container4["padx"] = 20
        self.container4["pady"] = 10
        self.container4.pack()

        self.container5 = Frame(master)
        self.container5["pady"] = 20
        self.container5.pack()

        self.titulo = Label(self.container1, text="Dados do usuário", font=("Arial", "10", "bold"))
        self.titulo.pack()

        self.nomelabel = Label(self.container2, text="Nome", font= self.fontepadrao)
        self.nomelabel.pack(side=LEFT)

        self.nome = Entry(self.container2)
        self.nome["width"] = 30
        self.nome["font"] = self.fontepadrao
        self.nome.pack(side=LEFT)

        self.senhalabel = Label(self.container3, text="Senha")
        self.senhalabel["font"] = self.fontepadrao
        self.senhalabel.pack(side=LEFT)

        self.senha = Entry(self.container3)
        self.senha["width"] = 30
        self.senha["font"] = self.fontepadrao
        self.senha["show"] = "*"
        self.senha.pack(side=LEFT)

        self.senhabotao = Button(self.container4, text="Mostrar senha", font=("Arial", "7"), width=12, command=self.mostraSenha)
        self.senhabotao.pack(side=RIGHT)

        self.senhabotao = Button(self.container4, text="Esconder senha", font=("Arial", "7"), width=12, command=self.escondesenha)
        self.senhabotao.pack(side=RIGHT)

        self.login = Button(self.container5, text="Login", font=self.fontepadrao, width=12,command= self.verificalogin)
        self.login.pack()
        
        self.cadastro = Button(self.container5, text="Cadastrar", font=self.fontepadrao, width=12, command=self.cadastrar) 
        self.cadastro.pack()

        self.msg = Label(self.container5, text= "", font=self.fontepadrao)
        self.msg.pack()

    def verificalogin(self):
        usuario = str(self.nome.get())
        senha = str(self.senha.get())
        if usuario not in usuarios or senha != usuarios[usuario]:
            self.msg["text"] = "Usuário ou senha incorretos."
            self.msg["fg"] = "red"
        elif usuario in usuarios and usuarios[usuario] == senha:
            self.msg["text"] = "Login feito!"
            self.msg["fg"] = "darkgreen"
    def mostraSenha(self):  
        self.senha["show"] = ""   
    def escondesenha(self):
        self.senha["show"] = "*"
    def cadastrar(self):
        usuario = self.nome.get()
        senha = self.senha.get()
        if usuario in usuarios:
            self.msg["text"] = "Usuário já possui cadastrado. Tente o login."
            self.msg["fg"] = "green"
        elif usuario not in usuarios:
            usuarios[usuario] = senha
            lst = [usuario, senha]
            cursor.execute(sql_insert,lst)
            lst.clear()
            print(usuarios)
            cursor.execute(sql_select)
            print(cursor.fetchall())
            self.msg["text"] = "Usuário cadastrado."
            self.msg["fg"] = "green"
            con.commit()

        
root = Tk()
root.geometry("600x300")
Application(root)
root.mainloop()
con.close()