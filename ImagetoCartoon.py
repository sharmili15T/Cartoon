import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import cv2 
import imageio 
import numpy as np 
import matplotlib.pyplot as plt


tp=tk.Tk()
tp.geometry('400x400')
tp.title('Covert your image to a cartoon')
tp.configure(background='white')
label=Label(tp,background='#AAABCD', font=('arial',20,'bold'))

def upload():
    ImagePath=filedialog.fileopenbox() ##to get the image from the path
    convert_Image(ImagePath)

def convert_Image(ImagePath):
    # read the image
    rawImage = cv2.imread(ImagePath)
    rawImage = cv2.cvtColor(rawImage, cv2.COLOR_BGR2RGB)
    #print(image)  # image is stored in form of numbers

    # Check if the image is present
    if rawImage is None:
        print("Upload Image")
        tp.quit()

    ReSized1 = cv2.resize(rawImage, (960, 540)) ## Resize image to appropriate size
    #plt.imshow(ReSized1, cmap='gray')


    #converting an image to grayscale
    grayScaleConvertedImage= cv2.cvtColor(rawImage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleConvertedImage, (960, 540))
    #plt.imshow(ReSized2, cmap='gray')


    #smoothing out the images
    getEdge = cv2.adaptiveThreshold(grayScaleConvertedImage, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized3 = cv2.resize(getEdge, (960, 540))
    #plt.imshow(ReSized3, cmap='gray')

    #applying bilateral filter to remove noise 
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(rawImage, 9, 300, 300)
    ReSized4 = cv2.resize(colorImage, (960, 540))
    #plt.imshow(ReSized4, cmap='gray')


    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized5 = cv2.resize(cartoonImage, (960, 540))
    #plt.imshow(ReSized5, cmap='gray')

    # Plotting the whole transition
    images=[ReSized1, ReSized2,  ReSized3, ReSized4, ReSized5]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    imgName="cartoonImage"
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(ImagePath, imgName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized5, cv2.COLOR_RGB2BGR))
    out_message = "Cartoon Image is saved at:"+ path 
    tk.messagebox.showinfo(title=None, message=out_message)

upload=Button(tp,text="Convert Image to Cartoon",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=tp,pady=50)

tp.mainloop()



