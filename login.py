from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path='../chromedriver/chromedriver.exe')
driver.implicitly_wait(10)
driver.maximize_window()

driver.get('https://www.demoblaze.com')

login_button = driver.find_element_by_id('login2')
login_button.click()

driver.find_element_by_id('loginusername').send_keys('squishy2512')
driver.find_element_by_id('loginpassword').send_keys('password123')

time.sleep(5)

elementXpath = driver.find_element_by_xpath('//*[@id="logInModal"]/div/div/div[3]/button[2]').click()

time.sleep(7)

driver.close()
driver.quit()
print("Test Completed")

