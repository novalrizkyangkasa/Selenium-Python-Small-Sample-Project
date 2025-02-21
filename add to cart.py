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

time.sleep(5)

object = driver.find_element_by_xpath('//*[@id="tbodyid"]/div[1]/div/a/img')
driver.execute_script('arguments[0].scrollIntoView();',object)

elementXpath = driver.find_element_by_xpath('//*[@id="tbodyid"]/div[1]/div/a/img').click()
time.sleep(3)
elementXpath = driver.find_element_by_xpath('//*[@id="tbodyid"]/div[2]/div/a').click()
time.sleep(3)
driver.switch_to_alert().accept()

driver.find_element_by_id('cartur').click()
time.sleep(2)

elementXpath = driver.find_element_by_xpath('//*[@id="page-wrapper"]/div/div[2]/button').click()
time.sleep(2)
driver.find_element_by_id('name').send_keys('Noval Rizky')
time.sleep(2)
driver.find_element_by_id('country').send_keys('Indonesia')
time.sleep(2)
driver.find_element_by_id('city').send_keys('Mojokerto')
time.sleep(2)
driver.find_element_by_id('card').send_keys('91902100001234')
time.sleep(2)
driver.find_element_by_id('month').send_keys('Juni')
time.sleep(2)
driver.find_element_by_id('year').send_keys('1996')
time.sleep(2)
elementXpath = driver.find_element_by_xpath('//*[@id="orderModal"]/div/div/div[3]/button[2]').click()
time.sleep(3)
elementXpath = driver.find_element_by_xpath('/html/body/div[10]/div[7]/div/button').click()

time.sleep(3)

driver.find_element_by_id('logout2').click()

time.sleep(2)

driver.close()
driver.quit()
print("Test Completed")
