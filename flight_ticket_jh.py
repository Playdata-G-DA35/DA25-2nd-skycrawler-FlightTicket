from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

"""
    1. URL ==> 페이지 번호
    2. 조회할 항목 => SELECTOR
    3. 저장방식 (CSV)

"""

# 날짜 선택하는 함수 정의
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


service=Service(executalbe_path=ChromeDriverManager().install())
browser=webdriver.Chrome(service=service, options=chrome_options)


# 네이버 항공권으로 이동
browser.get('https://flight.naver.com')

browser.maximize_window()
time.sleep(3)


start_area=input("어디서 갈거야:")
end_area=input("어디로 갈건데:")
start_date=input("출발 날짜를 YYYY/mm/dd로 입력해:")
end_date=input("도착 날짜를 YYYY/mm/dd로 입력해:")



# 출발, 도착 날짜를 / 기준으로 나누고 0000.00. 형식으로 다시 저장
start_list = []
start_list = start_date.split("/")
start_month = start_list[0] + "." + start_list[1] + "."
start_day = start_list[2]

end_list = []
end_list = end_date.split("/")
end_month = end_list[0] + "." + end_list[1] + "."
end_day = end_list[2]




# 버튼 찾기
start_area_button = browser.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[4]/div/div/div[2]/div[1]/button[1]')
end_area_button = browser.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[4]/div/div/div[2]/div[1]/button[2]')


# 출발지 선택
start_area_button.click()                        
time.sleep(1)

search_area = browser.find_element(By.CLASS_NAME, 'autocomplete_input__1vVkF')
search_area.send_keys(start_area)
time.sleep(1)

finish_area = browser.find_element(By.CLASS_NAME, 'autocomplete_inner__3Owyw')
finish_area.click()
time.sleep(1)

# 도착지 선택
end_area_button.click()
time.sleep(1)

search_area = browser.find_element(By.CLASS_NAME, 'autocomplete_input__1vVkF')
search_area.send_keys(end_area)
time.sleep(1)

finish_area = browser.find_element(By.CLASS_NAME, 'autocomplete_inner__3Owyw')
finish_area.click()
time.sleep(1)


# 출발, 도착 날짜 버튼 찾기
start_area_date = browser.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[4]/div/div/div[2]/div[2]/button[1]')
end_area_date = browser.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[4]/div/div/div[2]/div[2]/button[2]')

# 출발 날짜 버튼 선택
start_area_date.click()
time.sleep(1)

# 출발 날짜
select_day(start_month, start_day)
time.sleep(1)

# 도착 날짜 버튼 선택
end_area_date.click()
time.sleep(2)

# 도착 날짜
select_day(end_month, end_day)
time.sleep(2)

# 항공권 검색버튼 선택
search = browser.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[4]/div/div/div[2]/button')
search.click()
browser.implicitly_wait(15)


cur_url = browser.current_url
browser.get(cur_url)

# 페이지 로딩 대기 (필요에 따라 시간 조정)
browser.implicitly_wait(10)  # 10초 동안 대기

# 페이지의 HTML 소스 가져오기
html = browser.current_url

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html, 'lxml')

# 텍스트 추출 및 출력
text = soup.get_text()
print(text)