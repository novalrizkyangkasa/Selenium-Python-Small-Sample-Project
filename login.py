from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

time.sleep(2)

elementXpath = driver.find_element(By.XPATH, '//*[@id="logInModal"]/div/div/div[3]/button[2]').click()

time.sleep(3)

driver.close()
driver.quit()
print("Test Completed")

