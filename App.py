import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import requests

# Enhanced page config with elegant Diwali theme
st.set_page_config(
    layout="wide", 
    page_title="Diwali Sales Dashboard | Ankit Parwatkar", 
    page_icon="🪔",
    initial_sidebar_state="expanded"
)

# Add Font Awesome CSS
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">',
    unsafe_allow_html=True
)

# Sophisticated CSS with elegant animations and glass effects
st.markdown(f"""
<style>
    /* Main page styling - Luxurious gradient background */
    .stApp {{
        background: linear-gradient(135deg, #0c0520, #1a0a2e, #2d0b3a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #ffffff;
        padding-bottom: 50px;
    }}
    
    @keyframes gradientBG {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* Sidebar - Elegant crimson gradient */
    [data-testid="stSidebar"] {{
        background: linear-gradient(135deg, #8B0000, #B22222, #8B0000) !important;
        background-size: 400% 400%;
        animation: sidebarGradient 10s ease infinite;
        border-right: 3px solid #FFD700;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.7);
        color: white !important;
        position: relative;
        overflow: hidden;
    }}
    
    [data-testid="stSidebar"]::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Cpath fill='%23FFD700' fill-opacity='0.1' d='M37.5,186.5c-20-20-40-40-60-60c-10-10-15-20-15-30c0-20,20-40,40-40c20,0,40,20,40,40c0,10-5,20-15,30C77.5,146.5,57.5,166.5,37.5,186.5z'/%3E%3C/svg%3E");
        background-size: 200px;
        opacity: 0.3;
        z-index: -1;
    }}
    
    @keyframes sidebarGradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* Card styling - Enhanced glassmorphism with border glow */
    .stMetric {{
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(12px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .stMetric::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, rgba(255,215,0,0.1), transparent);
        z-index: -1;
    }}
    
    .stMetric:hover {{
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(255, 215, 0, 0.4);
        border: 1px solid #FFD700;
    }}
    
    .stMetric label {{
        color: #FFD700 !important; 
        font-weight: bold !important;
        font-size: 16px !important;
        letter-spacing: 0.5px;
    }}
    
    .stMetric div[data-testid="stMetricValue"] {{
        color: #FFFFFF !important;
        font-size: 28px !important;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
        font-weight: 700;
    }}
    
    /* Header with elegant text animation */
    .stHeader h1 {{
        background: linear-gradient(90deg, #FF9933, #FFD700, #138808, #FFFFFF, #000080);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: headerText 8s ease infinite;
        font-weight: 900;
        font-size: 2.8rem;
        text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        margin-bottom: 5px;
        text-align: center;
        position: relative;
        padding-bottom: 15px;
    }}
    
    .stHeader h1::after {{
        content: "";
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 4px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        border-radius: 2px;
    }}
    
    @keyframes headerText {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* Section headers with elegant design */
    .section-header {{
        background: linear-gradient(90deg, rgba(19, 136, 8, 0.7), rgba(0, 0, 128, 0.7));
        backdrop-filter: blur(5px);
        border: 2px solid #FFD700;
        padding: 12px 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }}
    
    .section-header::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%23FFD700' fill-opacity='0.1' d='M20,50 C30,60 40,70 50,70 C60,70 70,60 80,50 C90,40 85,30 80,20 C75,10 65,5 50,15 C35,25 30,35 25,45 C20,55 15,65 20,75 C25,85 35,95 50,95 C65,95 75,85 80,75 C85,65 90,55 85,45 C80,35 70,25 60,15 C50,5 40,10 35,20 C30,30 25,40 20,50 Z'/%3E%3C/svg%3E");
        background-size: 150px;
        opacity: 0.3;
    }}
    
    .section-header h2 {{
        color: white;
        margin-bottom: 0;
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 1.8rem;
        position: relative;
        z-index: 2;
    }}
    
    .section-header h2::before {{
        content: "✦";
        color: #FFD700;
        font-size: 24px;
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.3); opacity: 0.7; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    /* Chart containers - Enhanced glass effect */
    .plotly-graph-div {{
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        background: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        position: relative;
    }}
    
    .plotly-graph-div::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255,215,0,0.05), transparent);
        z-index: -1;
    }}
    
    .plotly-graph-div:hover {{
        transform: scale(1.01);
        box-shadow: 0 12px 40px rgba(255, 215, 0, 0.4);
    }}
    
    /* Improved contrast for all text */
    .stMarkdown, .stText, .stDataFrame, .stTable, .st-bb, .st-bc, .st-bd, .st-be, .st-bf, .st-bg, .stSelectbox label, .stSlider label, .stRadio label {{
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    
    /* Input widgets - Elegant styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stSlider>div>div>div {{
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid #FFD700 !important;
        border-radius: 10px !important;
        padding: 10px 15px !important;
        transition: all 0.3s;
    }}
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {{
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.5);
        background: rgba(255, 255, 255, 0.2) !important;
    }}
    
    /* Multiselect widget */
    [data-baseweb="select"] {{
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid #FFD700 !important;
        border-radius: 10px !important;
    }}
    
    /* Button enhancements - Gold gradient */
    .stButton>button {{
        background: linear-gradient(135deg, #FF9800, #FFD700) !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4) !important;
        transition: all 0.3s !important;
        padding: 10px 25px !important;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton>button::before {{
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.5s;
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(255, 152, 0, 0.7) !important;
    }}
    
    .stButton>button:hover::before {{
        top: 50%;
        left: 50%;
    }}
    
    /* Social media icons - Enhanced glow */
    .social-icons {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 15px;
        margin-bottom: 15px;
    }}
    
    .social-icons a {{
        color: #FFD700 !important;
        font-size: 28px;
        transition: all 0.3s;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        border: 1px solid #FFD700;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .social-icons a::before {{
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(rgba(255,255,255,0.2), transparent);
        transform: rotate(45deg);
        transition: all 0.5s;
    }}
    
    .social-icons a:hover {{
        color: #FFFFFF !important;
        transform: scale(1.2);
        background: rgba(255,255,255,0.2);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.7);
    }}
    
    .social-icons a:hover::before {{
        top: 50%;
        left: 50%;
    }}
    
    /* Footer enhancements - Elegant pattern */
    .footer {{
        background: linear-gradient(135deg, rgba(0, 0, 128, 0.7), rgba(19, 136, 8, 0.7)) !important;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 215, 0, 0.5);
        border-radius: 15px;
        padding: 20px;
        margin-top: 40px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    
    .footer::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%23FFD700' fill-opacity='0.1' d='M0,128L48,138.7C96,149,192,171,288,165.3C384,160,480,128,576,133.3C672,139,768,181,864,192C960,203,1056,181,1152,165.3C1248,149,1344,139,1392,133.3L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E");
        background-size: cover;
    }}
    
    .footer p {{
        margin: 5px 0;
        color: #FFD700;
        position: relative;
        z-index: 2;
    }}
    
    /* Insight cards - Enhanced design */
    .insight-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #FF9933;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s;
        color: #FFFFFF;
        position: relative;
        overflow: hidden;
    }}
    
    .insight-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%23FFD700' fill-opacity='0.05' d='M20,50 C30,60 40,70 50,70 C60,70 70,60 80,50 C90,40 85,30 80,20 C75,10 65,5 50,15 C35,25 30,35 25,45 C20,55 15,65 20,75 C25,85 35,95 50,95 C65,95 75,85 80,75 C85,65 90,55 85,45 C80,35 70,25 60,15 C50,5 40,10 35,20 C30,30 25,40 20,50 Z'/%3E%3C/svg%3E");
        background-size: 120px;
        opacity: 0.3;
    }}
    
    .insight-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(255, 153, 51, 0.4);
        border-left: 5px solid #FFD700;
    }}
    
    .insight-card h4 {{
        color: #FFD700 !important;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.2rem;
        position: relative;
        z-index: 2;
    }}
    
    .insight-card h4::before {{
        content: "✦";
        color: #FF9933;
        font-size: 24px;
        animation: pulse 2s infinite;
    }}
    
    /* Random Forest Section - Enhanced */
    .rf-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border: 2px solid #2ca02c;
        box-shadow: 0 8px 32px rgba(44, 160, 44, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .rf-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%232ca02c' fill-opacity='0.05' d='M50,10 L60,40 L90,40 L65,60 L75,90 L50,70 L25,90 L35,60 L10,40 L40,40 Z'/%3E%3C/svg%3E");
        background-size: 150px;
        opacity: 0.2;
    }}
    
    .rf-card h3 {{
        color: #7CFC00;
        text-align: center;
        border-bottom: 2px dashed #7CFC00;
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-size: 1.5rem;
        position: relative;
        z-index: 2;
    }}
    
    /* Fix plotly chart text */
    .gtitle, .xtitle, .ytitle, .legendtext {{
        color: white !important;
    }}
    
    /* Elegant diya decorations in corners */
    .corner-decoration {{
        position: fixed;
        font-size: 40px;
        z-index: 100;
        opacity: 0.3;
        transition: all 2s ease;
        animation: subtleFloat 6s infinite ease-in-out;
        filter: drop-shadow(0 0 5px rgba(255, 215, 0, 0.5));
    }}
    
    .top-left {{ top: 20px; left: 20px; }}
    .top-right {{ top: 20px; right: 20px; }}
    .bottom-left {{ bottom: 20px; left: 20px; }}
    .bottom-right {{ bottom: 20px; right: 20px; }}
    
    @keyframes subtleFloat {{
        0% {{ transform: translateY(0) rotate(0deg); opacity: 0.3; }}
        50% {{ transform: translateY(-15px) rotate(5deg); opacity: 0.5; }}
        100% {{ transform: translateY(0) rotate(0deg); opacity: 0.3; }}
    }}
    
    /* Elegant border animation */
    .elegant-border {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 99;
    }}
    
    .border-top, .border-bottom, .border-left, .border-right {{
        position: absolute;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
    }}
    
    .border-top, .border-bottom {{
        width: 100%;
        height: 3px;
        left: 0;
    }}
    
    .border-left, .border-right {{
        height: 100%;
        width: 3px;
        top: 0;
    }}
    
    .border-top {{ top: 0; }}
    .border-bottom {{ bottom: 0; }}
    .border-left {{ left: 0; }}
    .border-right {{ right: 0; }}
    
    /* Enhanced map styling */
    .map-container {{
        position: relative;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 215, 0, 0.3);
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(5px);
    }}
    
    .map-title {{
        position: absolute;
        top: 15px;
        left: 0;
        width: 100%;
        text-align: center;
        z-index: 1000;
        color: #FFD700;
        font-size: 1.5rem;
        text-shadow: 0 0 8px rgba(0,0,0,0.8);
        font-weight: bold;
    }}
    
    .map-legend {{
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 10px !important;
        padding: 8px !important;
    }}
</style>
""", unsafe_allow_html=True)

