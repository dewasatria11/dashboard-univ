import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Dashboard Universitas - Student Performance",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS FOR PREMIUM LOOK - GREEN & WHITE THEME
# ============================================
st.markdown("""
<style>
    /* Hide Streamlit loading indicators (status + spinners) */
    div[data-testid="stStatusWidget"],
    div[data-testid="stSpinner"],
    div[data-testid="stPageLoadingIndicator"],
    .stSpinner {
        display: none !important;
    }

    /* ========== ANIMATIONS ========== */
    @keyframes fadeInUp {
        0% {
            opacity: 0;
            transform: translateY(30px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInScale {
        0% {
            opacity: 0;
            transform: scale(0.8);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes slideInLeft {
        0% {
            opacity: 0;
            transform: translateX(-50px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            transform: scale(1);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }
    
    /* Title animation */
    h1 {
        animation: fadeInUp 0.8s ease-out forwards;
    }
    
    /* Subtitle/description animation */
    [data-testid="stMarkdownContainer"] > p:first-child {
        animation: fadeInUp 0.8s ease-out 0.2s forwards;
        opacity: 0;
        animation-fill-mode: forwards;
    }
    
    /* Metric cards animation - staggered */
    [data-testid="metric-container"] {
        animation: bounceIn 0.6s ease-out forwards;
        opacity: 0;
        animation-fill-mode: forwards;
    }
    
    [data-testid="column"]:nth-child(1) [data-testid="metric-container"] {
        animation-delay: 0.3s;
    }
    
    [data-testid="column"]:nth-child(2) [data-testid="metric-container"] {
        animation-delay: 0.5s;
    }
    
    [data-testid="column"]:nth-child(3) [data-testid="metric-container"] {
        animation-delay: 0.7s;
    }
    
    [data-testid="column"]:nth-child(4) [data-testid="metric-container"] {
        animation-delay: 0.9s;
    }
    
    /* Subheaders animation */
    h2, h3 {
        animation: slideInLeft 0.7s ease-out forwards;
        opacity: 0;
        animation-fill-mode: forwards;
        animation-delay: 0.5s;
    }
    
    /* Chart containers animation */
    .stPlotlyChart {
        animation: fadeInScale 0.8s ease-out forwards;
        opacity: 0;
        animation-fill-mode: forwards;
        animation-delay: 1s;
    }
    
    /* Sidebar animation */
    [data-testid="stSidebar"] > div {
        animation: slideInLeft 0.6s ease-out forwards;
    }
    
    /* Table animation */
    [data-testid="stMarkdownContainer"] > div {
        animation: fadeInUp 0.8s ease-out forwards;
        opacity: 0;
        animation-fill-mode: forwards;
        animation-delay: 1.2s;
    }
    
    /* Horizontal rule animation */
    hr {
        animation: fadeInUp 0.5s ease-out forwards;
    }
    
    /* Hover effects for interactive elements */
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(46, 125, 50, 0.25);
        transition: all 0.3s ease;
    }
    
    .stPlotlyChart:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.15);
        transition: all 0.3s ease;
    }
    
    /* Main background - Light green gradient */
    .stApp {
        background: linear-gradient(135deg, #f0fff4 0%, #e8f5e9 100%);
    }
    
    /* Streamlit Header/Toolbar - White/Light theme */
    header[data-testid="stHeader"] {
        background: #ffffff !important;
        border-bottom: 1px solid rgba(46, 125, 50, 0.2);
    }
    
    /* Header toolbar buttons */
    header[data-testid="stHeader"] button {
        color: #333333 !important;
    }
    
    header[data-testid="stHeader"] svg {
        fill: #333333 !important;
        color: #333333 !important;
    }
    
    /* Decoration/status bar */
    [data-testid="stDecoration"] {
        background: #2e7d32 !important;
    }
    
    /* Status widget */
    [data-testid="stStatusWidget"] {
        background: #ffffff !important;
        color: #333333 !important;
    }
    
    [data-testid="stStatusWidget"] label {
        color: #333333 !important;
    }
    
    /* Toolbar actions */
    [data-testid="stToolbar"] {
        background: #ffffff !important;
    }
    
    [data-testid="stToolbar"] button {
        color: #333333 !important;
    }
    
    /* App menu (hamburger menu) */
    [data-testid="stMainMenu"] {
        background: #ffffff !important;
    }
    
    [data-testid="stMainMenu"] button {
        color: #333333 !important;
    }
    
    /* Deploy button area */
    .stDeployButton {
        background: #ffffff !important;
    }
    
    .stDeployButton button {
        background: #2e7d32 !important;
        color: #ffffff !important;
    }
    
    /* Sidebar styling - Green theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2e7d32 0%, #1b5e20 100%);
        border-right: 1px solid rgba(46, 125, 50, 0.3);
    }
    
    /* Headers - Dark green */
    h1, h2, h3 {
        color: #1b5e20 !important;
    }
    
    /* Metric cards - Green accent */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.1) 0%, rgba(200, 230, 201, 0.5) 100%);
        border: 1px solid rgba(46, 125, 50, 0.3);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    [data-testid="stMetricValue"] {
        color: #1b5e20 !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4a4a4a !important;
    }
    
    /* Cards/containers */
    .stPlotlyChart {
        background: rgba(255,255,255,0.8);
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(46, 125, 50, 0.2);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Dataframe - White background */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        background: #ffffff !important;
    }
    
    /* Dataframe container */
    [data-testid="stDataFrame"] > div {
        background: #ffffff !important;
    }
    
    [data-testid="stDataFrame"] {
        background: #ffffff !important;
    }
    
    /* Table styling */
    .stDataFrame table {
        background: #ffffff !important;
    }
    
    .stDataFrame th {
        background: #2e7d32 !important;
        color: #ffffff !important;
    }
    
    .stDataFrame td {
        background: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Streamlit data editor and table */
    [data-testid="stDataFrameResizable"] {
        background: #ffffff !important;
    }
    
    /* Glide data grid (new streamlit tables) - COMPREHENSIVE */
    .dvn-scroller {
        background: #ffffff !important;
    }
    
    [data-testid="glideDataEditor"] {
        background: #ffffff !important;
    }
    
    /* All glide data grid cells and text */
    .gdg-header, .gdg-header-container {
        background: #2e7d32 !important;
        color: #ffffff !important;
    }
    
    .gdg-cell, .gdg-data-cell {
        background: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Canvas wrapper for dataframe */
    [data-testid="stDataFrame"] canvas {
        background: #ffffff !important;
    }
    
    /* Data cell text in glide grid */
    .dvn-stack, .dvn-underlay, .dvn-overlay {
        background: #ffffff !important;
    }
    
    /* Override all text inside dataframe to be dark */
    [data-testid="stDataFrame"] * {
        color: #333333 !important;
    }
    
    /* But keep header text white */
    [data-testid="stDataFrame"] th,
    [data-testid="stDataFrame"] .gdg-header {
        color: #ffffff !important;
    }
    
    /* Glide cells specifically */
    [class*="glide"] {
        background: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Data cell styling for new streamlit */
    [data-testid="StyledDataFrameDataCell"] {
        color: #333333 !important;
        background: #ffffff !important;
    }
    
    [data-testid="StyledDataFrameHeaderCell"] {
        color: #ffffff !important;
        background: #2e7d32 !important;
    }
    
    /* Styled dataframe container */
    [data-testid="stStyledDataFrame"] {
        background: #ffffff !important;
    }
    
    [data-testid="stStyledDataFrame"] * {
        color: #333333 !important;
    }
    
    [data-testid="stStyledDataFrame"] th {
        color: #ffffff !important;
        background: #2e7d32 !important;
    }
    
    /* Select boxes - Main content area */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(46, 125, 50, 0.3);
        border-radius: 8px;
    }
    
    /* Main content text - Dark for readability */
    p, span, label, div, .stSelectbox label, .stMarkdown {
        color: #333333 !important;
    }
    
    /* Headers keep green color */
    h1, h2, h3, h4, h5, h6 {
        color: #1b5e20 !important;
    }
    
    /* Sidebar text - White for contrast (except selectbox) */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] > div > div > div > p,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #ffffff !important;
    }
    
    /* SIDEBAR SELECTBOX - White background with dark text */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
        color: #333333 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div {
        color: #333333 !important;
        background: #ffffff !important;
    }
    
    /* Sidebar selectbox arrow/icon */
    [data-testid="stSidebar"] .stSelectbox svg {
        fill: #333333 !important;
        color: #333333 !important;
    }
    
    /* Selectbox text in main area */
    .stSelectbox div[data-baseweb="select"] span {
        color: #333333 !important;
    }
    
    /* Dropdown menu options - BOTH main and sidebar */
    [data-baseweb="menu"], [data-baseweb="popover"] {
        background: #ffffff !important;
    }
    
    [data-baseweb="menu"] li, [data-baseweb="popover"] li {
        color: #333333 !important;
        background: #ffffff !important;
    }
    
    [data-baseweb="menu"] li:hover, [data-baseweb="popover"] li:hover {
        background: #e8f5e9 !important;
        color: #1b5e20 !important;
    }
    
    /* Dropdown list container */
    [data-baseweb="list"] {
        background: #ffffff !important;
    }
    
    [data-baseweb="list"] li {
        color: #333333 !important;
        background: #ffffff !important;
    }
    
    [data-baseweb="list"] li:hover {
        background: #e8f5e9 !important;
        color: #1b5e20 !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Info box in sidebar - White text */
    [data-testid="stSidebar"] .stAlert {
        background: rgba(255,255,255,0.2) !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
    }
    
    [data-testid="stSidebar"] .stAlert p,
    [data-testid="stSidebar"] .stAlert span,
    [data-testid="stSidebar"] .stAlert div,
    [data-testid="stSidebar"] .stAlert strong,
    [data-testid="stSidebar"] .stAlert b,
    [data-testid="stSidebar"] [data-testid="stAlertContentInfo"],
    [data-testid="stSidebar"] [data-testid="stAlertContentInfo"] * {
        color: #ffffff !important;
    }
    
    /* Sidebar info icon */
    [data-testid="stSidebar"] .stAlert svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }
    
    /* Main block container */
    [data-testid="stMainBlockContainer"] {
        background: transparent !important;
    }
    
    /* Ensure all containers are white/transparent */
    .element-container {
        background: transparent !important;
    }
    
    /* Caption text */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #666666 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #ffffff !important;
        color: #333333 !important;
    }
    
    .streamlit-expanderContent {
        background: #ffffff !important;
    }
    
    /* Markdown text */
    [data-testid="stMarkdownContainer"] p {
        color: #333333 !important;
    }
    
    /* Horizontal rule */
    hr {
        border-color: rgba(46, 125, 50, 0.2) !important;
    }
    
    /* Column gap fix */
    [data-testid="column"] {
        background: transparent !important;
    }
    
    /* ========== COMPREHENSIVE FONT COLOR FIX ========== */
    
    /* All text elements - Force black */
    .stApp p, .stApp span, .stApp label, .stApp div {
        color: #333333 !important;
    }
    
    /* Keep headers green */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #1b5e20 !important;
    }
    
    /* Sidebar override - keep white */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Widget labels */
    .stTextInput label, .stSelectbox label, .stMultiSelect label, 
    .stSlider label, .stCheckbox label, .stRadio label {
        color: #333333 !important;
    }
    
    /* Input text */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        color: #333333 !important;
        background: #ffffff !important;
    }
    
    /* Selectbox selected value */
    [data-baseweb="select"] > div {
        color: #333333 !important;
    }
    
    /* Tooltip and info */
    [data-testid="stTooltipContent"] {
        color: #333333 !important;
        background: #ffffff !important;
    }
    
    /* Metric delta */
    [data-testid="stMetricDelta"] {
        color: #2e7d32 !important;
    }
    
    /* Alert/Info boxes in main area */
    .stAlert {
        color: #333333 !important;
    }
    
    /* Strong and bold text */
    strong, b {
        color: #333333 !important;
    }
    
    /* Links */
    a {
        color: #2e7d32 !important;
    }
    
    a:hover {
        color: #1b5e20 !important;
    }
    
    /* Code blocks */
    code {
        color: #333333 !important;
        background: rgba(46, 125, 50, 0.1) !important;
    }
    
    /* Table text - ensure visibility */
    table, th, td {
        color: #333333 !important;
    }
    
    th {
        background: #2e7d32 !important;
        color: #ffffff !important;
    }
    
    /* Plotly chart text override */
    .js-plotly-plot .plotly text {
        fill: #333333 !important;
    }
    
    /* Button text */
    .stButton button {
        color: #ffffff !important;
        background: #2e7d32 !important;
    }
    
    .stButton button:hover {
        background: #1b5e20 !important;
    }
    
    /* Download button */
    .stDownloadButton button {
        color: #ffffff !important;
        background: #2e7d32 !important;
    }
    
    /* Checkbox and radio labels */
    .stCheckbox span, .stRadio span {
        color: #333333 !important;
    }
    
    /* Slider values */
    .stSlider [data-baseweb="slider"] div {
        color: #333333 !important;
    }
    
    /* Number input */
    .stNumberInput div {
        color: #333333 !important;
    }
    
    /* Date input */
    .stDateInput div {
        color: #333333 !important;
    }
    
    /* File uploader */
    .stFileUploader div {
        color: #333333 !important;
    }
    
    /* Progress bar text */
    .stProgress div {
        color: #333333 !important;
    }
    
    /* Spinner text */
    .stSpinner div {
        color: #333333 !important;
    }
    
    /* Empty state text */
    [data-testid="stEmpty"] {
        color: #333333 !important;
    }
    
    /* JSON viewer */
    .stJson {
        color: #333333 !important;
        background: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING
# ============================================
@st.cache_data
def load_data():
    """Load and preprocess student performance data."""
    df = pd.read_csv("data/Student_Performance_Data.csv")
    # Extract year from Student_ID (e.g., SID20131143 -> 2013)
    df['Year'] = df['Student_ID'].str.extract(r'SID(\d{4})').astype(int)
    # Convert semester name to number for sorting
    df['Semester_Num'] = df['Semster_Name'].str.extract(r'Sem_(\d+)').astype(int)
    return df

df = load_data()

# ============================================
# IPK CONVERSION FUNCTION
# ============================================
def marks_to_ipk(marks):
    """Convert marks (0-100) to IPK (0-4.00) scale."""
    if marks >= 85:
        return 4.00
    elif marks >= 80:
        return 3.50
    elif marks >= 75:
        return 3.00
    elif marks >= 70:
        return 2.50
    elif marks >= 60:
        return 2.00
    elif marks >= 50:
        return 1.00
    else:
        return 0.00

# ============================================
# SIDEBAR - FILTERS
# ============================================
st.sidebar.title("🎓 Dashboard Universitas")
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filter Data")

# Semester filter
all_semesters = ["Semua Semester"] + sorted(df['Semster_Name'].unique().tolist(), key=lambda x: int(x.split('_')[1]))
selected_semester = st.sidebar.selectbox(
    "Pilih Semester:",
    all_semesters,
    index=0
)

# Paper/Course filter
all_papers = ["Semua Mata Kuliah"] + sorted(df['Paper_Name'].unique().tolist())
selected_paper = st.sidebar.selectbox(
    "Pilih Mata Kuliah:",
    all_papers,
    index=0
)

# Year filter
all_years = ["Semua Tahun"] + sorted(df['Year'].unique().tolist())
selected_year = st.sidebar.selectbox(
    "Pilih Tahun Angkatan:",
    all_years,
    index=0
)

# Apply filters
filtered_df = df.copy()
if selected_semester != "Semua Semester":
    filtered_df = filtered_df[filtered_df['Semster_Name'] == selected_semester]
if selected_paper != "Semua Mata Kuliah":
    filtered_df = filtered_df[filtered_df['Paper_Name'] == selected_paper]
if selected_year != "Semua Tahun":
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]

st.sidebar.markdown("---")
st.sidebar.info(f"📊 **Data yang ditampilkan:** {len(filtered_df):,} records")

# ============================================
# MAIN CONTENT - HEADER
# ============================================
st.markdown('<p style="color: #333333; font-size: 1rem; font-weight: 500; margin-bottom: 0;">Tugas Dewa Satria</p>', unsafe_allow_html=True)
st.title("📊 Dashboard Performa Akademik Mahasiswa")
st.markdown("**Analisis komprehensif data performa mahasiswa universitas**")
st.markdown("---")

# ============================================
# KPI METRICS ROW
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_students = filtered_df['Student_ID'].nunique()
    st.metric(
        label="👨‍🎓 Total Mahasiswa",
        value=f"{total_students:,}",
        delta=None
    )

with col2:
    avg_marks = filtered_df['Marks'].mean()
    avg_ipk = marks_to_ipk(avg_marks)
    st.metric(
        label="📈 IPK Rata-rata",
        value=f"{avg_ipk:.2f}",
        delta=None
    )

with col3:
    max_marks = filtered_df['Marks'].max()
    st.metric(
        label="🏆 Nilai Tertinggi",
        value=f"{max_marks}",
        delta=None
    )

with col4:
    min_marks = filtered_df['Marks'].min()
    st.metric(
        label="📉 Nilai Terendah",
        value=f"{min_marks}",
        delta=None
    )

st.markdown("---")

# ============================================
# CHARTS ROW 1 - Line Chart & Bar Chart
# ============================================
col_left, col_right = st.columns(2)

# Line Chart - Trend rata-rata nilai per semester
with col_left:
    st.subheader("📈 Tren Nilai Per Semester")
    
    semester_trend = filtered_df.groupby('Semester_Num')['Marks'].mean().reset_index()
    semester_trend['Semester'] = semester_trend['Semester_Num'].apply(lambda x: f"Semester {x}")
    
    fig_line = px.line(
        semester_trend,
        x='Semester',
        y='Marks',
        markers=True,
        template='plotly_white'
    )
    fig_line.update_traces(
        line=dict(color='#2e7d32', width=3),
        marker=dict(size=10, color='#4caf50', line=dict(width=2, color='white'))
    )
    fig_line.update_layout(
        plot_bgcolor='rgba(255,255,255,0.8)',
        paper_bgcolor='rgba(255,255,255,0)',
        xaxis_title="Semester",
        yaxis_title="Rata-rata Nilai",
        font=dict(color='#333333'),
        yaxis=dict(range=[0, 100]),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#ffffff',
            font_size=14,
            font_family='Arial',
            font_color='#333333',
            bordercolor='#2e7d32'
        )
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Bar Chart - Rata-rata nilai per mata kuliah
with col_right:
    st.subheader("📊 Nilai Per Mata Kuliah")
    
    paper_avg = filtered_df.groupby('Paper_Name')['Marks'].mean().reset_index()
    paper_avg = paper_avg.sort_values('Marks', ascending=True)
    
    colors = px.colors.sequential.RdPu[::-1][:len(paper_avg)]
    
    fig_bar = px.bar(
        paper_avg,
        x='Marks',
        y='Paper_Name',
        orientation='h',
        template='plotly_white',
        color='Marks',
        color_continuous_scale='Greens'
    )
    fig_bar.update_layout(
        plot_bgcolor='rgba(255,255,255,0.8)',
        paper_bgcolor='rgba(255,255,255,0)',
        xaxis_title="Rata-rata Nilai",
        yaxis_title="",
        font=dict(color='#333333'),
        showlegend=False,
        coloraxis_showscale=False,
        xaxis=dict(range=[0, 100]),
        hoverlabel=dict(
            bgcolor='#ffffff',
            font_size=14,
            font_family='Arial',
            font_color='#333333',
            bordercolor='#2e7d32'
        )
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ============================================
# CHARTS ROW 2 - Histogram & Pie Chart
# ============================================
col_left2, col_right2 = st.columns(2)

# Histogram - Distribusi nilai
with col_left2:
    st.subheader("📉 Distribusi Nilai Mahasiswa")
    
    fig_hist = px.histogram(
        filtered_df,
        x='Marks',
        nbins=20,
        template='plotly_white',
        color_discrete_sequence=['#4caf50']
    )
    fig_hist.update_layout(
        plot_bgcolor='rgba(255,255,255,0.8)',
        paper_bgcolor='rgba(255,255,255,0)',
        xaxis_title="Nilai",
        yaxis_title="Frekuensi",
        font=dict(color='#333333'),
        bargap=0.1,
        hoverlabel=dict(
            bgcolor='#ffffff',
            font_size=14,
            font_family='Arial',
            font_color='#333333',
            bordercolor='#2e7d32'
        )
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Pie Chart - Kategori nilai
with col_right2:
    st.subheader("🎯 Kategori Nilai")
    
    def categorize_marks(mark):
        if mark >= 85:
            return 'A (Sangat Baik)'
        elif mark >= 70:
            return 'B (Baik)'
        elif mark >= 55:
            return 'C (Cukup)'
        elif mark >= 40:
            return 'D (Kurang)'
        else:
            return 'E (Sangat Kurang)'
    
    filtered_df_copy = filtered_df.copy()
    filtered_df_copy['Grade'] = filtered_df_copy['Marks'].apply(categorize_marks)
    grade_counts = filtered_df_copy['Grade'].value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Count']
    
    fig_pie = px.pie(
        grade_counts,
        values='Count',
        names='Grade',
        template='plotly_white',
        color_discrete_sequence=['#1b5e20', '#2e7d32', '#4caf50', '#81c784', '#c8e6c9'],
        hole=0.4
    )
    fig_pie.update_layout(
        plot_bgcolor='rgba(255,255,255,0.8)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(color='#333333'),
        legend=dict(orientation='h', yanchor='bottom', y=-0.2),
        hoverlabel=dict(
            bgcolor='#ffffff',
            font_size=14,
            font_family='Arial',
            font_color='#333333',
            bordercolor='#2e7d32'
        )
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# ============================================
# DATA TABLE
# ============================================
st.subheader("📋 Detail Data Mahasiswa")

# Summary statistics per student
student_summary = filtered_df.groupby('Student_ID').agg({
    'Marks': ['mean', 'min', 'max', 'count'],
    'Year': 'first'
}).reset_index()
student_summary.columns = ['Student_ID', 'Rata-rata Nilai', 'Nilai Min', 'Nilai Max', 'Jumlah MK', 'Tahun Angkatan']
student_summary['IPK'] = student_summary['Rata-rata Nilai'].apply(marks_to_ipk)
student_summary['Rata-rata Nilai'] = student_summary['Rata-rata Nilai'].round(2)
student_summary = student_summary[['Student_ID', 'IPK', 'Rata-rata Nilai', 'Nilai Min', 'Nilai Max', 'Jumlah MK', 'Tahun Angkatan']]
student_summary = student_summary.sort_values('IPK', ascending=False)

# Display as HTML table with proper styling
def create_html_table(df):
    html = '''
    <div style="overflow-x: auto; border-radius: 12px; border: 1px solid #c8e6c9;">
        <table style="width: 100%; border-collapse: collapse; background: #ffffff;">
            <thead>
                <tr style="background: #2e7d32;">
    '''
    # Header
    for col in df.columns:
        html += f'<th style="padding: 12px 15px; text-align: left; color: #ffffff; font-weight: bold; border-bottom: 2px solid #1b5e20;">{col}</th>'
    html += '</tr></thead><tbody>'
    
    # Rows
    for idx, row in df.iterrows():
        bg_color = '#ffffff' if idx % 2 == 0 else '#f5f5f5'
        html += f'<tr style="background: {bg_color};">'
        for val in row:
            html += f'<td style="padding: 10px 15px; color: #333333; border-bottom: 1px solid #e0e0e0;">{val}</td>'
        html += '</tr>'
    
    html += '</tbody></table></div>'
    return html

st.markdown(create_html_table(student_summary.head(10).reset_index(drop=True)), unsafe_allow_html=True)
st.caption(f"Menampilkan 10 data teratas dari {len(student_summary)} mahasiswa")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🎓 <b>Dashboard Universitas</b> - Student Performance Analysis</p>
    <p>Data Source: <a href="https://www.kaggle.com/datasets/ananta/student-performance-dataset" target="_blank">Kaggle - Student Performance Dataset</a></p>
    <p>Built with ❤️ using Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
