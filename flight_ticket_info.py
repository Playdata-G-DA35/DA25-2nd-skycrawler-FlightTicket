from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
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
browser.maximize_window() # 화면 최대화


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
time.sleep(1)

# 도착 날짜
select_day(end_month, end_day)
time.sleep(1)

# 항공권 검색버튼 선택
search = browser.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[4]/div/div/div[2]/button')
search.click()
time.sleep(20) # implicitly wait ; 페이지 로딩되는데 바가 남아있음

all_flights= browser.find_elements(By.CLASS_NAME,'concurrent_inner__iqfJr')
result_list=[]
a_list=[]
r_list=[]
p_list=[]
tickets=[]
# for ticket in all_flights:  
#     =ticket.text

# airlines= browser.find_elements(By.CLASS_NAME,'airline_name__Tm2wJ') #항공사 이름
# routes =browser.find_elements(By.CLASS_NAME,'route_Route__2UInh') # 시간 공항
# prices =browser.find_elements(By.CLASS_NAME,'item_summary__3XqKA') # 가격정보

# for airline in airlines:
#     a_list.append(airline.text.strip())
# for route in routes:
#     r_list.append(route.text.strip())
# for price in prices:
#     p_list.append(price.text.strip())


for val in all_flights:
        try:
            # 각 항공권 요소마다 시간 가져오기
            time = val.find_elements(By.CLASS_NAME,'route_time__-2Z1T')
            tickets.append({
                # '로고': val.find_element(By.XPATH,'//*[@id="container"]/div/div/div/div/div/div/div/div/div/span/img')
                '항공': val.find_element(By.CLASS_NAME,'airline_name__Tm2wJ').text,
                '출발 시간1' : time[0].text,
                '도착 시간1' : time[1].text,
                '소요 시간1' : val.find_elements(By.CLASS_NAME,'route_info__1RhUH')[0].text,
                '출발 시간2' : time[2].text,
                '도착 시간2' : time[3].text,
                '소요 시간2' : val.find_elements(By.CLASS_NAME,'route_info__1RhUH')[1].text,
                '카드사' : val.find_element(By.CLASS_NAME,'item_type__2KJOZ').text,
                '가격' : val.find_element(By.CLASS_NAME,'item_num__3R0Vz').text

            })
        except:
            continue




import os 
import datetime
import pandas as pd

df = pd.DataFrame(tickets)

## 저장 디렉토리 생성
os.makedirs('ticket_info', exist_ok=True)


## 파일명 - %Y-%m-%d 
c_day = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
file_path=f"ticket_info/{c_day}.csv"
df.to_csv(file_path, index=False)
print(">>>>>>>>완료<<<<<<<<<")


