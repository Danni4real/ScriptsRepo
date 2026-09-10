import os
import time
import ddddocr
import pymouse
import requests
import pyautogui
import pyperclip
import contextlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from pynput.keyboard import Key, Controller as kCtr

def download_captcha_pic():
    x, y, width, height = 800, 664, 108, 28
    img = pyautogui.screenshot(region=(x, y, width, height))
    img.save('captcha.jpg')

def get_captcha_pic_content():
    download_captcha_pic()
    ocr = ddddocr.DdddOcr()
    image = open('captcha.jpg', 'rb').read()
    result = ocr.classification(image)
    return result

def login(driver):
    driver.get("http://39.108.56.240/biz/user-login-L2Jpei9lZmZvcnQtY2FsZW5kYXIuaHRtbA==.html")
    time.sleep(1)# 等待页面加载

    driver.find_element(By.NAME, "account").send_keys("nidan") 
    driver.find_element(By.NAME, "password").send_keys("N1dan@hangsheng")
    driver.find_element(By.NAME, "captcha").send_keys(get_captcha_pic_content())
    
    time.sleep(2)# 等待登录完成
    driver.find_element(By.XPATH, "//button[@type='submit']").click()  # 替换为登录按钮的 XPath
        
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for alert ' +
                                   'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
        print("login failed!")
        driver.quit()
        return False
    except TimeoutException:
        print("login ok!")
        return True

def copy_logs():
    keyboard = kCtr()
    # 抓取页面内容
    m = pymouse.PyMouse()
    m.press(192,307) #mouse button press
    m.move(973,1027)
    time.sleep(1)
    m.release(973,1027) #mouse button release
    
    with keyboard.pressed(Key.ctrl):
        keyboard.press('c')
        time.sleep(1)
        keyboard.release('c')

def extract_log_from_web():
    while True:
        driver = webdriver.Chrome(service=Service(executable_path="/usr/bin/chromedriver"))
        if login(driver) == True:
            driver.get("http://39.108.56.240/biz/effort-calendar.html") # 替换为目标页面的URL
            time.sleep(2)
            copy_logs()
            driver.quit()
            break

    return pyperclip.paste()
