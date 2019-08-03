# keywords = input("enter the input txt file")
import re
import pandas as pd
import time
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-setuid-sandbox")
from selenium.webdriver import Chrome

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
url = "https://www.youtube.com/results?search_query={}&sp=EgIIAg%253D%253D"
prefix = {'K':'e3','M':'e6','B':'e9'}
from datetime import datetime

class Browser:
    index=0
    def __init__(self):
        try:
            with open('done.pickle','rb') as token:
                self.done = pickle.load(token)
        except:
            self.done = []
        try:
            self.data = pd.read_csv('data.csv').to_values.to_list()
        except: self.data = []
        self.driver = driverGetter()
        self.driver.get("https://youtube.com")

    def get_result_of_keyword(self,keyword):
        query = url.format(quote(keyword))
        self.driver.get(query)
        time.sleep(2)
        filterBtn = self.driver.find_element_by_xpath('//*[contains(text(),"Filter")]')
        self.get_results(keyword)

    def get_results(self,keyword,current_url=None):
        while 1:
            try:
                self.driver.find_element_by_xpath('//*[contains(text(),"No more results")]')
                break
            except:
                self.driver.execute_script('window.scrollBy(0,3000);')
                time.sleep(2)
            save(self.driver)
            results = self.driver.find_elements_by_tag_name('ytd-video-renderer')
            for i in results:
                j = self.get_info_of_one(i,keyword)
                if j:
                    
                    pd.DataFrame(self.data).to_csv('data.csv',index=False)
                    save(self.driver)
                    self.data.append(j)

    def get_info_of_one(self,driver:Chrome,keyword):
        try:
            length = driver.find_element_by_xpath('.//span[contains(@aria-label,"minutes")]').get_attribute('aria-label').split(' ')[0]
            if int(length) > 10:
                return False
        except: length=0
        title = driver.find_element_by_id('title-wrapper').text
        el = driver.find_element_by_xpath('.//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]')
        link = el.get_attribute('href')
        if link in self.done:
            return False
        print(len(self.done))
        self.done.append(link)
        with open('done.pickle','wb') as token:
            pickle.dump(self.done,token)
        user_name = el.text
        views = driver.find_element_by_xpath('.//span[@class="style-scope ytd-video-meta-block"]').text.split(' ')[0]
        try:
            views = int(views)
        except:
            return False
        driver = driverGetter()
        try:
            print('done')
            email = self.check_email(link,driver)
            
        except:
            email = ''
        subscriber = driver.find_element_by_id('subscriber-count').text.split(' ')[0]
        driver.close()
        return ((keyword,title,user_name,link,email,subscriber))

    def check_email(self,link,driver):

        driver.get(link+'/about')
        description = self.driver.find_element_by_id("description-container").text
        match = re.search(r'[\w\.-]+@[\w\.-]+', description).group()

        return match


    def __del__(self):

        del self.driver

def driverGetter():
    driver = Chrome(options=chrome_options)
    driver.set_window_size(1300,700)
    return driver

if __name__=="__main__":
    print("testing")
    self = Browser()
    lines = ['fitness','vegan']
    while 1:
        #lines = open(keywords,'r').readlines()
        for line in lines:
            self.get_result_of_keyword(line)
