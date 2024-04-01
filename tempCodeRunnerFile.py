flight_ticket_df=pd.DataFrame(tickets)

# ### 저장 디렉토리 생성
# os.makedirs('tickets_info', exist_ok=True)
# ### 파일명-%Y-%m-%d
# c_day=datetime.date.today().strftime("%Y-%m-%d")
# file_path=f"tickets_info/{c_day}.csv"
# flight_ticket_df.to_csv(file_path, index=False)
# print("============완료=============")