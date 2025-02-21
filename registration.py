from selenium import webdriver
<<<<<<< HEAD
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

=======
import time

driver = webdriver.Chrome(executable_path='../chromedriver/chromedriver.exe')
>>>>>>> 4fd18ae11a6c78c680312ff5e9fd13009349fce8
driver.implicitly_wait(10)
driver.maximize_window()

driver.get('https://www.demoblaze.com')

<<<<<<< HEAD
# Tunggu hingga URL mengandung kata 'demoblaze'
wait = WebDriverWait(driver, 10)  # Waktu tunggu maksimum 10 detik
wait.until(EC.url_contains("demoblaze"))

regris_button = driver.find_element(By.ID, 'signin2')
regris_button.click()

driver.find_element(By.ID, 'sign-username').send_keys('squishy251225')
time.sleep(2)
driver.find_element(By.ID, 'sign-password').send_keys('password123')

elementXpath = driver.find_element(By.XPATH, '//*[@id="signInModal"]/div/div/div[3]/button[2]').click()

time.sleep(3)

# Menangani alert
alert = Alert(driver)  # Membuat objek Alert untuk menangani alert
alert.accept()  # Menerima alert

driver.close()
driver.quit()
print("Test Completed")
=======
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

>>>>>>> 4fd18ae11a6c78c680312ff5e9fd13009349fce8
