import streamlit as st
import pandas as pd

st.title("血圧表変換")

rawcsv = st.file_uploader("upload file", type={"csv", "txt"})
if rawcsv is not None:
    df = pd.read_csv(rawcsv)

    # 測定日を日時形式に変換
    df['測定日'] = pd.to_datetime(df['測定日'])


    # 日付と時刻を分離 もし時刻がAM5時以前なら日付を前日にする
    df['date'] = df['測定日'].dt.date - pd.to_timedelta((df['測定日'].dt.time < pd.to_datetime('05:00:00').time()).astype(int), unit='d')
    df['time'] = df['測定日'].dt.time

    # 朝と夜のデータを分ける  午前5時より前のデータは前日夜、午前5時以降のデータは当日朝、１２時以降は当日夜とする
    df_morning = df[(df['time'] >= pd.to_datetime('05:00:00').time()) & (df['time'] < pd.to_datetime('12:00:00').time())]
    df_evening = df[(df['time'] >= pd.to_datetime('12:00:00').time()) | (df['time'] < pd.to_datetime('05:00:00').time())]

    # 日付ごとにグループ化して最初の測定値を取得
    morning_data = df_morning.groupby('date').agg({
        '最高血圧(mmHg)': 'first', 
        '最低血圧(mmHg)': 'first', 
        '脈拍(bpm)': 'first'
    }).reset_index()

    evening_data = df_evening.groupby('date').agg({
        '最高血圧(mmHg)': 'first', 
        '最低血圧(mmHg)': 'first', 
        '脈拍(bpm)': 'first'
    }).reset_index()

    # 日付をマージする前に文字列に変換
    morning_data['date'] = morning_data['date'].astype(str)
    evening_data['date'] = evening_data['date'].astype(str)

    # 朝と夜のデータを日付でマージ
    df_final = pd.merge(morning_data, evening_data, on='date',how="outer", suffixes=('_morning', '_evening'))

    # カラム名を変更
    df_final.columns = [
        '日付', 
        '朝：最高血圧(mmHg)', 
        '朝：最低血圧(mmHg)', 
        '朝：脈拍(bpm)', 
        '夜：最高血圧(mmHg)', 
        '夜：最低血圧(mmHg)', 
        '夜：脈拍'
    ]

    tab1 , tab2 = st.tabs(["変換前","変換後"])
    tab1.write(df)
    tab2.write(df_final)

