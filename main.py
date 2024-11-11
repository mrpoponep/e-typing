from selenium import webdriver
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

import pyautogui
import pykakasi
import keyboard
import time

chrome_driver_path = "C:/code/chromedriver-win64"
service = Service()
kks = pykakasi.kakasi()
driver = webdriver.Chrome(service=service)
WAIT = WebDriverWait(driver, 5)

def typing_kana():
    wait = WebDriverWait(driver, 10)
    while True:
        sentence_text_element = wait.until(EC.presence_of_element_located((By.ID, "kanaText")))
        text_content = sentence_text_element.text
        result = kks.convert(text_content)
        if result:
            print(result[0]["hepburn"])
        for i in result[0]["hepburn"]:
            pyautogui.press(i)
            if keyboard.is_pressed('space'):
                print("Break key pressed. Exiting...")
                exit()

def typing_romaji():
    wait = WebDriverWait(driver, 10)
    while True:
        sentence_text_element = wait.until(EC.presence_of_element_located((By.ID, "sentenceText")))
        text_content = sentence_text_element.text
        print(text_content)
        for i in text_content:
            pyautogui.press(i)
            time.sleep(0.1)
            if keyboard.is_pressed('space'):
                print("Break key pressed. Exiting...")
                exit()

if __name__ == "__main__":
    driver.maximize_window()
    driver.get('https://www.e-typing.ne.jp/roma/check/')

    email = "abc@gmail.com" 
    password = "123456" 

    email_field = driver.find_element(By.ID, "mail")
    email_field.send_keys(email)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    login_button = driver.find_element(By.ID, "login_btn")
    login_button.click()
    time.sleep(5)

    check_button = driver.find_element(By.CSS_SELECTOR, "#level_check_member a")
    check_button.click()

    script = """
    const element = document.getElementById('sentenceText');
    element.style.fontSize = '16px'; // Thay đổi kích thước chữ
    """

    driver.implicitly_wait(5)
    
    new_element = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, "pp_pic_holder"))) 
    pp_full_res_element = WAIT.until(EC.presence_of_element_located((By.ID, "pp_full_res"))) 

    iframe_element = pp_full_res_element.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe_element)

    start_btn = driver.find_element(By.ID, 'start_btn')
    start_btn.click()

    while True:
        if keyboard.is_pressed('space'):
            print("start")
            time.sleep(3.5)
            # typing_kana()
            typing_romaji()
            break

    input("Press Enter to close...")
    driver.quit()