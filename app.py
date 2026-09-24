import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="JewelVision AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
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


# ============================================================
# CREATE NAVIGATION
# ============================================================

pg = st.navigation(
    [
        home,
        visual_search,
        add_jewelry,
        catalog,
    ]
)


# ============================================================
# RUN CURRENT PAGE
# ============================================================

pg.run()