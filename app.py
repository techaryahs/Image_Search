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

    /* =============================================
       BASE
       ============================================= */

    .stApp {
        background: #080a0f;
        color: #f0f0f0;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* =============================================
       HEADINGS — bright white on all screens
       ============================================= */

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    /* =============================================
       BODY TEXT — high contrast
       ============================================= */

    p, span, div, li {
        color: #e8e8e8;
    }

    /* =============================================
       METRIC CARDS — fix dim label + value on mobile
       ============================================= */

    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] span,
    [data-testid="stMetricLabel"] {
        color: #d0d0d0 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }

    /* =============================================
       FORM LABELS — visible on mobile
       ============================================= */

    label, .stTextInput label, .stSelectbox label,
    .stTextArea label, .stFileUploader label,
    .stSlider label, .stRadio label,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span {
        color: #e0e0e0 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }

    /* =============================================
       CAPTION / HELPER TEXT — readable but softer
       ============================================= */

    [data-testid="stCaptionContainer"] p,
    .stCaption, small {
        color: #b0b8c8 !important;
        font-size: 0.85rem !important;
    }

    /* =============================================
       RADIO BUTTONS — label text visible
       ============================================= */

    div[role="radiogroup"] label p,
    div[role="radiogroup"] label span {
        color: #e8e8e8 !important;
        font-size: 1rem !important;
    }

    /* =============================================
       SLIDER — label and value
       ============================================= */

    [data-testid="stSlider"] p,
    [data-testid="stSlider"] span {
        color: #e0e0e0 !important;
    }

    /* =============================================
       SELECT / INPUT — text inside widgets
       ============================================= */

    .stSelectbox div[data-baseweb="select"] span,
    .stTextInput input,
    .stTextArea textarea {
        color: #f0f0f0 !important;
    }

    /* =============================================
       BUTTONS
       ============================================= */

    .stButton > button {
        min-height: 48px;
        border-radius: 10px;
        border: 1px solid #353a45;
        background: #15181f;
        color: #ffffff !important;
        font-weight: 700;
        font-size: 1rem;
    }

    .stButton > button:hover {
        border-color: #caa55c;
        color: #e3c57d !important;
    }

    /* =============================================
       SUCCESS / WARNING / INFO BANNERS
       ============================================= */

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* =============================================
       MOBILE SPECIFIC
       ============================================= */

    @media (max-width: 768px) {

        .main .block-container {
            padding: 0.8rem 1rem 3rem;
        }

        h1 {
            font-size: 1.8rem !important;
        }

        h2 {
            font-size: 1.4rem !important;
        }

        h3 {
            font-size: 1.2rem !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.6rem !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.85rem !important;
        }

        label,
        [data-testid="stWidgetLabel"] p {
            font-size: 0.9rem !important;
        }

        .stButton > button {
            font-size: 0.95rem;
            padding: 0.6rem 1rem;
        }
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