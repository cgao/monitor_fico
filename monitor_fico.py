# check fico score

from splinter.browser import Browser
import re
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import pdb
import time
import csv

#=============================================================================
#=============================================================================
class Base:
    checkDate = time.strftime("%x")
    company = 'N/A'
    bureaus = 'N/A'
    score = 'N/A'
    scoreDate = 'N/A'
    previous = 'N/A'
    def __init__(self, username, password, filename):
        self.username = username
        self.password = password
        self.filename = filename

    def writeResult(self):
        result = [  self.checkDate, 
                    self.company, 
                    self.bureaus, 
                    self.score, 
                    self.scoreDate, 
                    self.previous,
                    '\n'
                ]
        with open(self.filename, "a") as myfile:
            wr = csv.writer(myfile, dialect='excel')
            wr.writerow(result)


#=============================================================================
class Amex(Base):
    window_size_x = 1500
    window_size_y = 1500
    url = 'https://www.americanexpress.com/'
    username_id = 'Username'
    password_id = 'Password'
    loginbutton_id = 'loginLink'
    fico_button = 'ah-useful-links-experience-btn'
    score_id = 'cs-score-value'     
    date_id = 'cs-score-text'       
    previous_id = 'cs-score-date'

    def getInfo(self):
        self.company = 'American Express'
        self.bureaus = 'Experian'
        try:
            browser = Browser(driver_name='firefox')
            browser.visit(self.url)
            browser.driver.set_window_size(self.window_size_x, self.window_size_y)
            browser.find_by_id(self.username_id).fill(self.username)
            browser.find_by_id(self.password_id).fill(self.password)
            browser.find_by_id(self.loginbutton_id).click()
            time.sleep(1)
            browser.find_by_id(self.fico_button).click()
            time.sleep(1)
            self.score = browser.find_by_id(self.score_id).text.encode('ascii','ignore')
            self.scoreDate =  browser.find_by_id(self.date_id).text.encode('ascii','ignore')
            self.previous = browser.find_by_id(self.previous_id).text.encode('ascii','ignore')
            browser.quit()
            print(self.company + " succeeds!")
        except:
            print(self.company + " failed!")
            if browser:
                browser.quit()

#=============================================================================
class Barclay(Base):
    window_size_x = 1500
    window_size_y = 1500
    url = 'https://www.barclaycardus.com/servicing/ficoScore'
    username_id = 'username'
    continue_button = 'loginButton-button'
    password_id = 'password'
    loginbutton_id = 'loginButton-button'
    fico_button = 'N/A'
    score_id = 'ficoScore'     
    date_id = 'lastUpdated'       
    previous_id = 'N/A'

    def getInfo(self):
        self.company = 'Barclay'
        self.bureaus = 'TransUnion'
        try:
            browser = Browser(driver_name='firefox')
            browser.visit(self.url)
            browser.driver.set_window_size(self.window_size_x, self.window_size_y)
            browser.find_by_id(self.username_id).fill(self.username)
            browser.find_by_id(self.continue_button).click()
            time.sleep(5)
            browser.find_by_id(self.password_id).fill(self.password)
            browser.find_by_id(self.loginbutton_id).click()
            time.sleep(5)
            digit1 = browser.find_by_id('digit1')['class']
            digit2 = browser.find_by_id('digit2')['class']
            digit3 = browser.find_by_id('digit3')['class']
            self.score = digit1 + digit2 + digit3
            self.score = re.sub("[^0-9]", "", self.score)
            self.scoreDate =  browser.find_by_id(self.date_id).text.encode('ascii','ignore')
            self.scoreDate = "last updated on " + re.sub("[^0-9/]", "", self.scoreDate)
            browser.quit()
            print(self.company + " succeeds!")
        except:
            print(self.company + " failed!")
            if browser:
                browser.quit()
