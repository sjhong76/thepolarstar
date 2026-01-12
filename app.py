import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
import os
from datetime import datetime
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from dotenv import load_dotenv
from openai import OpenAI

# --- 0. 환경 변수 로드 및 OpenAI 클라이언트 설정 ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# --- 1. 페이지 설정 및 디자인 ---
st.set_page_config(page_title="PolarStar Navigator", page_icon="🌟", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stApp { background: radial-gradient(circle at top right, #001529, #0e1117); }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        padding-bottom: 1rem;
    }
    .stButton>button {
        border-radius: 8px;
        background: linear-gradient(45deg, #004a99, #007bff);
        color: white;
        border: none;
    }
    .log-card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4facfe;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 세션 상태 초기화 ---
if 'db_data' not in st.session_state:
    st.session_state.db_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=5, freq='D'),
        'Exposures': np.random.randint(1000, 5000, 5),
        'Clicks': np.random.randint(100, 500, 5),
        'Cost': np.random.randint(50000, 200000, 5),
        'Label': ['Existing' for _ in range(5)]
    })

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'upload_log' not in st.session_state:
    st.session_state.upload_log = []
if 'report_log' not in st.session_state:
    st.session_state.report_log = []

# --- 3. 핵심 기능 함수 ---

def safe_display_df(df):
    df_display = df.copy()
    df_display.columns = [str(c) for c in df_display.columns]
    return df_display.fillna("")

def generate_pdf_report(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, text="PolarStar Navigator - Business Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font("helvetica", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, text=f"Generated Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return bytes(pdf.output())

def get_openai_response(prompt, df):
    cols = df.columns.tolist()
    total_rows = len(df)
    
    stats_info = ""
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols:
        stats_info = "수치 데이터 요약:\n"
        for c in num_cols:
            stats_info += f"- {c}: 평균 {df[c].mean():,.2f}, 최대 {df[c].max():,.2f}\n"
    
    date_range = "정보 없음"
    date_col = next((c for c in cols if 'date' in str(c).lower() or '날짜' in str(c)), None)
    if date_col:
        try:
            temp_date = pd.to_datetime(df[date_col], errors='coerce')
            date_range = f"{temp_date.min().date()} ~ {temp_date.max().date()}"
        except:
            date_range = "날짜 형식 분석 불가"

    data_summary = f"""
    [현재 DB 데이터 상태]
    - 사용 가능한 컬럼: {', '.join(cols)}
    - 총 레코드 수: {total_rows}건
    - 데이터 기간: {date_range}
    {stats_info}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": f"너는 '더폴스타'의 전문 AI 컨설턴트 'PolarStar Navigator'야. 다음 데이터를 바탕으로 전문적으로 답변해줘. {data_summary}"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ 분석 중 오류가 발생했습니다: {str(e)}"

# --- 4. 사이드바 내비게이션 ---
with st.sidebar:
    st.markdown("### 🛰️ NAVIGATION")
    menu = st.radio("Select Page", ["Navigator Chat", "Dashboard", "Data Factory"], index=0)
    st.divider()
    st.caption("PolarStar Navigator v1.7")

# --- 5. 페이지 1: Navigator Chat ---
if menu == "Navigator Chat":
    st.markdown('<p class="main-title">Navigator Chat</p>', unsafe_allow_html=True)
    
    chat_display = st.container(height=450)
    with chat_display:
        if not st.session_state.chat_history:
            st.info("안녕하세요, 주인님. 어떤 데이터를 분석해 드릴까요?")
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    uploaded_file = st.file_uploader("새로운 데이터를 여기에 드래그하세요 (Excel/CSV)", type=['xlsx', 'csv'])
    
    if uploaded_file:
        try:
            new_df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file, encoding='utf-8-sig')
            with st.expander("📄 데이터 미리보기", expanded=True):
                st.dataframe(safe_display_df(new_df.head(3)), width='stretch')
                if st.button("Confirm: DB 등록"):
                    st.session_state.db_data = pd.concat([st.session_state.db_data, new_df], ignore_index=True, sort=False)
                    st.session_state.upload_log.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "filename": uploaded_file.name, "rows": len(new_df)})
                    st.success("등록 완료!")
        except Exception as e:
            st.error(f"파일을 읽는 중 에러가 발생했습니다: {e}")

    if prompt := st.chat_input("질문을 입력하세요..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.spinner("분석 중..."):
            response = get_openai_response(prompt, st.session_state.db_data)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# --- 6. 페이지 2: Dashboard ---
elif menu == "Dashboard":
    st.markdown('<p class="main-title">System Dashboard</p>', unsafe_allow_html=True)
    num_df = st.session_state.db_data.select_dtypes(include=[np.number])
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("DB 레코드", f"{len(st.session_state.db_data)}건")
    with c2:
        val = num_df.iloc[:, 0].mean() if not num_df.empty else 0
        label = num_df.columns[0] if not num_df.empty else "데이터 없음"
        st.metric(f"평균 {label}", f"{val:,.0f}")
    with c3:
        pdf_bytes = generate_pdf_report(st.session_state.db_data)
        if st.download_button("📄 PDF 보고서 생성", data=pdf_bytes, file_name="Report.pdf", mime="application/pdf"):
            st.session_state.report_log.insert(0, {"time": datetime.now().strftime("%H:%M"), "name": "Performance Report"})

    st.divider()
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("📂 업로드 이력")
        for log in st.session_state.upload_log[:5]:
            st.markdown(f'<div class="log-card"><strong>{log["filename"]}</strong><br><small>{log["time"]}</small></div>', unsafe_allow_html=True)
    with col_r:
        st.subheader("📑 보고서 이력")
        for log in st.session_state.report_log[:5]:
            st.markdown(f'<div class="log-card" style="border-left-color:#ffc107;"><strong>{log["name"]}</strong><br><small>{log["time"]}</small></div>', unsafe_allow_html=True)

# --- 7. 페이지 3: Data Factory ---
elif menu == "Data Factory":
    st.markdown('<p class="main-title">Data Factory</p>', unsafe_allow_html=True)
    st.dataframe(safe_display_df(st.session_state.db_data), width='stretch')
    if st.button("데이터 정제 (중복 제거)"):
        st.session_state.db_data = st.session_state.db_data.drop_duplicates()
        st.rerun()