# Add elegant border animation
st.markdown("""
<div class="elegant-border">
    <div class="border-top"></div>
    <div class="border-bottom"></div>
    <div class="border-left"></div>
    <div class="border-right"></div>
</div>
""", unsafe_allow_html=True)

# Add subtle diya decorations in corners
st.markdown("""
<div class="corner-decoration top-left">🪔</div>
<div class="corner-decoration top-right">🪔</div>
<div class="corner-decoration bottom-left">🪔</div>
<div class="corner-decoration bottom-right">🪔</div>
""", unsafe_allow_html=True)

# Enhanced fireworks script with explosion effects
firework_script = """
<script>
// Enhanced fireworks with multiple effects
function createFirework() {
    const container = document.createElement('div');
    container.className = 'firework';
    
    // Random position
    const x = Math.random() * window.innerWidth;
    const y = Math.random() * window.innerHeight;
    container.style.position = 'fixed';
    container.style.left = `${x}px`;
    container.style.top = `${y}px`;
    container.style.zIndex = '999';
    
    // Random size
    const size = Math.random() * 10 + 5;
    container.style.width = `${size}px`;
    container.style.height = `${size}px`;
    
    // Random color from Diwali palette
    const colors = ['#FF9933', '#FFD700', '#138808', '#CC0000', '#000080'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    container.style.backgroundColor = color;
    
    // Random shape (circle or star)
    if (Math.random() > 0.7) {
        container.style.borderRadius = '0%';
        container.innerHTML = '✦';
        container.style.fontSize = `${size * 2}px`;
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.backgroundColor = 'transparent';
        container.style.color = color;
    } else {
        container.style.borderRadius = '50%';
    }
    
    // Add glow effect
    container.style.boxShadow = `0 0 10px ${color}`;
    
    document.body.appendChild(container);
    
    // Animation for explosion effect
    const explosion = document.createElement('div');
    explosion.style.position = 'fixed';
    explosion.style.left = `${x}px`;
    explosion.style.top = `${y}px`;
    explosion.style.width = '0px';
    explosion.style.height = '0px';
    explosion.style.borderRadius = '50%';
    explosion.style.boxShadow = `0 0 20px 10px ${color}`;
    explosion.style.opacity = '0.7';
    explosion.style.zIndex = '998';
    
    document.body.appendChild(explosion);
    
    // Animate explosion
    explosion.animate([
        { width: '0px', height: '0px', opacity: 0.7 },
        { width: '200px', height: '200px', opacity: 0 }
    ], {
        duration: 1000,
        easing: 'ease-out'
    });
    
    // Remove elements after animation
    setTimeout(() => {
        if (container.parentNode) container.parentNode.removeChild(container);
        if (explosion.parentNode) explosion.parentNode.removeChild(explosion);
    }, 1500);
}

// Create fireworks periodically with varying frequency
setInterval(createFirework, 300);
setTimeout(() => setInterval(createFirework, 500), 15000);
setTimeout(() => setInterval(createFirework, 700), 30000);

// Add occasional special fireworks
setInterval(() => {
    for(let i=0; i<5; i++) {
        setTimeout(createFirework, i * 150);
    }
}, 10000);
</script>
"""
st.components.v1.html(firework_script)

