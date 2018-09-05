from tkinter import *
from tkinter.filedialog import askopenfilename
import ftplib

vfiles = ""
loggedin = False
#enter FTP server credentials to access server
session = ftplib.FTP('<IP>', '<Username>', '<Password>')
login = {'Maanav': 'jeff', 'Parth': 'mouse'}
user = ''


def Validate(u, p, w):
    global loggedin , user
    user = u.get()
    password = p.get()
    if user in login:
        if password == login[user]:
            loggedin = True
            w.destroy()
            session.cwd(user)
            ViewFiles()


def Login():
    user_text = StringVar()
    pass_text = StringVar()
    login = Toplevel()
    login.geometry('300x300')
    Label(login, text='Username').pack()
    Entry(login, textvariable=user_text).pack()
    Label(login, text='Password').pack()
    Entry(login, textvariable=pass_text, show='*').pack()
    Button(login, text="Login", command=lambda: Validate(user_text, pass_text, login)).pack()


def ViewFiles():
    if loggedin == True:
        files = session.nlst()
        for i in files:
            try:
                session.cwd(i)
                temp = session.nlst()
                for j in temp:
                    files.insert(files.index(i) + 1, '\t' + j)
                files[files.index(i)] = i + '/'
            except Exception:
                print()
            session.cwd('/')
            session.cwd(user)
        vfiles = '\n'.join(files)
        Label(root, text='Current Files:\n\n' + vfiles, justify='left', font=(None, 10)).grid(row=0, column=2, pady=10)
    else:
        Button(root, text='Login', command=lambda: Login()).grid(row=7, column=2)


def AboutApp():
    gui = Tk()
    abttxt = "Use this app to upload/download files to your drive\nCreated By: Maanav Acharya, Parth Dalal\n\t\t-T.E Comps, KJSIEIT"
    Label(gui, text=abttxt).pack()


def OpenFile(text):
    name = askopenfilename(initialdir="/", filetypes=(("All Files", "*.*"), ("Text File", "*.txt")),
                           title="Choose a file.")
    text.set(name)


def Upload(path):
    file = open(path, 'rb')
    ufname = path.split('/')[-1]
    session.storbinary("STOR " + ufname, file)
    ViewFiles()


def Download(path):
    if '/' in path:
        path = path.split('/')
        session.cwd(path[0])
        file = open('C:\\Users\\Maanav\\Downloads\\' + path[1], 'wb')
        session.retrbinary("RETR " + path[1], file.write)
    else:
        file = open('C:\\Users\\Maanav\\Downloads\\' + path, 'wb')
        session.retrbinary("RETR " + path, file.write)


root = Tk()
uptext = StringVar()
dowtext = StringVar()
root.geometry("600x600")
# toolbar
mymenu = Menu(root)
mymenu.add_command(label="Exit", command=root.quit)
mymenu.add_command(label="About", command=AboutApp)
root.config(menu=mymenu)
# upload
Label(root, text="Upload File", font=(None, 15)).grid(row=1, column=1, pady=10)
e1 = Entry(root, textvariable=uptext).grid(row=1, column=2)
Button(text="Browse", command=lambda: OpenFile(uptext)).grid(row=1, column=3, padx=10)
Button(text='upload', command=lambda: Upload(uptext.get())).grid(row=2, column=2)
# download
Label(root, text="\n").grid(row=3)
Label(root, text="Download File", font=(None, 15)).grid(row=4, column=1)
e2 = Entry(root, textvariable=dowtext).grid(row=4, column=2)
b1 = Button(text='Download', command=lambda: Download(dowtext.get())).grid(row=5, column=2)
Label(root, text='\n').grid(row=6)
ViewFiles()
root.grid_columnconfigure(0, minsize=10)
mainloop()
