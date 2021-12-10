'''
Created on 02-Oct-2020

@author: somsh
'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pytesseract as tess
import pdf2image 
from PIL import Image,ImageEnhance,ImageFilter

pages=pdf2image.convert_from_path('D:\Software\eclipse\jee-2019-12\eclipse-workspace\pdf_word_convert\pdf_word_convert\pp5.pdf',1000)
for page in pages:
    page.save('pp5.jpg','JPEG')
 
im=Image.open("pp5.jpg")
im=im.convert('RGB')
# im=im.filter(ImageFilter.MedianFilter())
# enhancer=ImageEnhance.Contrast(im)
# im=enhancer.enhance(2)
# im=im.convert('1')
im.save("enh_pp5.jpg")

tess.pytesseract.tesseract_cmd='D:/Software/Tesseract-OCR/tesseract.exe'
print(tess.get_tesseract_version())
text=tess.pytesseract.image_to_string('enh_pp5.jpg',lang='ben')
f=open('pp5.txt','w',encoding="utf-8")
f.write(text)
f.close()