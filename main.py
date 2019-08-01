import re
import time
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

    def __init__(self):
        self.data = []
        self.driver = driverGetter()
        self.driver.get("https://youtube.com")

    def get_result_of_keyword(self,keyword):
        query = url.format(quote(keyword))
        self.driver.get(query)
        time.sleep(2)
        filterBtn = self.driver.find_element_by_xpath('//*[contains(text(),"Filter")]')
        self.get_results()

    def get_results(self,current_url=None):
        while 1:
            try:
                self.driver.find_element_by_xpath('//*[contains(text(),"No more results")]')
                break
            except:
                self.driver.execute_script('window.scrollBy(0,3000);')
                time.sleep(2)
        results = self.driver.find_elements_by_tag_name('ytd-video-renderer')
        for i in results:
            j = self.get_info_of_one(i)
            if j:
                print(j)
                self.data.append(j)
                pd.DataFrame(j).to_csv('test.csv',index=False)

    def get_info_of_one(self,driver:Chrome):
        title = driver.find_element_by_id('title-wrapper').text
        el = driver.find_element_by_xpath('.//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]')
        link = el.get_attribute('href')
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
            print('done')
        except:
            email = ''
        driver.close()
        return ((datetime.now(),title,link,user_name,views,email))

    def check_email(self,link,driver):

        driver.get(link+'/about')
        description = self.driver.find_element_by_id("description-container").text
        match = re.search(r'[\w\.-]+@[\w\.-]+', description).group()

        return match


    def __del__(self):

        del self.driver

def driverGetter():
    driver = Chrome(chrome_options=chrome_options)
    return driver

if __name__=="__main__":
    print("testing")
    self = Browser()
    self.get_result_of_keyword("roof")
