from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# 初始化Chrome瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 設置全螢幕
driver.maximize_window()

# 打開YouTube登入頁面
print("打開YouTube登入頁面")
driver.get("https://accounts.google.com/signin/v2/identifier?service=youtube")

# 輸入電子郵件
print("輸入電子郵件")
email_field = driver.find_element(By.ID, "identifierId")
email_field.send_keys("sunwayvideo")
email_field.send_keys(Keys.RETURN)

# 等待密碼輸入框出現並輸入密碼
print("等待密碼輸入框出現")
password_field = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.NAME, "Passwd"))
)
print("輸入密碼")
password_field.send_keys("我的密碼(已移除真實密碼)")
password_field.send_keys(Keys.RETURN)

# 跳轉到指定的YouTube網址
print("跳轉到指定的YouTube網址")
driver.get("https://www.youtube.com/?authuser=0")

time.sleep(2)

# 點擊指定的按鈕
print("點擊登入的按鈕")
button = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/tp-yt-app-drawer/div[2]/div/div[2]/div[2]/ytd-guide-renderer/div[1]/ytd-guide-signin-promo-renderer/ytd-button-renderer/yt-button-shape/a/yt-touch-feedback-shape/div/div[2]")
button.click()

time.sleep(2)

# 檢測是否需要再次登入
try:
    print("檢測是否需要再次登入")
    email_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
    print("再次輸入電子郵件")
    email_field.send_keys("sunwayvideo")
    email_field.send_keys(Keys.RETURN)

    password_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "Passwd"))
    )
    print("再次輸入密碼")
    password_field.send_keys("我的密碼(已移除真實密碼)")
    password_field.send_keys(Keys.RETURN)
except:
    print("無需再次登入")

# 跳轉到上傳網址
print("跳轉到上傳網址")
driver.get("https://studio.youtube.com/channel/UClF0KJjYoPhaZqRLJ3xv6aA/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D")

time.sleep(2)

# 找到名稱中不包含"已上傳"的文件
print("查找名稱中不包含'已上傳'的文件")
folder_path = r"C:\Users\User\Desktop\工作\自動化傳影片\影片下載位置"
files_to_upload = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if '已上傳' not in f]

# 上傳文件
if files_to_upload:
    for file_path in files_to_upload:
        print(f"上傳文件: {file_path}")

        try:
            # 模擬文件選擇器選擇文件
            print("模擬文件選擇器選擇文件")
            file_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            file_input.send_keys(file_path)
            time.sleep(5)
            """
            # 點選「這不是為兒童設計」按鈕
            print("點選「這不是為兒童設計」按鈕")
            not_for_kids_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[1]/div[1]"))
            )
            not_for_kids_button.click()

            # 點選下一步
            print("點選下一步")
            next_button_1 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/ytcp-button-shape/button/yt-touch-feedback-shape/div/div[2]"))
            )
            next_button_1.click()

            time.sleep(1)

            # 再次點選下一步
            print("再次點選下一步")
            next_button_2 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/ytcp-button-shape/button/yt-touch-feedback-shape/div/div[2]"))
            )
            next_button_2.click()

            time.sleep(1)

            # 第三次點選下一步
            print("第三次點選下一步")
            next_button_3 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/ytcp-button-shape/button/yt-touch-feedback-shape/div/div[2]"))
            )
            next_button_3.click()

            time.sleep(2)

            # 點選私人影片按鈕
            print("點選私人影片按鈕")
            private_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[1]/div[1]/div[1]"))
            )
            private_button.click()

            # 點選儲存
            print("點選儲存")
            save_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]/ytcp-button-shape/button/yt-touch-feedback-shape/div/div[2]"))
            )
            save_button.click()

            # 等待儲存完成
            time.sleep(10)  # 調整等待時間以確保文件上傳並儲存完成
            """
            # 重命名文件，添加“已上傳”
            new_file_path = os.path.join(folder_path, os.path.basename(file_path).replace('.mp4', ' 已上傳.mp4'))
            os.rename(file_path, new_file_path)
            print(f"重命名文件: {new_file_path}")

        except Exception as e:
            print(f"上傳過程中出錯: {e}")
else:
    print("沒有找到不包含'已上傳'的文件")

print("結束")
# 你可以選擇是否在這裡關閉瀏覽器
# driver.quit()
