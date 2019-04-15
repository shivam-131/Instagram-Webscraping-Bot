from selenium import webdriver
import os
from time import sleep
import pyautogui
from bs4 import BeautifulSoup
import requests
import shutil
import xlwt
from xlwt import Workbook

class App:
    def __init__(self,username='webscraper7', password='shivam131' , target_username='danceclubiitk' , path="C:\\Users\\Shivam\\Desktop\\instaphotos"):
        self.username=username
        self.password=password
        self.target_username= target_username
        self.path= path
        self.driver= webdriver.Chrome()
        self.error=False
        self.main_url='https://www.instagram.com'
        self.driver.get(self.main_url)
        self.driver.maximize_window()
        sleep(3)
        self.log_in()
        sleep(5)
        self.remove_window()
        sleep(5)
        if self.error is False:
            self.close_dialog_box()
            self.search_profile()    
            self.click_on_target()
        posts= self.no_of_posts()
        if self.error is False:
            self.scroll_down(posts)
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
        self.downloading_images()          
        print("stop for now")
        sleep(3)
        self.driver.close()
    def downloading_images(self):
        soup= BeautifulSoup(self.driver.page_source, 'html.parser')
        all_images = soup.find_all('img')
        self.downloading_captions(all_images)
        print('length of all images', len(all_images))
        for index,image in enumerate(all_images):
           filename = 'image_' + str(index) + '.jpg'
           image_path = os.path.join(self.path,filename)
           link = image['src']
           print("Downloading image", index)
           response = requests.get(link, stream=True)
           try:
               with open(image_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file )
           except Exception:
               print(Exception)
               print('Could not download image number', index)
               print('Image link -->', link)
               print(image['src'])    
    
    def downloading_captions(self, images):
        captions_folder_path = os.path.join(self.path, 'captions')
        if not os.path.exists(captions_folder_path):
            os.mkdir(captions_folder_path)
        self.writing_cap_to_excel(images, captions_folder_path)    
        for index,image in enumerate(images):
            try:
                caption = image['alt']
            except KeyError:
                caption= 'No caption exists'    
            file_name = 'caption_' + str(index) + '.txt' 
            file_path = os.path.join(captions_folder_path,file_name)
            link = image['src']
            with open(file_path, 'wb') as file:
                file.write(str('link:' + str(link) + '\n' + '       '+ 'captions:' + caption).encode())

    def writing_cap_to_excel(self, images, caption_path):
        workbook = Workbook(caption_path + 'captions.xlsx')
        worksheet = workbook.add_sheet('SHEET 1')
        row=0
        worksheet.write(row,0,'Image name')
        worksheet.write(row,1, 'Caption')
        row=row+1
        for index,image in enumerate(images):
            filename = 'image_' + str(index) + '.jpg'
            try:
                caption = image['alt']
            except KeyError:
                caption= 'No caption exists'
            worksheet.write(row, 0, filename)
            worksheet.write(row, 1, caption)
            row+=1
        workbook.save('INSTABOT.xls')                
    def log_in(self):
        try:
            log_in_button= self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')
            log_in_button.click()
            sleep(5)
            try:
                username_x=792
                username_y=333
                password_x=792
                password_y=386
                button_x=952
                button_y=451
                pyautogui.click(username_x,username_y)
                pyautogui.typewrite(self.username,interval=0.25)
                pyautogui.click(password_x,password_y)
                pyautogui.typewrite(self.password,interval=0.25)
                pyautogui.click(button_x,button_y)
                sleep(3)
            except Exception:
                print("Some exception occured while trying to find username or password field") 
                self.error= True   
        except Exception:
            self.error=True
            print("Unable to find login button")
    def remove_window(self):
        not_now_x=946
        not_now_y=718
        pyautogui.click(not_now_x,not_now_y)

    def close_dialog_box(self):
        try:
            dialog_x=949
            dialog_y=765
            pyautogui.click(dialog_x,dialog_y)
            sleep(1)
        except Exception:
            pass
    def search_profile(self):
        try:
            searchbar_x=832
            searchbar_y=177
            pyautogui.click(searchbar_x,searchbar_y)
            pyautogui.typewrite(self.target_username,interval=0.25)
            pyautogui.press('enter')
            sleep(3)
        except Exception:
            self.error= True
            print('Could not find search bar')        
    def click_on_target(self):
        try:
            pyautogui.press('down')
            pyautogui.press('enter')
            sleep(1)
        except Exception:
            self.error= True
            print("Could not click on target's profile")
    def no_of_posts(self):
        posts=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span')
        posts=str(posts.text).replace(',','')
        posts=int(posts)
        print(posts)
        return posts
    def scroll_down(self,posts):
        try:
            self.no_of_posts=posts
            if self.no_of_posts>12:
                no_of_scrolls = int(self.no_of_posts/12) + 3
                for value in range(no_of_scrolls):
                    try:
                        print(value)
                        self.driver.execute_script('window.scrollTo(0 , document.body.scrollHeight);')
                        sleep(1)
                    except Exception:
                        self.error= True
                        print('Some error occured while trying to scroll down.')    
        except Exception:
            self.error= True
            print('Could not find no. of posts while trying to scroll down')            

if __name__ == '__main__':
    print("Please enter the target's username")
    target_username=input()
    app= App('webscraper7','shivam131',target_username)
