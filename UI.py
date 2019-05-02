from tkinter import *
from PIL import Image,ImageTk
import os, json


root = Tk()
root.title('VRBUST Motion sensor')
root.geometry('200x400')
root.configure(background='black')

##Logo
src_img_logo = Image.open("VR.png")
src_img_logo = src_img_logo.resize((120, 50))
img_logo = ImageTk.PhotoImage(src_img_logo)
panel_logo = Label(root, image = img_logo)
panel_logo.pack(side = "top", fill = "both")

## Functions
def activate(): # Activate softwear button
    f = json.load(open('settings.json'))
    f['active'] = True
    json.dump(f, open('settings.json', 'w'))
def deactivate():
    f = json.load(open('settings.json'))
    f['active'] = False
    json.dump(f, open('settings.json', 'w'))
def cameraon():
    f = json.load(open('settings.json'))
    f['camera-on'] = True
    json.dump(f, open('settings.json', 'w'))

def cameraoff():
    f = json.load(open('settings.json'))
    f['camera-on'] = False
    json.dump(f, open('settings.json', 'w'))

def showmask():
    f = json.load(open('settings.json'))
    f['mask'] = True
    json.dump(f, open('settings.json', 'w'))

def hidemask():
    f = json.load(open('settings.json'))
    f['mask'] = False
    json.dump(f, open('settings.json', 'w'))
def autodetectbackground():
    f = json.load(open('settings.json'))
    f['auto'] = True
    json.dump(f, open('settings.json', 'w'))

##Text

##buttons

detectionOn = Button (root, text = "Activate", command=activate, height = 1, width = 15, bg="orange", fg="black")
detectionOn.place(x=40, y=100) 


detectionOff = Button (root, text = "Deactivate", command=deactivate, height = 1, width = 15, bg="orange", fg="black")
detectionOff.place(x=40, y=130)

cameraOff = Button (root, text ="Camera ON", command = cameraon, height = 1, width = 15, bg="orange", fg="black")
cameraOff.place(x=40, y=190)

cameraOn = Button (root, text ="Camera OFF", command=cameraoff, height = 1, width = 15, bg="orange", fg="black")
cameraOn.place(x=40, y=220)

showMask = Button (root, text ="Show MASK", command = showmask, height = 1, width = 15, bg="orange", fg="black")
showMask.place(x=40, y=280)

hideMask = Button (root, text ="Hide MASK", command=hidemask, height = 1, width = 15, bg="orange", fg="black")
hideMask.place(x=40, y=310)

hideMask = Button (root, text ="Auto detect background", command=autodetectbackground, height = 1, width = 20, bg="orange", fg="black")
hideMask.place(x=25, y=370)


e1 = Entry(root)


e1.place(x=40, y=340, height = 20, width = 114)








root.mainloop()



