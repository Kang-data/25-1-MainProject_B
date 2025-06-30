from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("https://www.epeople.go.kr/nep/pttn/gnrlPttn/pttnSmlrCaseList.npaid")
time.sleep(3)

input("날짜를 변경 완료 시 ENTER:")

results = []

for i in range(1, 20):
    try:
        idx=i%10
        if idx==0:
            idx=10
        title_element = driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({idx}) td:nth-child(2) a")
        title_text = title_element.text
        print(title_text)
        title_element.click()
        time.sleep(2)
        try:
            content_elem = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#txt > div.same_mwWrap > div.samBox.mw > div > div.samC_c")))
            content_text = content_elem.text.strip()
        except:
            content_text = ""
        print(content_text)

        results.append({
            "제목": title_text,
            "본문": content_text
        })

        close_button = driver.find_element(By.CSS_SELECTOR, "#txt > div.same_mwWrap > div.btnArea.right > button")
        close_button.click()
        time.sleep(1)

    except Exception as e:
        print(f"Error on item {i}: {e}")
        continue

    if i%10==0:
        next_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#frm > div.page_list > span.nep_p_next > a")))
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2)

driver.quit()

df = pd.DataFrame(results)
df.to_csv("epeople_complaints.csv", index=False)
print(df.head())
