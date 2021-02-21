'''
Created on 02-Nov-2020

@author: somsh
'''
from project.Admin import Admin
from project.User import User

url="https://oldelectoralrolls.wb.gov.in/PDF_LINK/1952/COOCHBEHAR/DINHATA/1952---DINHATA-(1378)-PART-1.pdf"
page_no=12
left_upper_pixel=[216,521]
right_lower_pixel=[551,550]

user=User(url,page_no,left_upper_pixel,right_lower_pixel)
AdminUrl=user.get_url()
AdminPage_no=user.get_page_no()
file_details=user.get_file_details()
tpl=user.crop_image()

admin=Admin(AdminUrl,AdminPage_no,tpl,file_details)
admin.main()