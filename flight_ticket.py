from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date

from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option("detach", True) #꺼짐 방지


service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service,options=options)
url ="https://flight.naver.com"


# 페이지 이동 
browser.get(url)

# 출발지 도착지 버튼
start_button = browser.find_element(By.CSS_SELECTOR,'#__next > div > main > div.main_searchbox__3vrV3 > div > div > div.searchBox_tabpanel__1BSGR > div.tabContent_routes__laamB > button.tabContent_route__1GI8F.select_City__2NOOZ.start')
end_button = browser.find_element(By.CSS_SELECTOR,'#__next > div > main > div.main_searchbox__3vrV3 > div > div > div.searchBox_tabpanel__1BSGR > div.tabContent_routes__laamB > button.tabContent_route__1GI8F.select_City__2NOOZ.end')


# 장소 입력 받기 



# 출발 공항 선택
start_button.click()

dep_search = browser.find_element(By.CLASS_NAME,'autocomplete_input__1vVkF')
dep_search.send_keys(input("출발 공항을 입력하세요:"))
time.sleep(5) # 입력될 때까지 기다리기 
browser.find_element(By.CLASS_NAME,'autocomplete_inner__3Owyw').click()
# browser.find_element(By.CSS_SELECTOR,'#__next > div > main > div.autocomplete_autocomplete__ZEwU_.is_departure > div.autocomplete_content__3RhAZ > section > div > a > div').click()
time.sleep(1)

# 도착 공항 선택
end_button.click()
arr_search = browser.find_element(By.CSS_SELECTOR,' div.autocomplete_header__1NSMD > div > input')
arr_search.send_keys(input("도착 공항을 입력하세요:"))
time.sleep(5) # 입력될 때까지 기다리기 
browser.find_element(By.CLASS_NAME,'autocomplete_search_item__2WRSw').click()

# #날짜 버튼
# start_date_button=browser.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[4]/div/div/div[2]/div[2]/button[1]')
# end_date_button=browser.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[4]/div/div/div[2]/div[2]/button[2]')

# # 출발 날짜 입력
# start_date_button.click()
# y1,m1,d1 = map(int, input("출발 일정을 yyyy.mm.dd 형태로 입력하세요:)").split("."))
# # 상위 요소 - 월별 달력  
# # y_m = browser.find_element(By.CLASS_NAME, 'sc-iqcoie dCaTmH')  
# # calendar= browser.find_element(By.CSS_SELECTOR,'#__next > div > main > div.container_SearchModalContainer__2wVab > div.container_content__2w_MI.container_as_calendar__17CQb > div.calendar_calendar__2OzxE > div.calendar_content__1Xc5a > div > div:nth-child(2) > table')

# # # 각 달의 텍스트를 확인하여 출발 날짜 선택
# for month in calendar.find_elements(By.CLASS_NAME, 'sc-evZas dDVwEk num'):
#     if f"{y1}.{m1}." in month.text:  # yyyy.mm 이 같은 달에서
#         # 해당 월에 대한 일별 버튼 찾기
#         for d in month.find_elements(By.CLASS_NAME, 'sc-evZas dDVwEk num'):  
#             if d.text == str(d1).lstrip("0"):
#                 d.click()
#                 time.sleep(1)
#                 break  # 날짜를 클릭했으므로 루프 종료


# y2, m2, d2 = map(int, input("도착 일정을 연/월/일 형태로 입력하세요)").split("/"))

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

start_date=input("출발 날짜를 YYYY/mm/dd로 입력하세요:")
end_date=input("도착 날짜를 YYYY/mm/dd로 입력하세요:")

# 출발, 도착 날짜를 / 기준으로 나누고 0000.00. 형식으로 다시 저장
start_list = []
start_list = start_date.split("/")
start_month = start_list[0] + "." + start_list[1] + "."
start_day = start_list[2]

end_list = []
end_list = end_date.split("/")
end_month = end_list[0] + "." + end_list[1] + "."
end_day = end_list[2]



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
time.sleep(3)



time.sleep(1000)


# browser.close()
