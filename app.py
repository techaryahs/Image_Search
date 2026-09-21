import streamlit as st


st.set_page_config(
    page_title="JewelVision AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #080a0f;
        color: #f5f5f5;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #ffffff !important;
    }

    .hero {
        padding: 60px 20px 40px 20px;
        text-align: center;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        color: #9ca3af;
        margin-bottom: 30px;
    }

    .status {
        display: inline-block;
        padding: 10px 20px;
        border-radius: 30px;
        background: #103c29;
        color: #4ade80;
        font-weight: 700;
    }

    .feature-card {
        background: #10131a;
        border: 1px solid #282e39;
        border-radius: 16px;
        padding: 25px;
        min-height: 180px;
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 15px;
    }

    .feature-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 8px;
    }

    .feature-text {
        color: #9ca3af;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION
# ============================================================

home = st.Page(
    "pages/0_Home.py",
    title="Home",
    icon="💎",
)

visual_search = st.Page(
    "pages/1_Visual_Search.py",
    title="Visual Search",
    icon="🔎",
)

add_jewelry = st.Page(
    "pages/2_Add_Jewelry.py",
    title="Add Jewelry",
    icon="✨",
)

catalog = st.Page(
    "pages/3_Jewelry_Catalog.py",
    title="Jewelry Catalog",
    icon="📦",
)


pg = st.navigation(
    [
        home,
        visual_search,
        add_jewelry,
        catalog,
    ]
)


# ============================================================
# RUN SELECTED PAGE
# ============================================================

pg.run()