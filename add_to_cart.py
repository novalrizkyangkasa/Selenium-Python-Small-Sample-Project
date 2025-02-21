from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time

chrome_driver_path= '/Users/noval/Documents/Learn Automation Testing/chromedriver-mac-arm64/chromedriver'

# Membuat Service object untuk ChromeDriver
service = Service(executable_path=chrome_driver_path)

# Membuka Chrome dengan WebDriver
driver = webdriver.Chrome(service=service)

driver.implicitly_wait(10)
driver.maximize_window()

driver.get('https://www.demoblaze.com')

# Tunggu hingga URL mengandung kata 'demoblaze'
wait = WebDriverWait(driver, 10)  # Waktu tunggu maksimum 10 detik
wait.until(EC.url_contains("demoblaze"))

login_button = driver.find_element(By.ID, 'login2')
login_button.click()

driver.find_element(By.ID, 'loginusername').send_keys('squishy251225')
time.sleep(2)
driver.find_element(By.ID, 'loginpassword').send_keys('password123')

time.sleep(5)

elementXpath = driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[2]').click()

time.sleep(5)

object = driver.find_element(By.XPATH, '//*[@id="tbodyid"]/div[1]/div/a/img')
driver.execute_script('arguments[0].scrollIntoView();',object)

elementXpath = driver.find_element(By.XPATH, '//*[@id="tbodyid"]/div[1]/div/a/img').click()
time.sleep(3)
elementXpath = driver.find_element(By.XPATH, '//*[@id="tbodyid"]/div[2]/div/a').click()
time.sleep(3)

# Menangani alert
alert = Alert(driver)  # Membuat objek Alert untuk menangani alert
alert.accept()  # Menerima alert

driver.find_element(By.ID, 'cartur').click()
time.sleep(2)

elementXpath = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/div/div[2]/button').click()
time.sleep(2)
driver.find_element(By.ID, 'name').send_keys('Noval Rizky')
time.sleep(2)
driver.find_element(By.ID, 'country').send_keys('Indonesia')
time.sleep(2)
driver.find_element(By.ID, 'city').send_keys('Mojokerto')
time.sleep(2)
driver.find_element(By.ID, 'card').send_keys('91902100001234')
time.sleep(2)
driver.find_element(By.ID, 'month').send_keys('Juni')
time.sleep(2)
driver.find_element(By.ID, 'year').send_keys('1996')
time.sleep(2)
elementXpath = driver.find_element(By.XPATH, '//*[@id="orderModal"]/div/div/div[3]/button[2]').click()
time.sleep(3)
elementXpath = driver.find_element(By.XPATH, '/html/body/div[10]/div[7]/div/button').click()

time.sleep(3)

driver.find_element(By.ID, 'logout2').click()

time.sleep(2)

driver.close()
driver.quit()
print("Test Completed")