#=============================================================================
class Citi(Base):
    window_size_x = 1500
    window_size_y = 1500
    url = 'https://www.citi.com/credit-cards/citi.action'
    username_id = 'cA-cardsUseridMasked'
    password_name = 'PASSWORD'
    loginbutton_value = 'Sign On'
    fico_button = 'ficoScoreLink'
    score_id = 'cphMainContent_cphMainContent_phbaseredesign_0_pnlCreditScoreDisplayHeader'     
    date_id = 'cphMainContent_cphMainContent_phbaseredesign_0_lblFicoLastDate'       
    previous_id = 'N/A'

    def getInfo(self):
        self.company = 'Citi'
        self.bureaus = 'Equifax'
        try:
            browser = Browser(driver_name='firefox')
            browser.visit(self.url)
            browser.driver.set_window_size(self.window_size_x, self.window_size_y)
            time.sleep(5)
            browser.find_by_id(self.username_id).fill(self.username)
            time.sleep(5)
            browser.find_by_name(self.password_name).fill(self.password)
            time.sleep(5)
            browser.find_by_value(self.loginbutton_value).click()
            time.sleep(10)
            browser.find_by_id(self.fico_button).click()
            time.sleep(10)
            self.score = browser.find_by_id(self.score_id).text.encode('ascii','ignore')
            self.score = re.sub("[^0-9]", "", self.score)
            self.scoreDate =  browser.find_by_id(self.date_id).text.encode('ascii','ignore')
            browser.quit()
            print(self.company + " succeeds!")
        except:
            print(self.company + " failed!")
            pdb.set_trace()
            if browser:
                browser.quit()


#=============================================================================
class Discover(Base):
    window_size_x = 1500
    window_size_y = 1500
    url = 'https://www.discover.com/credit-cards/free-fico-score/'
    username_id = 'login-userId'
    password_id = 'login-password'
    loginbutton_id = 'login-submit'
    fico_button = 'N/A'
    score_class = '.ff-score'     
    date_class = '.fico-score-date'      
    previous_id = 'N/A'

    def getInfo(self):
        self.company = 'Discover'
        self.bureaus = 'TransUnion'
        try:
            browser = Browser(driver_name='firefox')
            browser.visit(self.url)
            browser.driver.set_window_size(self.window_size_x, self.window_size_y)
            browser.find_by_id(self.username_id).fill(self.username)
            browser.find_by_id(self.password_id).fill(self.password)
            browser.find_by_id(self.loginbutton_id).click()
            time.sleep(5)
            self.score = browser.find_by_css(self.score_class).text.encode('ascii','ignore')
            self.score = re.sub("[^0-9]", "", self.score)
            self.scoreDate =  browser.find_by_css(self.date_class).text.encode('ascii','ignore')
            browser.quit()
            print(self.company + " succeeds!")
        except:
            print(self.company + " failed!")
            pdb.set_trace()
            if browser:
                browser.quit()




#=============================================================================
#=============================================================================
# specify:
#       username_Amex, password_Amex
#       username_Barclay, password_Barclay
#       username_Citi, password_Citi 
#       username_Discover, password_Discover 
#       filename

if __name__ == '__main__':
    username_Amex, password_Amex = 'amex_username','amex_password'
    username_Barclay, password_Barclay = 'barclay_username','barclay_password'
    username_Citi, password_Citi = 'citi_username','citi_password'
    username_Discover, password_Discover = 'discover_username','discover_password'
    filename = '/Users/username/monitor_fico/myFICO.csv'


    myAmex = Amex(username_Amex, password_Amex, filename)
    myAmex.getInfo()
    myAmex.writeResult()

    myBarclay = Barclay(barclay_username, barclay_password, filename)
    myBarclay.getInfo()
    myBarclay.writeResult()
    
    myCiti = Citi(citi_username, citi_password, filename)
    myCiti.getInfo()
    myCiti.writeResult()
    
    myDiscover = Discover(discover_username, discover_password, filename)
    myDiscover.getInfo()
    myDiscover.writeResult()

    

