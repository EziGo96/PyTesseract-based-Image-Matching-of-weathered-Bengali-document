'''
Created on 02-Nov-2020

@author: somsh
'''
import pdf2image
import urllib3
import PIL
import shutil
import os.path

class User:
    def __init__(self,url,page_no,left_upper_pixel,right_lower_pixel):
        self.__url=url
        self.__page_no=page_no
        self.__left_upper_pixel=tuple(left_upper_pixel)
        self.__right_lower_pixel=tuple(right_lower_pixel)
        self.__file_details=None

    def get_url(self):
        return self.__url
    def get_page_no(self):
        return self.__page_no
    def get_left_upper_pixel(self):
        return self.__left_upper_pixel
    def get_right_lower_pixel(self):
        return self.__right_lower_pixel
    
    def set_url(self, value):
        self.__url = value
    def set_page_no(self, value):
        self.__page_no = value
    def set_left_upper_pixel(self, value):
        self.__left_upper_pixel = tuple(value)
    def set_right_lower_pixel(self, value):
        self.__right_lower_pixel = tuple(value)
        
    def get_file_details(self):
        self.__file_details=self.get_url().split('/')[4:7]
        if "PART" in self.get_url():
            self.__file_details.append("PART-"+self.get_url()[self.get_url().rfind('.')-1])
        else:
            self.__file_details.append(None)
        self.__file_details.append(self.get_page_no())
        return self.__file_details       

    def __get_pdf(self):
        filename="User "+self.get_url()[self.get_url().rfind('/')+1:]
        if not os.path.exists("./"+filename):
            http = urllib3.PoolManager()
            response = http.request('GET', self.get_url(), preload_content=False)
            with open(filename,'wb' ) as file:
                shutil.copyfileobj(response, file)
            file.close() 
            response.release_conn()
        return filename 

    def __get_image(self):
        filename=self.__get_pdf()
        file_details=self.get_file_details()
        pages=pdf2image.convert_from_path(filename,200,first_page=file_details[-1],last_page=file_details[-1])
        for page in pages:
            page.save('user_im.jpg','JPEG')
        im=PIL.Image.open("user_im.jpg")
        return im 
           
    def crop_image(self):
        im=self.__get_image()     
        pixel_tuple=self.get_left_upper_pixel()+self.get_right_lower_pixel()
        tpl=im.crop(pixel_tuple)
        tpl.save('tpl.jpg','JPEG')
        return tpl
