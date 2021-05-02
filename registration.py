from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path='../chromedriver/chromedriver.exe')
driver.implicitly_wait(10)
driver.maximize_window()

driver.get('https://www.demoblaze.com')

regris_button = driver.find_element_by_id('signin2')
regris_button.click()

driver.find_element_by_id('sign-username').send_keys('squishy2512')
driver.find_element_by_id('sign-password').send_keys('password123')

elementXpath = driver.find_element_by_xpath('//*[@id="signInModal"]/div/div/div[3]/button[2]').click()

time.sleep(7)

driver.switch_to_alert().accept()

driver.close()
driver.quit()
print("Test Completed")

