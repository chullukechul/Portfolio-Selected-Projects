import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from reader import load_units_from_csv,save_units_to_csv,read_excel
import time

def Automatic_Question_Generator(schedule_ID):

    url = "https://sunway.upad12.com/"
    driver = webdriver.Chrome()
    driver.maximize_window()  # 設定全螢幕
    driver.get(url)
    button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mainNav"]/div/div[2]/ul[2]/li[3]/a')))
    button.click()
    time.sleep(1)

    # 登入
    account_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"account")))
    password_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"password")))

    driver.execute_script("arguments[0].value = arguments[1];", account_field, "T035")
    driver.execute_script("arguments[0].value = arguments[1];", password_field, "1234")

    password_field.send_keys(Keys.RETURN)
    button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="menu_paper"]/a')))
    button.click()
    button2 = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="menu_paper"]/ul/li[1]/a')))
    button2.click()

    target = read_excel(schedule_ID)
    semester_dic = {"112上":'/html/body/div[1]/div[2]/div/form/div[1]/div[1]/div/a[2]',"112下":'/html/body/div[1]/div[2]/div/form/div[1]/div[1]/div/a[1]'}
    grade_dic = {
        "七": '/html/body/div[1]/div[2]/div/form/div[1]/div[2]/div/a[7]',
        "八": '/html/body/div[1]/div[2]/div/form/div[1]/div[2]/div/a[8]',
        "九": '/html/body/div[1]/div[2]/div/form/div[1]/div[2]/div/a[9]'}
    version_dic = {"南一":'/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div/a[1]',"翰林":'/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div/a[2]',"康軒":'/html/body/div[1]/div[2]/div/form/div[1]/div[3]/div/a[3]'}
    suject_dic = {"國文":'/html/body/div[1]/div[2]/div/form/div[1]/div[4]/select/option[2]',
                  "國語":'/html/body/div[1]/div[2]/div/form/div[1]/div[4]/select/option[2]',
                  "數學":'/html/body/div[1]/div[2]/div/form/div[1]/div[4]/select/option[4]',
                  "英語":'/html/body/div[1]/div[2]/div/form/div[1]/div[4]/select/option[3]',
                  "英文":'/html/body/div[1]/div[2]/div/form/div[1]/div[4]/select/option[3]',
                  "自然":'/html/body/div[1]/div[2]/div/form/div[1]/div[4]/select/option[5]'}

    semester = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,semester_dic[target[0]])))
    semester.click()

    grade = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,grade_dic[target[1]])))
    grade.click()

    version = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,version_dic[target[2]])))
    version.click()

    button1 = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'book')))
    button1.click()
    time.sleep(1)
    suject = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, suject_dic[target[3]])))
    suject.click()
    time.sleep(1)

    # 反選所有選項
    checkboxes = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input.sourceCheckbox')))
    for checkbox in checkboxes:
        if checkbox.is_selected():
            checkbox.click()

    # 選定共同選項
    common_options = [] # 你需要選擇的共同選項文本
    target_list = target[4].split(',')
    while target_list:
        common_options.append(target_list.pop())
    for option_text in common_options:
        for checkbox in checkboxes:
            parent_td = checkbox.find_element(By.XPATH, './..')
            parent_tr = parent_td.find_element(By.XPATH, './..')
            text = parent_tr.find_element(By.XPATH, './td[2]').text
            if option_text in text:
                if not checkbox.is_selected():
                    checkbox.click()
                    print(f"Clicked checkbox for: {option_text}")
                else:
                    print(f"Checkbox for {option_text} already selected.")
                break

    time.sleep(2)

    # 處理單元選擇
    units_div_xpath = '//*[@id="unit_div"]'
    units_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, units_div_xpath)))

    # 檢查或創建current_mission.csv文件
    file_path = 'current_mission.csv'
    if not os.path.exists(file_path):
        unit_elements = units_div.find_elements(By.CSS_SELECTOR, 'input.unitCheckbox')
        print(f"Found {len(unit_elements)} units.")
        units = []
        for unit in unit_elements:
            unit_value = unit.get_attribute('value')
            unit_label = unit.find_element(By.XPATH, '..')  # 上級標籤是<label>
            unit_name = unit_label.text.split(">", 1)[-1].strip()  # 獲取<label>的文本
            print(f"Unit value: {unit_value}, Unit name: {unit_name}")
            units.append({"unit": unit_value, "name": unit_name, "status": ""})
        if units:  # 檢查是否抓取到單元信息
            save_units_to_csv(units, file_path)
            print("Units saved to CSV.")
        else:
            print("No units found to save.")

    # 讀取CSV文件，找到尚未完成的單元並將其名稱存儲到變數this_unit_name
    if os.path.exists(file_path):
        units_df = load_units_from_csv(file_path)
        all_finished = True  # 標記是否所有單元都已經完成
        for index, row in units_df.iterrows():
            if row['status'] != 'finish':
                all_finished = False  # 找到尚未完成的單元，標記為 False
                unit_id = str(int(row['unit']))  # 將單元 ID 轉換為整數格式
                unit_checkbox = driver.find_element(By.XPATH, f'//input[@value="{unit_id}"]')
                if not unit_checkbox.is_selected():
                    unit_checkbox.click()
                    this_unit_name = row['name']  # 儲存本次運行的單元名稱
                    print(f"Selected unit: {unit_id} ({this_unit_name})")
                units_df.at[index, 'status'] = 'finish'
                break
        # 保存更新後的CSV文件
        units_df.to_csv(file_path, index=False)
        if all_finished:
            return 1  # 如果所有單元都已經完成，返回 1

    # 點擊下一步按鈕
    next_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[2]/div/form/div[2]/div[3]/div/button')))
    next_button.click()
    time.sleep(1)
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()
        print("Alert accepted.")
    except:
        print("No alert found.")

    # 等待新頁面加載
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'computer')))

    # 填寫 sys_question_count 到 user_question_count
    rows = driver.find_elements(By.CSS_SELECTOR, 'tr.type_row')
    for i, row in enumerate(rows):
        sys_question_count = row.find_element(By.CSS_SELECTOR, f'label[name="sys_question_count[{i}]"]').text
        user_question_input = row.find_element(By.CSS_SELECTOR, f'input[name="user_question_count[{i}]"]')
        user_question_input.clear()
        user_question_input.send_keys(sys_question_count)
        print(f"Set user_question_count[{i}] to {sys_question_count}")

    time.sleep(1)

    # 點擊下一步按鈕
    next_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="computer"]/div[2]/input[4]')))
    next_button.click()
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()
        print("Alert accepted.")
    except:
        print("No alert found.")
    time.sleep(1)
    # 點擊下一步按鈕
    next_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div/form/div[3]/input[3]')))
    next_button.click()
    time.sleep(1)

    # 勾選詳解
    checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="paper_form4"]')))
    checkbox.click()

    input_xpath = '/html/body/div[1]/div[2]/div/div[4]/form/div[2]/div[3]/input'
    paper_name_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, input_xpath)))
    paper_name_input.clear()
    name = this_unit_name + target[4]
    paper_name_input.send_keys(name)

    output_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[2]/div/div[4]/form/div[2]/div[4]/button')))
    output_button.click()

    return 2

