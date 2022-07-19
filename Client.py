# import all the modules you will need.
import socket
import threading
import random

from colorama import Fore, init, Back
from tkinter import *
from tkinter import font
from tkinter import ttk

# Bind client ip and port
SERVER = "192.168.42.46"
PORT = 5000
# Create a Tuple for the ADDRESS variable 
ADDRESS = (SERVER, PORT)

FORMAT = "utf-8"
# create random color 
color = "%06x" % random.randint(0, 0xFFFFFF)
usercolor = "#" + color

 
# Create a new client
# Then connect the client to the server
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)

#Creation of the class for the Window
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

        # create a Label
        self.pls = Label(self.login,
                       text = "Please pick a Username to continue",
                       justify = CENTER,
                       font = "Helvetica 14 bold",
                       fg = "#66ff00",
                       bg = "#000000")
         
        self.pls.place(relheight = 0.15,
                       relx = 0.2,
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Username: ",
                               font = "Helvetica 12",
                               fg = "#66ff00",
                               bg = "#000000")

         
        self.labelName.place(relheight = 0.2,
                             relx = 0.1,
                             rely = 0.2)
         
        # create a entry box 
        self.entryName = Entry(self.login,
                             font = "Helvetica 14")

         
        self.entryName.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
         
        # set the focus of the curser
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
         
        # receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()
 
    # layout of the chat
    def layout(self,name):
       
        self.name = name
        # chat window
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
         
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
         
        self.entryMsg.focus()
         
        # create a Send Button
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
         
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
         
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
         
        scrollbar.config(command = self.textCons.yview)
         
        self.textCons.config(state = DISABLED)
 
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        snd= threading.Thread(target = self.sendMessage)
        snd.start()
 
    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                  
                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END,
                                         message+"\n\n")
                     
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                client.close()
                break
         
    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))   
            break   
 
# create a GUI class object
g = GUI()
