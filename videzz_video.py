import time
import os
import random
import requests
import re
import pickle
import subprocess
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import chromedriver_autoinstaller
import undetected_chromedriver as uc
from fake_useragent import UserAgent

# Tự động cài đặt chromedriver tương thích
chromedriver_autoinstaller.install()

# Tạo Chrome options cho macOS
def create_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return options

# Di chuyển chuột ngẫu nhiên
def random_mouse_move(driver):
    try:
        window_width = driver.execute_script("return window.innerWidth;")
        window_height = driver.execute_script("return window.innerHeight;")
        action = ActionChains(driver)
        x_offset = random.randint(-window_width // 2, window_width // 2)
        y_offset = random.randint(-window_height // 2, window_height // 2)
        action.move_by_offset(x_offset, y_offset).perform()
        time.sleep(random.uniform(0.5, 1.5))
    except Exception as e:
        print(f"Error: {e}")
        driver.execute_script("window.scrollBy(0, 250);")
        time.sleep(1)

# Lấy danh sách link từ GitHub
url = "https://raw.githubusercontent.com/talblubClouby96/videzz_video/refs/heads/main/links.txt"
response = requests.get(url)
response.raise_for_status()
link_list = response.text.strip().splitlines()

# Chọn ngẫu nhiên
selected_links = random.sample(link_list, 2)
selected_links += selected_links

print(selected_links)

def run_main_selenium():
    for link in selected_links:
        for i in ["1", "2", "2"]:
            driver = webdriver.Chrome(options=create_chrome_options())
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            driver.get("https://www.dailymotion.com/playlist/x9dd5m")
            time.sleep(random.uniform(5, 10))

            driver.get(link)
            time.sleep(random.uniform(3, 5))
            random_mouse_move(driver)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vplayer")))

            for i in range(5):
                try:
                    play_button_xpath = "//button[@title='Play Video']"
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, play_button_xpath)))
                    play_button = driver.find_element(By.XPATH, play_button_xpath)
                    driver.execute_script("arguments[0].scrollIntoView(true);", play_button)
                    play_button.click()
                    driver.execute_script("""
                        var playButton = document.evaluate("//div[@id='vplayer']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (playButton) {
                            playButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            setTimeout(function() { playButton.click(); }, 500);
                        }
                    """)
                    time.sleep(5)
                    driver.save_screenshot(f"screenshot_{i}.png")
                    random_mouse_move(driver)
                except Exception as e:
                    print(f"Error: {e}")
                    try:
                        driver.execute_script("""
                            var element = document.getElementById('vplayer');
                            var clickEvent = new MouseEvent('click', {
                                bubbles: true,
                                cancelable: true,
                                view: window
                            });
                            element.dispatchEvent(clickEvent);
                        """)
                        try:
                            element = driver.find_element(By.XPATH, play_button_xpath)
                            actions = ActionChains(driver)
                            actions.move_to_element_with_offset(element, 5, 5).click().perform()
                            time.sleep(30)
                            driver.save_screenshot(f"screenshot_error_{i}.png")
                        except Exception as e:
                            print(f"PyAutoGUI click failed: {e}")
                    except Exception as click_error:
                        print(f"Không thể click tọa độ: {click_error}")
            time.sleep(150)
            driver.save_screenshot("screenshot_final.png")

            # Tải video
            download_button_xpath = "//a[@class='btn btn-success btn-lg btn-download btn-download-n']"
            for i in range(5):
                try:
                    download_button = driver.find_element(By.XPATH, download_button_xpath)
                    download_button.click()
                    time.sleep(random.uniform(1, 3))
                    random_mouse_move(driver)
                    driver.save_screenshot(f"screenshot_download_{i}.png")
                except Exception as e:
                    print(f"Download Error: {e}")

            driver.quit()

# Chạy chương trình
run_main_selenium()
