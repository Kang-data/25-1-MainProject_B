from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()

urls = [
    "https://www.yc.go.kr/portal/contents.do?mId=0409020000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409010000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409030000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409360000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409040000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409050000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409060000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409070000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409080000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409110000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409120000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409130000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409160000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409170000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409180000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409140000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409150000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409090000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409100000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409330000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409200000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409190000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409370000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409220000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409210000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409230000",
    "https://www.yc.go.kr/portal/contents.do?mId=0409320000"
]

results = []

for i in range(len(urls)):
    driver.get(urls[i])
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dept = driver.find_element(By.CSS_SELECTOR, f"#container > div > section.snb_wrap > nav > ul > li:nth-child(7) > ul > li:nth-child({str(i+1)}) > a").text.strip()
    print(dept)
    headers = soup.select("#conts h4")
    work=soup.select("#conts > div")
    for header in range(len(headers)):
        who = headers[header].get_text(strip=True)
        works=soup.select(f"#conts > div:nth-child({str(header+1)}) > table > tbody > tr:nth-child(3) > td > ul > li")
        for work in works:
            doing=work.get_text(strip=True)
            print(dept, who, doing)
            results.append({
            "부서": dept,
            "담당": who,
            "업무": doing
            })

driver.quit()

df = pd.DataFrame(results)
df.to_csv("영천시_부서_담당_업무.csv", index=False)
print(df.head())