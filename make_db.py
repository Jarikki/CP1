import sqlite3

#데이터프레임 db로 변환 및 기존 db파일에 데이터 추가
def df_to_db(datas_df):
    con = sqlite3.connect("data.db")
    datas_df.to_sql('data', con, if_exists="append", index=False)