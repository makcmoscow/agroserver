from selenium import webdriver
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException as NoElement
from selenium.common.exceptions import \
    StaleElementReferenceException as NoElement2
from selenium.common.exceptions import ElementNotVisibleException as NotVisible

PATH = 'D:\python\агросервер.ру\\'
done_files = []

class Parser:
    def __init__(self, category):
        opt = webdriver.ChromeOptions()
        # opt.add_extension("D:\disable_img_chrome\Block-image_v1.1.crx")
        # opt.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=opt)
        self.dir_links = []
        self.category = category.replace('\n', '')



    def get_subdir(self):
        self.driver.get(self.category)
        time.sleep(5)
        if len(self.driver.find_elements_by_class_name('notfound'))>0:
            print('Нас забанили')
            time.sleep(60000)
        try:
            lis = self.driver.find_element_by_class_name('b_list_nav')
            lis = lis.find_elements_by_tag_name('li')
            for li in lis:
                self.dir_links.append(li.find_element_by_tag_name('a').get_attribute('href'))
            with open(PATH+self.category.split('/')[-2]+'.txt', 'w') as file:
                for subcat in self.dir_links:
                    file.write(subcat+'\n')
        except NoElement:
            pass
    def parser_quit(self):
        time.sleep(5)
        self.driver.quit()

def worker():

    for cat_file in os.listdir(PATH):
        if cat_file not in done_files:
            if cat_file.endswith('.txt'):
                with open(PATH+cat_file, 'r') as file:
                    for line in file.readlines():
                        parser = Parser(line)
                        parser.get_subdir()
                        parser.parser_quit()
                done_files.append(cat_file)
                try:
                    os.rename(PATH+cat_file, PATH+'done\\'+cat_file)
                    print('file ', cat_file, 'was moved to "done"')
                except Exception as e:
                    print('58 ', e)
                worker()
        else:
            pass
worker()



