import datetime
import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# read info from properties file
config = configparser.ConfigParser()
config.read("config.ini")

directory_id = config.get("UserInfo", "directory_id")
password = config.get("UserInfo", "password")
uid = config.get("UserInfo", "uid")
duo_passcode = config.get("UserInfo", "duo_passcode")

# initialize chrome options
option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})

# driver
driver = webdriver.Chrome(chrome_options=option, executable_path=r'\chromedriver.exe')

def login():
    # go to imleagues login
    driver.get("https://www.imleagues.com/spa/account/login")
    driver.implicitly_wait(10)

    # enter school name
    driver.find_element_by_xpath('//button[@class="btn dropdown-toggle btn-default"]').click()
    searchbox = driver.find_element_by_xpath('.//div[@class="bs-searchbox"]')
    school_input = searchbox.find_element_by_xpath('.//input[@type="text"]')
    school_input.send_keys('University of Maryland')
    school_input.send_keys(Keys.ENTER)
    driver.implicitly_wait(100)

    # click skip button
    driver.find_element_by_xpath('//*[@id="ssoDirect"]').click()

    # enter CAS credentials
    directory_id_input = driver.find_element_by_xpath('//input[@id="username"]')
    directory_id_input.send_keys(directory_id)
    password_input = driver.find_element_by_xpath('//input[@id="password"]')
    password_input.send_keys(password)
    driver.find_element_by_xpath('//button[@class="form-element form-button"]').click()
    driver.implicitly_wait(100)

    # log into duo
    driver.switch_to.frame('duo_iframe')
    button = driver.find_element_by_xpath('//button[normalize-space(text()) = "Enter a Passcode"]')
    button.click()
    passcode_input = driver.find_element_by_xpath('//input[@name="passcode"]')
    passcode_input.send_keys(duo_passcode)
    button.click()
    driver.implicitly_wait(100)

def get_next_date():
    date = int(str(datetime.date.today())[8:])
    date += 1
    if date < 10:
        return f'0{date}'
    return str(date)

def make_reservation():
    # slow down bitch
    time.sleep(4)

    # go to reservations page
    driver.get('https://www.imleagues.com/spa/fitness/4395e0c781af4905a4088a9561509399/home')
    driver.implicitly_wait(100)

    # click on the right date(the next day)
    driver.find_element_by_xpath(f'//div[contains(text(), {get_next_date()})]').click()
    driver.implicitly_wait(100)

    # find the right row to click
    row_divs = driver.find_elements_by_xpath('//div[@class="event-item bottom-line"]')
    for row in row_divs:
        try:
            location = row.find_element_by_xpath(f'.//div[normalize-space(text()) = "{location}"][@class="event-title"]')
            """
            TODO: Select by time also
            date = location.find_element_by_xpath(f'.//div[normalize-space(text()) = "{time}"][@class="event-text"]')
            """
            row.click()
            break
        except:
            print("not the right one")
    driver.implicitly_wait(100)

    # click sign up button
    driver.find_element_by_xpath(f'//a[normalize-space(text()) = "Sign Up"]').click()
    driver.implicitly_wait(100)

    # enter uid
    uid_input = driver.find_element_by_xpath('//input[@name="txtSID"]')
    uid_input.send_keys(uid)
    driver.implicitly_wait(100)
    driver.find_element_by_xpath('//button[normalize-space(text()) = "Sign Up"]').click()

if __name__ == '__main__':
    login()
    make_reservation()


