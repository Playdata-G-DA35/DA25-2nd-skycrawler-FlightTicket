from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import datetime
import time
import os
from sqlalchemy import create_engine
import pymysql

"""
    1. URL ==> 페이지 번호
    2. 조회할 항목 => SELECTOR
    3. 저장방식 (CSV)

"""

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

service=Service(executalbe_path=ChromeDriverManager().install())
browser=webdriver.Chrome(service=service, options=chrome_options)

# 네이버 항공권으로 이동
browser.get('https://flight.naver.com')
browser.maximize_window()



"""
    자동 검색

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
                        time.sleep(2)
                        day_element.click()
                        return
                



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
time.sleep(20)


"""
항공권 크롤링

"""

# 데이터 담을 변수
tickets=[]

# 항공권 개수
cnt=200


# 항공권 모든 데이터 크롤링하기
# all_flight_tickets = browser.find_elements(By.CSS_SELECTOR,'#container > div.international_content__2Z9HD > div > div.concurrent_ConcurrentList__1EKaB > div > div > div.concurrent_schedule__1Na5l > div')

# 항공권 구간 나누기 
all_flight_tickets=browser.find_elements(By.CLASS_NAME,'concurrent_ConcurrentItemContainer__2lQVG')


# 항공권 크롤링하기
for l, val in enumerate(all_flight_tickets):
    if l < cnt:
        try:
            # 각 항공권 마다 route time과 route code 가져오기
            time = val.find_elements(By.CLASS_NAME,'route_time__-2Z1T') ## 각 항공권 마다 route time 가져오기
            airline = val.find_elements(By.CLASS_NAME,'airline_name__Tm2wJ')
            route_info = val.find_elements(By.CLASS_NAME,'route_info__1RhUH')
            
            if len(airline) == 1:
                tickets.append({
                    'out_항공': airline[0].text,
                    'out_출발시간' : time[0].text,
                    'out_도착시간' : time[1].text,
                    'out_소요시간' : route_info[0].text,
                    'in_항공': airline[0].text, 
                    'in_출발시간' : time[2].text,
                    'in_도착시간' : time[3].text,
                    'in_소요시간' : route_info[1].text,
                    '카드사' : val.find_element(By.CLASS_NAME,'item_type__2KJOZ').text,
                    '가격' : val.find_element(By.CLASS_NAME,'item_num__3R0Vz').text
                })
            else:
                tickets.append({
                    'out_항공': airline[0].text,
                    'out_출발시간' : time[0].text,
                    'out_도착시간' : time[1].text,
                    'out_소요시간' : route_info[0].text,
                    'in_항공': airline[1].text,
                    'in_출발시간' : time[2].text,
                    'in_도착시간' : time[3].text,
                    'in_소요시간' : route_info[1].text,
                    '카드사' : val.find_element(By.CLASS_NAME,'item_type__2KJOZ').text,
                    '가격' : val.find_element(By.CLASS_NAME,'item_num__3R0Vz').text
                })

        except:
            continue

# browser 연결 끊기
# browser.close()


# list -> dataframe
df = pd.DataFrame(tickets)


# # 컬럼명, MultiIndex 지정
# new_column_names = [('가는 편', '항공사'), ('가는 편', '출발 시간 (공항)'), ('가는 편', '도착 시간 (공항)'), ('가는 편', '소요 시간'),
#                     ('오는 편', '항공사'), ('오는 편', '출발 시간 (공항)'), ('오는 편', '도착 시간 (공항)'), ('오는 편', '소요 시간'),
#                     ('구분','카드사'), ('구분','가격(원)')]
# multi_index = pd.MultiIndex.from_tuples(new_column_names)
# df.columns = multi_index


# # 스트링 타입으로 나누고 출발시간 (공항) 형식으로 나누기
# # df[('구분', '가격(원)')] = df[('구분', '가격(원)')].astype(str).replace(',','').astype(int)
# df[('가는 편','도착 시간 (공항)')] = df[('가는 편','도착 시간 (공항)')].astype(str).apply(lambda x: '{} ({})'.format(x[:-3], x[-3:]))
# df[('가는 편','출발 시간 (공항)')] = df[('가는 편','출발 시간 (공항)')].astype(str).apply(lambda x: '{} ({})'.format(x[:-3], x[-3:]))
# df[('오는 편','출발 시간 (공항)')] = df[('오는 편','출발 시간 (공항)')].astype(str).apply(lambda x: '{} ({})'.format(x[:-3], x[-3:]))
# df[('오는 편','도착 시간 (공항)')] = df[('오는 편','도착 시간 (공항)')].astype(str).apply(lambda x: '{} ({})'.format(x[:-3], x[-3:]))


# 가격이 낮은 순으로 df 정렬
# df=df.sort_values(by=('구분','가격(원)'))


### 저장 디렉토리 생성
os.makedirs('tickets_info', exist_ok=True)
### 파일명-%Y-%m-%d
c_day=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
file_path=f"tickets_info/from_{start_area}to_{end_area}{c_day}.csv"
df.to_csv(file_path)

print("============완료=============")


'''
    db 연결

'''
# db 연결
engine= create_engine(
    "mysql+pymysql://2nd_project:1111@127.0.0.1:3306/db?charset=utf8"  #계정, 비밀번호
)
# db 연결 및 시작

try: 
    tran = None
    conn = None
    with engine.connect() as conn:
        tran = conn.begin()

    df.to_sql('ft', con=engine, if_exists='replace')

    tran.commit()

except Exception as e:
    if tran:
        tran.rollback()
    print("Transaction rolled back due to an error:", e)

# db 연결 끊기
finally:
    if conn:
        conn.close()
    engine.dispose()
    print('lid_rtate_vmtc: Transaction closed successfully')