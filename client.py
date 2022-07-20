import socket
import threading
import random

from colorama import Fore, init, Back
from tkinter import *
from tkinter import font
from tkinter import ttk

SERVER = "192.168.42.46"
PORT = 5000

ADDRESS = (SERVER, PORT)

FORMAT = "utf-8"

color = "%06x" % random.randint(0, 0xFFFFFF)
usercolor = "#" + color

 
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)

class GUI:

    def __init__(self):
        

        self.Window = Tk()
        self.Window.withdraw()
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width = True, height = True)
        self.login.configure(width = 600,
                             height = 500,
                             bg = "#000000")

        self.pls = Label(self.login,
                       text = "Please pick a Username to continue",
                       justify = CENTER,
                       font = "Helvetica 14 bold",
                       fg = "#66ff00",
                       bg = "#000000")
         
        self.pls.place(relheight = 0.15,
                       relx = 0.2,
                       rely = 0.07)
       
        self.labelName = Label(self.login,
                               text = "Username: ",
                               font = "Helvetica 12",
                               fg = "#66ff00",
                               bg = "#000000")

         
        self.labelName.place(relheight = 0.2,
                             relx = 0.1,
                             rely = 0.2)
         
      
        self.entryName = Entry(self.login,
                             font = "Helvetica 14")

         
        self.entryName.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
      
        self.entryName.focus()
         
        # create a Button to join the chat 
        # along with action
        self.go = Button(self.login,
                         text = "Join",
                         font = "Helvetica 14 bold",
                         command = lambda: self.goAhead(self.entryName.get()))
         
        self.go.place(relx = 0.4,
                      rely = 0.55)
        self.Window.mainloop()
 
    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
         
    
        rcv = threading.Thread(target=self.receive)
        rcv.start()
 

    def layout(self,name):
       
        self.name = name
  
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = True,
                              height = True)
        self.Window.configure(width = 600,
                              height = 500,
                              bg = "#000000")

        name = usercolor
        self.labelHead = Label(self.Window,
                             bg = "#000000",
                              fg = usercolor,
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
         
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#000000")
         
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)

        
         
        self.textCons = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#000000",
                             fg = usercolor,
                             font = "Helvetica 14",
                             padx = 5,
                             pady = 5)
         
        self.textCons.place(relheight = 0.745,
                            relwidth = 1,
                            rely = 0.08)
         
        self.labelBottom = Label(self.Window,
                                 bg = "#000000",
                                 height = 80)
         
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
         
        self.entryMsg = Entry(self.labelBottom,  ########################
                              bg = "#000000",
                              fg = "#ffffff",
                              font = "Helvetica 13")
         
      
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
         
        self.entryMsg.focus()
 
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
         
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06,
                             relwidth = 0.22)
         
        self.textCons.config(cursor = "arrow")
         
    
        scrollbar = Scrollbar(self.textCons)
  
        scrollbar.place(relheight = 1,
                        relx = 0.974)
         
        scrollbar.config(command = self.textCons.yview)
         
        self.textCons.config(state = DISABLED)
 
 
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        snd= threading.Thread(target = self.sendMessage)
        snd.start()
 

    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                  
          
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
          
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END,
                                         message+"\n\n")
                     
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
            except:
             
                print("An error occured!")
                client.close()
                break
         

    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))   
            break   

g = GUI()
