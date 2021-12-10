'''
Created on 02-Nov-2020

@author: somsh
'''
import pdf2image
import urllib3
import numpy as np
import PIL
import shutil
import matplotlib.pyplot as plt 
import os.path
import pandas

class Admin:
    def __init__(self,url,page_no,tpl,file_details):
        self.__url=url
        self.__page_no=page_no
        self.__tpl=tpl
        self.__file_details=file_details


    def get_url(self):
        return self.__url
    def get_page_no(self):
        return self.__page_no
    def get_tpl(self):
        return self.__tpl
    def get_file_details(self):
        return self.__file_details
    

    def set_url(self, value):
        self.__url = value
    def set_page_no(self, value):
        self.__page_no = value
    def set_tpl(self, value):
        self.__tpl = value
    def set_file_details(self, value):
        self.__file_details = value
        
    
    def __get_pdf(self):
        filename="Admin "+self.get_url()[self.get_url().rfind('/')+1:]
        if not os.path.exists("./"+filename):
            http = urllib3.PoolManager()
            response = http.request('GET', self.get_url(), preload_content=False)
            with open(filename,'wb' ) as file:
                shutil.copyfileobj(response, file)
            file.close() 
            response.release_conn()
        return filename 
    
    def __find_image(self,im, tpl):
        im = np.atleast_3d(im)
        tpl = np.atleast_3d(tpl)
        H, W, D = im.shape[:3]
        h, w = tpl.shape[:2]
        # Integral image and template sum per channel
        sat = im.cumsum(1).cumsum(0)
        tplsum = np.array([tpl[:, :, i].sum() for i in range(D)])
        # Calculate lookup table for all the possible windows
        iA, iB, iC, iD = sat[:-h, :-w], sat[:-h, w:], sat[h:, :-w], sat[h:, w:] 
        lookup = iD - iB - iC + iA
        # Possible matches
        possible_match = np.where(np.logical_and.reduce([lookup[..., i] == tplsum[i] for i in range(D)]))
        # Find exact match
        for y, x in zip(*possible_match):
            if np.all(im[y+1:y+h+1, x+1:x+w+1] == tpl):
                print("MATCH CONFIRMED")
                return (y+1, x+1)
        raise Exception("Image not found")
    
    def __get_image(self,filename,file_details):
        pages=pdf2image.convert_from_path(filename,200,first_page=file_details[-1],last_page=file_details[-1])
        for page in pages:
            page.save('im.jpg','JPEG')
        im=PIL.Image.open("im.jpg")
        return im
    
    def main(self): 
        file_details=self.get_file_details()
        filename=self.__get_pdf()
        im=self.__get_image(filename, file_details)
        tpl=self.get_tpl() 
        im_arr=np.array(im)
        tpl_arr=np.array(tpl)       
        y, x = self.__find_image(im_arr, tpl_arr)
        dictionary={"Year":None,"District":None,"Constituency":None,"Part":None,"Page no.":None}
        for key,i in zip(dictionary.keys(),file_details):
            dictionary[key]=[i]
        df=pandas.DataFrame(dictionary)
        print(df.to_string(index=False))
        f=open("File Details.txt",'w')
        f.write(df.to_string(index=False))
        f.close
        plt.imshow(im)
        plt.show()
        plt.imshow(tpl)
        plt.show()
        fig, ax = plt.subplots()
        plt.imshow(im)
        rect = plt.Rectangle((x, y), tpl_arr.shape[1], tpl_arr.shape[0], edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        plt.show()    

          
    


    