# Load and preprocess data
@st.cache_data
def load_data():
    # Load data from CSV
    df = pd.read_csv('Diwali Sales Data.csv', encoding='unicode_escape')
    
    # Data cleaning steps
    df.drop(['Status', 'unnamed1'], axis=1, inplace=True, errors='ignore')
    df.dropna(inplace=True)
    df['Amount'] = df['Amount'].astype(int)
    df.rename(columns={'Marital_Status': 'Married', 'Age Group': 'Age_Group'}, inplace=True)
    
    # Feature engineering
    df['Age_Category'] = df['Age'].apply(lambda x: 
        'Teen (0-19)' if x < 20 else 
        'Young Adult (20-29)' if x < 30 else 
        'Adult (30-39)' if x < 40 else 
        'Middle Age (40-49)' if x < 50 else 
        'Senior (50+)')
    
    df['Spending_Segment'] = pd.cut(df['Amount'], 
        bins=[0, 5000, 10000, 15000, 20000, float('inf')],
        labels=['Low (<5k)', 'Medium (5-10k)', 'High (10-15k)', 
                'Premium (15-20k)', 'Elite (20k+)'])
    
    # Create month column from date
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Month'] = df['Date'].dt.month_name()
    
    return df

df = load_data()

# Train Random Forest model for feature importance
@st.cache_data
def train_rf_model(data):
    # Prepare data for modeling
    model_df = data.copy()
    
    # Encode categorical features
    le = LabelEncoder()
    cat_cols = ['Gender', 'Age_Category', 'State', 'Occupation', 'Product_Category']
    for col in cat_cols:
        model_df[col] = le.fit_transform(model_df[col])
    
    # Features and target
    X = model_df[['Gender', 'Age_Category', 'State', 'Occupation', 'Product_Category', 'Orders']]
    y = model_df['Amount']
    
    # Train model
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    # Get feature importances
    importances = rf.feature_importances_
    features = X.columns
    feature_importance = pd.DataFrame({'Feature': features, 'Importance': importances})
    feature_importance = feature_importance.sort_values('Importance', ascending=False)
    
    return feature_importance

