import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# 파일 저장 경로 설정
path = "./sample_data"
if not os.path.exists(path):
    os.makedirs(path)

# 기본 날짜 설정
base_date = datetime(2025, 12, 1)
dates = [base_date + timedelta(days=i) for i in range(30)]

print("🚀 더폴스타 맞춤형 가상 데이터 생성을 시작합니다...")

# 1. 광고 성과 (CSV)
df1 = pd.DataFrame({
    'Date': dates,
    'Exposures': np.random.randint(5000, 20000, 30),
    'Clicks': np.random.randint(200, 1000, 30),
    'Cost': np.random.randint(100000, 500000, 30),
    'Channel': np.random.choice(['Google', 'Meta', 'YouTube'], 30)
})
df1.to_csv(f"{path}/01_Ad_Performance.csv", index=False, encoding='utf-8-sig')

# 2. 언론 노출 내역 (Excel)
df2 = pd.DataFrame({
    'Date': dates[:10],
    'Media': ['Chosun', 'Joongang', 'Donga', 'MK', 'Hankyung'] * 2,
    'Title': [f"The Polestar PR News Article {i}" for i in range(10)],
    'Reach': np.random.randint(10000, 50000, 10)
})
df2.to_excel(f"{path}/02_Press_Monitoring.xlsx", index=False)

# 3. SNS 인게이지먼트 (CSV)
df3 = pd.DataFrame({
    'Platform': ['Instagram', 'Facebook', 'TikTok', 'X'] * 5,
    'Followers': np.random.randint(1000, 5000, 20),
    'Likes': np.random.randint(50, 500, 20),
    'Shares': np.random.randint(5, 50, 20)
})
df3.to_csv(f"{path}/03_Social_Engagement.csv", index=False, encoding='utf-8-sig')

# 4. 인플루언서 캠페인 (Excel)
df4 = pd.DataFrame({
    'Influencer': [f"Influencer_{chr(65+i)}" for i in range(10)],
    'Category': np.random.choice(['Tech', 'Beauty', 'Life'], 10),
    'Views': np.random.randint(5000, 100000, 10),
    'Cost': np.random.randint(1000000, 5000000, 10)
})
df4.to_excel(f"{path}/04_Influencer_Campaign.xlsx", index=False)

# 5. 웹 트래픽 분석 (CSV)
df5 = pd.DataFrame({
    'Source': ['Direct', 'Organic', 'Referral', 'Social'] * 10,
    'Sessions': np.random.randint(100, 1000, 40),
    'BounceRate': np.random.uniform(30.0, 70.0, 40),
    'ConvRate': np.random.uniform(1.0, 5.0, 40)
})
df5.to_csv(f"{path}/05_Web_Traffic.csv", index=False, encoding='utf-8-sig')

# 6. 경쟁사 벤치마킹 (Excel)
df6 = pd.DataFrame({
    'Brand': ['The Polestar', 'Competitor_A', 'Competitor_B', 'Competitor_C'],
    'MarketShare': [35.5, 25.0, 20.5, 19.0],
    'Mentions': [5400, 3200, 2100, 1900],
    'Score': [9.2, 7.5, 6.8, 6.2]
})
df6.to_excel(f"{path}/06_Competitor_Benchmarking.xlsx", index=False)

# 7. 일본 지사 마케팅 성과 (CSV)
df7 = pd.DataFrame({
    'Date': dates[:10],
    'City': ['Tokyo', 'Osaka', 'Fukuoka'] * 3 + ['Nagoya'],
    'Exposures': np.random.randint(3000, 15000, 10),
    'Cost_JPY': np.random.randint(10000, 50000, 10)
})
df7.to_csv(f"{path}/07_Global_Marketing_JP.csv", index=False, encoding='utf-8-sig')

# 8. 브랜드 평판 분석 (Excel)
df8 = pd.DataFrame({
    'Keyword': ['Service', 'Quality', 'Price', 'Communication', 'Speed'],
    'Positive': [75, 82, 45, 90, 60],
    'Neutral': [20, 10, 30, 8, 25],
    'Negative': [5, 8, 25, 2, 15]
})
df8.to_excel(f"{path}/08_Sentiment_Analysis.xlsx", index=False)

# 9. 오프라인 이벤트 KPI (CSV)
df9 = pd.DataFrame({
    'EventName': ['Launch Party', 'Pop-up Store', 'Tech Seminar'],
    'Visitors': [250, 1500, 80],
    'Leads': [45, 320, 12],
    'Satisfaction': [4.8, 4.2, 4.9]
})
df9.to_csv(f"{path}/09_Event_KPI.csv", index=False, encoding='utf-8-sig')

# 10. 월간 ROI 요약 (Excel)
df10 = pd.DataFrame({
    'Month': ['Oct', 'Nov', 'Dec'],
    'TotalSpend': [50000000, 65000000, 80000000],
    'Revenue': [120000000, 180000000, 250000000],
    'ROI': [2.4, 2.7, 3.1]
})
df10.to_excel(f"{path}/10_Monthly_ROI.xlsx", index=False)

print(f"✅ 모든 데이터 생성이 완료되었습니다! 폴더: {os.path.abspath(path)}")