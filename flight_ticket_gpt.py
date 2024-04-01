import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# 날짜 선택 함수
def select_day(month, day):
    # 모든 날짜를 가져오기
    all_days = browser.find_elements(By.CLASS_NAME, 'sc-kDDrLX.ctbFvd.month')  # class: 모든 날짜 테이블
    
    # 입력한 월과 일을 찾기 
    for day_group in all_days:
        # 해당 월 찾기 
        months = day_group.find_elements(By.CLASS_NAME, 'sc-iqcoie.dCaTmH')    # class: 0000.00 형식의 월 
        for month_element in months:
            # 월을 찾으면 해당 월의 날짜를 찾기
            if month_element.text == month:
                # 해당 월의 날짜를 가져오기
                days = day_group.find_elements(By.CLASS_NAME, 'sc-evZas.dDVwEk.num')      # class: 모든 날짜
                # 해당 날짜를 찾으면 클릭
                for day_element in days:
                    if day_element.text == day:
                        day_element.click()
                        return

# 항공권 정보를 가져오는 코루틴 함수
async def get_page_info(cur_url, session):
    async with session.get(cur_url) as res:
        if res.status == 200:
            html = await res.text()
            soup = BeautifulSoup(html, 'lxml')
            all_flights = soup.select('.concurrent_ConcurrentItemContainer__2lQVG')
            result_list = []
            for idx, ticket in enumerate(all_flights):
                content_list = [idx, ticket.text]
                result_list.append(content_list)
            return result_list

# 메인 비동기 함수
async def main():
    cur_url = browser.current_url
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    async with aiohttp.ClientSession(headers={"user-agent": user_agent}) as session:
        result = await get_page_info(cur_url, session)
    return result

if __name__ == "__main__":
    # 출발지, 도착지, 출발 날짜, 도착 날짜 입력 받기
    start_area = input("어디서 갈거야:")
    end_area = input("어디로 갈건데:")
    start_date = input("출발 날짜를 YYYY/mm/dd로 입력해:")
    end_date = input("도착 날짜를 YYYY/mm/dd로 입력해:")

    # 출발 날짜와 도착 날짜를 파싱하여 월과 일로 분리
    start_list = start_date.split("/")
    start_month = start_list[0] + "." + start_list[1] + "."
    start_day = start_list[2]

    end_list = end_date.split("/")
    end_month = end_list[0] + "." + end_list[1] + "."
    end_day = end_list[2]

    # Chrome WebDriver 설정
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    service = Service(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.get('https://flight.naver.com')
    browser.maximize_window()

    # 출발지와 도착지 입력
    start_area_button = browser.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[4]/div/div/div[2]/div[1]/button[1]')
    end_area_button = browser.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[4]/div/div/div[2]/div[1]/button[2]')
    start_area_button.click()
    time.sleep(1)
    search_area = browser.find_element(By.CLASS_NAME, 'autocomplete_input__1vVkF')
    search_area.send_keys(start_area)
    time.sleep(1)
    finish_area = browser.find_element(By.CLASS_NAME, 'autocomplete_inner__3Owyw')
    finish_area.click()
    time.sleep(1)
    end_area_button.click()
    time.sleep(1)
    search_area = browser.find_element(By.CLASS_NAME, 'autocomplete_input__1vVkF')
    search_area.send_keys(end_area)
    time.sleep(1)
    finish_area = browser.find_element(By.CLASS_NAME, 'autocomplete_inner__3Owyw')
    finish_area.click()
    time.sleep(1)

    # 출발 날짜와 도착 날짜 선택
    start_area_date = browser.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[4]/div/div/div[2]/div[2]/button[1]')
    end_area_date = browser.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[4]/div/div/div[2]/div[2]/button[2]')
    start_area_date.click()
    time.sleep(1)
    select_day(start_month, start_day)
    time.sleep(1)
    end_area_date.click()
    time.sleep(1)
    select_day(end_month, end_day)
    time.sleep(1)

    # 항공권 검색
    search = browser.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[4]/div/div/div[2]/button')
    search.click()
    browser.implicitly_wait(20)

    # 비동기로 항공권 정보 수집
    result = asyncio.run(main())
    
    # 결과를 데이터프레임으로 변환하여 저장
    df = pd.DataFrame(result)
    os.makedirs('ticket_info', exist_ok=True)
    c_day = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = f"ticket_info/{c_day}.csv"
    df.to_csv(file_path, index=False)
    print(">>>>>>>>완료<<<<<<<<<")