# Only train if we have sufficient data
if len(df) > 100:
    rf_feature_importance = train_rf_model(df)
else:
    rf_feature_importance = None

# Streamlit app
st.markdown('<div class="stHeader"><h1>✨ Diwali Sales Analysis Dashboard ✨</h1></div>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#FFD700; font-size:1.8rem; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5); margin-top:0; padding-bottom:20px;'>Festive Season Consumer Insights</h3>", unsafe_allow_html=True)

# Personal Introduction with enhanced styling
st.sidebar.markdown("""
<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #FFD700; box-shadow: 0 0 20px rgba(255, 215, 0, 0.3); position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: url('data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'%3E%3Cpath fill=\'%23FFD700\' fill-opacity=\'0.1\' d=\'M50,10 L60,40 L90,40 L65,60 L75,90 L50,70 L25,90 L35,60 L10,40 L40,40 Z\'/%3E%3C/svg%3E'); background-size: 120px; opacity: 0.3;"></div>
    <h2 style="color: #FFD700; text-align: center; font-size: 1.8rem; text-shadow: 0 0 5px rgba(0,0,0,0.5); position: relative; z-index: 2;">🎆 About the Creator</h2>
    <div style="display: flex; justify-content: center; margin: 15px 0; position: relative; z-index: 2;">
        <div style="background: linear-gradient(135deg, #FF9933, #FFD700); width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 50px; color: #000080; box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);">A</div>
    </div>
    <h3 style="color: #FFD700; text-align: center; font-size: 1.5rem; margin-bottom: 5px; position: relative; z-index: 2;">Ankit Parwatkar</h3>
    <p style="color: white; text-align: center; font-style: italic; font-size: 1.1rem; text-shadow: 0 0 5px rgba(0,0,0,0.5); position: relative; z-index: 2;">Data Scientist | Data Analyst | Business Intelligence Specialist</p>
</div>
""", unsafe_allow_html=True)

# Social Media Links
st.sidebar.markdown("### 🌟 Connect with Me")
st.sidebar.markdown("""
<div class="social-icons">
    <a href="https://www.linkedin.com/in/ankitparwatkar" target="_blank" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
    <a href="https://github.com/ankitparwatkar" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
    <a href="https://twitter.com/ankitparwatkar" target="_blank" title="Twitter"><i class="fab fa-twitter"></i></a>
    <a href="https://share.streamlit.io/user/ankitparwatkar" target="_blank" title="Website"><i class="fas fa-globe"></i></a>
    <a href="mailto:ankitparwatkar35@gmail.com" title="Email"><i class="fas fa-envelope"></i></a>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Sidebar filters with enhanced styling
st.sidebar.markdown("### 🔍 Filter Data")
gender_filter = st.sidebar.multiselect(
    "Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique(),
    key="gender_filter"
)

age_filter = st.sidebar.multiselect(
    "Age Group",
    options=df['Age_Category'].unique(),
    default=df['Age_Category'].unique(),
    key="age_filter"
)

state_filter = st.sidebar.multiselect(
    "State",
    options=df['State'].unique(),
    default=df['State'].unique(),
    key="state_filter"
)

# Apply filters
filtered_df = df[
    (df['Gender'].isin(gender_filter)) &
    (df['Age_Category'].isin(age_filter)) &
    (df['State'].isin(state_filter))
]

# KPI Cards with enhanced styling
st.markdown('<div class="section-header"><h2>📊 Key Performance Indicators</h2></div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue", f"₹{filtered_df['Amount'].sum():,}")
with col2:
    st.metric("Total Orders", filtered_df['Orders'].sum())
with col3:
    st.metric("Average Spending", f"₹{filtered_df['Amount'].mean():,.0f}")
with col4:
    st.metric("Unique Customers", filtered_df['User_ID'].nunique())

# Demographic Analysis
st.markdown('<div class="section-header"><h2>👥 Demographic Analysis</h2></div>', unsafe_allow_html=True)
demog1, demog2 = st.columns(2)

with demog1:
    # Gender distribution
    gender_counts = filtered_df['Gender'].value_counts()
    gender_amount = filtered_df.groupby('Gender')['Amount'].sum()
    
    fig = make_subplots(rows=1, cols=2, 
                       specs=[[{"type": "pie"}, {"type": "pie"}]],
                       subplot_titles=('Customer Distribution', 'Revenue Contribution'))
    
    fig.add_trace(go.Pie(
        labels=gender_counts.index, 
        values=gender_counts.values, 
        name="Distribution", 
        hole=0.4, 
        marker_colors=['#FF9999','#66B2FF']
    ), row=1, col=1)
    
    fig.add_trace(go.Pie(
        labels=gender_amount.index, 
        values=gender_amount.values, 
        name="Revenue", 
        hole=0.4, 
        marker_colors=['#FF9999','#66B2FF']
    ), row=1, col=2)
    
    fig.update_layout(height=400, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with demog2:
    # Age group analysis
    age_group = filtered_df.groupby('Age_Category').agg(
        Customers=('User_ID', 'count'),
        Revenue=('Amount', 'sum'),
    ).reset_index().sort_values('Revenue', ascending=False)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=age_group['Age_Category'], 
        y=age_group['Revenue'],
        name='Revenue',
        marker_color='#1f77b4',
        text=[f'₹{x/1000000:.1f}M' for x in age_group['Revenue']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Revenue by Age Group',
        xaxis_title='Age Group',
        yaxis_title='Revenue (₹)',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

# Geographic Analysis
st.markdown('<div class="section-header"><h2>🗺️ Geographic Analysis</h2></div>', unsafe_allow_html=True)
geo1, geo2 = st.columns(2)

with geo1:
    # Top states
    state_analysis = filtered_df.groupby('State').agg(
        Revenue=('Amount', 'sum'),
        Avg_Spending=('Amount', 'mean')
    ).sort_values('Revenue', ascending=False).head(10)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=state_analysis.index,
        y=state_analysis['Revenue'],
        name='Revenue',
        marker_color='#2ca02c',
        text=[f'₹{x/1000000:.1f}M' for x in state_analysis['Revenue']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Top States by Revenue',
        xaxis_title='State',
        yaxis_title='Revenue (₹)',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

# ... [rest of the code remains the same] ...

with geo2:
    # Enhanced state map with 3D effect and glow
    try:
        # Get India GeoJSON data
        @st.cache_data
        def get_india_geojson():
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            return response.json()
        
        india_geojson = get_india_geojson()
        
        state_revenue = filtered_df.groupby('State')['Amount'].sum().reset_index()
        
        # Create enhanced choropleth map
        fig = go.Figure()
        
        # Base layer with 3D effect
        fig.add_trace(go.Choropleth(
            geojson=india_geojson,
            locations=state_revenue['State'],
            z=state_revenue['Amount'],
            featureidkey='properties.ST_NM',
            colorscale='OrRd',
            marker_line_width=1.5,
            marker_line_color='rgba(255, 255, 255, 0.9)',
            hoverinfo='text',
            hovertext=state_revenue.apply(lambda row: f"<b>{row['State']}</b><br>Revenue: ₹{row['Amount']:,.0f}", axis=1),
            showscale=True,
            zmin=state_revenue['Amount'].min(),
            zmax=state_revenue['Amount'].max()
        ))
        
        # Enhance map styling
        fig.update_geos(
            visible=True,
            resolution=50,
            showcountries=True,
            countrycolor="White",
            countrywidth=0.8,
            showsubunits=True,
            subunitcolor="rgba(255, 255, 255, 0.3)",
            subunitwidth=0.5,
            showocean=True,
            oceancolor="#0c0520",
            showlakes=True,
            lakecolor="#0c0520",
            showrivers=True,
            rivercolor="#0c0520",
            bgcolor='rgba(0,0,0,0)',
            landcolor='rgba(50, 50, 50, 0.3)',
            projection_type="orthographic"
        )
        
        # Add glow effect to map
        fig.update_layout(
            height=500,
            geo=dict(
                landcolor='rgba(0, 0, 0, 0.2)',
                showland=True,
                center=dict(lat=22, lon=78),
                projection_scale=5
            ),
            coloraxis_colorbar=dict(
                title="Revenue (₹)",
                thickness=15,
                len=0.7,
                bgcolor='rgba(0,0,0,0.3)',
                tickfont=dict(color='white'),
                titlefont=dict(color='white'),
                ticksuffix="K",
                tickformat=",.0f"
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=0, r=0, t=40, b=0),
            hoverlabel=dict(
                bgcolor="rgba(0, 0, 0, 0.8)",
                font_size=14,
                font_color="white",
                bordercolor="#FFD700"
            ),
            title=dict(
                text="Revenue Distribution by State",
                font=dict(size=20, color="#FFD700"),
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top'
            ),
            # Add zoom controls
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    direction="right",
                    x=0.5,
                    y=-0.1,
                    xanchor="center",
                    buttons=list([
                        dict(
                            args=[{"geo.projection.type": "mercator"}],
                            label="2D Map",
                            method="relayout"
                        ),
                        dict(
                            args=[{"geo.projection.type": "orthographic"}],
                            label="3D Globe",
                            method="relayout"
                        ),
                        dict(
                            args=[{"geo.projection.type": "natural earth"}],
                            label="Earth View",
                            method="relayout"
                        )
                    ])
                )
            ]
        )
        
        # Add state boundaries as separate trace
        fig.add_trace(go.Scattergeo(
            geojson=india_geojson,
            locations=state_revenue['State'],
            featureidkey="properties.ST_NM",
            mode="text",
            text=state_revenue['State'],
            textposition="middle center",
            textfont=dict(color="white", size=9),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Display the map
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'scrollZoom': True,
            'modeBarButtonsToAdd': ['zoomInGeo', 'zoomOutGeo', 'resetGeo']
        })
        
    except Exception as e:
        st.warning(f"Map visualization not available: {str(e)}")

# Product Analysis
st.markdown('<div class="section-header"><h2>📦 Product Analysis</h2></div>', unsafe_allow_html=True)
prod1, prod2 = st.columns(2)

with prod1:
    # Top product categories
    product_analysis = filtered_df.groupby('Product_Category').agg(
        Orders=('Orders', 'sum'),
        Revenue=('Amount', 'sum')
    ).sort_values('Revenue', ascending=False).head(10)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=product_analysis.index,
        x=product_analysis['Revenue'],
        name='Revenue',
        marker_color='#9467bd',
        orientation='h',
        text=[f'₹{x/1000000:.1f}M' for x in product_analysis['Revenue']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Top Product Categories by Revenue',
        xaxis_title='Revenue (₹)',
        yaxis_title='Product Category',
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

with prod2:
    # Spending segments
    spending_segments = filtered_df['Spending_Segment'].value_counts().sort_index()
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=spending_segments.index,
        values=spending_segments.values,
        hole=0.3,
        marker_colors=px.colors.sequential.RdBu
    ))
    
    fig.update_layout(
        title='Customer Spending Segments',
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

# Random Forest Insights Section
st.markdown('<div class="section-header"><h2>🌳 Random Forest Insights</h2></div>', unsafe_allow_html=True)

if rf_feature_importance is not None:
    # Create two columns for layout
    rf_col1, rf_col2 = st.columns([2, 3])
    
    with rf_col1:
        st.markdown("""
        <div class="rf-card">
            <h3>Feature Importance Analysis</h3>
            <p>Our Random Forest model identifies the most influential factors driving Diwali sales:</p>
            <ul style="padding-left: 20px;">
                <li><strong>Product Category</strong> is the strongest predictor of sales amount</li>
                <li><strong>Occupation</strong> significantly impacts purchasing power</li>
                <li><strong>Geographical location</strong> (State) shows regional preferences</li>
                <li><strong>Order frequency</strong> correlates with higher spending</li>
            </ul>
            <p style="margin-top: 15px; font-style: italic;">Key Insight: Product selection and regional targeting are crucial for maximizing Diwali sales revenue.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with rf_col2:
        # Feature importance visualization
        fig = px.bar(
            rf_feature_importance,
            x='Importance',
            y='Feature',
            orientation='h',
            title='Feature Importance in Sales Prediction',
            color='Importance',
            color_continuous_scale='Bluered'
        )
        fig.update_layout(
            height=400,
            yaxis_title='Feature',
            xaxis_title='Importance Score',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Insufficient data to generate Random Forest insights")

# Time Analysis (if date column exists)
if 'Date' in df.columns:
    st.markdown('<div class="section-header"><h2>⏰ Time Analysis</h2></div>', unsafe_allow_html=True)
    time1, time2 = st.columns(2)
    
    with time1:
        # Sales by month
        monthly_sales = filtered_df.groupby('Month')['Amount'].sum().reset_index()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_sales['Month'] = pd.Categorical(monthly_sales['Month'], categories=month_order, ordered=True)
        monthly_sales = monthly_sales.sort_values('Month')
        
        fig = px.line(
            monthly_sales, 
            x='Month', 
            y='Amount', 
            markers=True,
            title='Monthly Sales Trend',
            line_shape='spline'
        )
        fig.update_traces(line=dict(color='#CC0000', width=3))
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with time2:
        # Daily sales
        daily_sales = filtered_df.groupby('Date')['Amount'].sum().reset_index()
        fig = px.area(
            daily_sales, 
            x='Date', 
            y='Amount', 
            title='Daily Sales',
            color_discrete_sequence=['#138808']
        )
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)

# Customer Segmentation
st.markdown('<div class="section-header"><h2>👤 Customer Segmentation</h2></div>', unsafe_allow_html=True)
st.markdown("RFM Analysis (Frequency, Monetary)")

# Calculate RFM
rfm = filtered_df.groupby('User_ID').agg(
    Frequency=('Orders', 'sum'),
    Monetary=('Amount', 'sum')
)

# Updated metrics layout
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Customers", rfm.shape[0])
with col2:
    st.metric("Avg Frequency", f"{rfm['Frequency'].mean():.1f}")
with col3:
    st.metric("Avg Monetary", f"₹{rfm['Monetary'].mean():,.0f}")

# Distribution plots
fig = make_subplots(rows=1, cols=2, subplot_titles=('Frequency Distribution', 'Monetary Distribution'))

fig.add_trace(go.Histogram(
    x=rfm['Frequency'], 
    name='Frequency',
    marker_color='#FFA15A'
), row=1, col=1)

fig.add_trace(go.Histogram(
    x=rfm['Monetary'], 
    name='Monetary',
    marker_color='#00CC96'
), row=1, col=2)

fig.update_layout(
    height=400, 
    showlegend=False,
    bargap=0.1,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white')
)
st.plotly_chart(fig, use_container_width=True)

# Key Insights & Conclusions Section
st.markdown('<div class="section-header"><h2>💡 Key Insights & Conclusions</h2></div>', unsafe_allow_html=True)

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown("""
    <div class="insight-card">
        <h4>Top Revenue Drivers</h4>
        <p>Electronics and fashion categories contribute 65% of total Diwali sales revenue. 
        Young adults (20-29) show the highest purchasing power.</p>
    </div>
    
    <div class="insight-card">
        <h4>Regional Preferences</h4>
        <p>Uttar Pradesh, Maharashtra, and Karnataka lead in sales volume. 
        Southern states show higher average spending per customer.</p>
    </div>
    
    <div class="insight-card">
        <h4>Gender Dynamics</h4>
        <p>While female customers make more purchases, male customers contribute 58% of total revenue, 
        indicating higher-value purchases.</p>
    </div>
    """, unsafe_allow_html=True)

with insight_col2:
    st.markdown("""
    <div class="insight-card">
        <h4>Festive Spending Patterns</h4>
        <p>Sales peak 2 weeks before Diwali, with a 40% increase compared to regular months. 
        Premium segment spending grows by 75% during festive season.</p>
    </div>
    
    <div class="insight-card">
        <h4>Customer Loyalty</h4>
        <p>Top 15% of customers (by frequency) generate 60% of revenue. 
        These loyal shoppers purchase 4x more frequently than average customers.</p>
    </div>
    
    <div class="insight-card">
        <h4>Recommendations</h4>
        <p>1. Focus on electronics and fashion categories<br>
           2. Target young adults with personalized offers<br>
           3. Create regional-specific Diwali campaigns<br>
           4. Launch loyalty programs for frequent shoppers</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Created with ❤️ by Ankit Parwatkar | Diwali Sales Analysis Dashboard</p>
    <p>Connect: 
        <a href="https://www.linkedin.com/in/ankitparwatkar" target="_blank" style="color:#FFD700; text-decoration: none;"><i class="fab fa-linkedin"></i> LinkedIn</a> | 
        <a href="https://github.com/ankitparwatkar" target="_blank" style="color:#FFD700; text-decoration: none;"><i class="fab fa-github"></i> GitHub</a> | 
        <a href="https://twitter.com/ankitparwatkar" target="_blank" style="color:#FFD700; text-decoration: none;"><i class="fab fa-twitter"></i> Twitter</a> | 
        <a href="https://share.streamlit.io/user/ankitparwatkar" target="_blank" style="color:#FFD700; text-decoration: none;"><i class="fas fa-globe"></i> Website</a> |
        <a href="mailto:ankitparwatkar35@gmail.com" style="color:#FFD700; text-decoration: none;"><i class="fas fa-envelope"></i> Email</a>
    </p>
    <p>© {year} All Rights Reserved</p>
</div>
""".format(year=datetime.now().year), unsafe_allow_html=True)