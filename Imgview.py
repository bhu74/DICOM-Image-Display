# -*- coding: utf-8 -*-
"""
#### Program to display a DICOM image
"""

import numpy as np
from tkinter import *
from tkinter import filedialog
from pydicom import dcmread
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

root = Tk()
root.geometry("800x600")
root.title('DICOM Image Display')

def show():
    s1 = var.get()
    ds = dcmread(s1)
    imgpx = ds.pixel_array
    imgpx = imgpx.astype(float)
    imgpx = imgpx*ds.RescaleSlope + ds.RescaleIntercept
    display_img = apply_ct_window(imgpx, [400,50])
    img_bbox = Image.fromarray((255*display_img).astype('uint8')).resize((250,200))
        
    window1 = Toplevel()
    dspimg = ImageTk.PhotoImage(img_bbox)
    img_lbl = Label(window1, image=dspimg)
    img_lbl.pack()
    window1.mainloop()

def browsefiles():
    filename = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=[("all files","*.*")])
    var.set(filename)
    
def apply_ct_window(img, window):
    # window = (window width, window level)
    R = (img-window[1]+0.5*window[0])/window[0]
    R[R<0] = 0
    R[R>1] = 1
    return R

frame1 = Frame(root)
Label(frame1,text = "DICOM Image Display",font=('Times New Roman',20,'bold')).grid(row=0, column=0, pady=(0,20))
Label(frame1,text = "Enter path to image", font =('Times New Roman', 13)).grid(row=1, column=0, sticky='w')
var=StringVar()
e1 = Entry(frame1,width = 70, textvariable=var).grid(row=2, column=0, sticky='w')
b1 = Button(frame1,text="Browse", command=browsefiles).grid(row=2, column = 1, padx=(30,0), sticky='w')
b2 = Button(frame1,text="Show Image", command=show).grid(row=3, column = 0)
frame1.place(relx=0.5, rely=0.4, anchor='center')

root.mainloop()