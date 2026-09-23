import streamlit as st
from pathlib import Path
import json

from src.sidebar_style import apply_sidebar_style

apply_sidebar_style()


# ============================================================
# DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CATALOG_FILE = BASE_DIR / "jewelry_catalog.json"


def load_catalog():
    if not CATALOG_FILE.exists():
        return []

    try:
        with open(CATALOG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


catalog = load_catalog()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #080a0f;
}

.main .block-container {
    max-width: 1400px;
    padding-top: 0.5rem;
    padding-bottom: 3rem;
}

.hero {
    text-align: center;
    padding: 0 10px;
    margin-top: -30px;
}

.hero h1 {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    color: #9ca3af;
    font-size: 1.2rem;
}

.status {
    display: inline-block;
    background: #103c29;
    color: #4ade80;
    padding: 10px 20px;
    border-radius: 30px;
    font-weight: 700;
    margin-top: 15px;
}

.card {
    background: #10131a;
    border: 1px solid #282e39;
    border-radius: 16px;
    padding: 25px;
    min-height: 180px;
}

.card-icon {
    font-size: 2.3rem;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 12px;
}

.card-text {
    color: #9ca3af;
    line-height: 1.6;
}

.tech {
    text-align: center;
    background: #10131a;
    border: 1px solid #282e39;
    border-radius: 14px;
    padding: 20px;
}

@media (max-width: 768px) {

    .main .block-container {
        padding: 1rem;
    }

    .hero h1 {
        font-size: 2.3rem;
    }

    .hero p {
        font-size: 1rem;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">
    <div style="font-size:4.5rem;">💎</div>
    <h1>JewelVision AI</h1>
    <p>AI-Powered Jewelry Visual Search Platform</p>
    <div class="status">● AI ENGINE ONLINE</div>
</div>
""",
    unsafe_allow_html=True,
)


st.divider()


# ============================================================
# INTRO
# ============================================================

st.title("Intelligent Jewelry Discovery")

st.write(
    "Upload a jewelry image and discover visually similar "
    "designs from your jewelry collection using AI."
)


st.write("")


# ============================================================
# FEATURES
# ============================================================

col1, col2, col3 = st.columns(3, gap="large")


with col1:
    st.markdown(
        """
<div class="card">
    <div class="card-icon">🔎</div>
    <div class="card-title">Visual Search</div>
    <div class="card-text">
        Upload a jewelry image and find visually similar
        designs using AI-powered image search.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


with col2:
    st.markdown(
        """
<div class="card">
    <div class="card-icon">✨</div>
    <div class="card-title">Add Jewelry</div>
    <div class="card-text">
        Register new jewelry designs with images,
        categories, subtypes and collection details.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


with col3:
    st.markdown(
        """
<div class="card">
    <div class="card-icon">📦</div>
    <div class="card-title">Jewelry Catalog</div>
    <div class="card-text">
        Browse and filter all registered jewelry
        designs in one organized catalog.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# COLLECTION OVERVIEW
# ============================================================

st.write("")
st.write("")

st.subheader("Collection Overview")

total = len(catalog)

gold = sum(
    1
    for item in catalog
    if item.get("collection") == "Gold"
)

prototype = sum(
    1
    for item in catalog
    if item.get("collection") == "Prototype"
)

female = sum(
    1
    for item in catalog
    if item.get("gender") == "Female"
)


m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Total Designs", total)

with m2:
    st.metric("Gold Collection", gold)

with m3:
    st.metric("Prototype Collection", prototype)

with m4:
    st.metric("Female Designs", female)


# ============================================================
# TECHNOLOGY
# ============================================================

st.write("")
st.write("")

st.subheader("AI Technology")

tech1, tech2, tech3 = st.columns(3, gap="large")


with tech1:
    st.markdown(
        """
<div class="tech">
    🧠<br><br>
    <b>DINOv2</b><br>
    Visual Feature Extraction
</div>
""",
        unsafe_allow_html=True,
    )


with tech2:
    st.markdown(
        """
<div class="tech">
    ⚡<br><br>
    <b>FAISS</b><br>
    Fast Similarity Search
</div>
""",
        unsafe_allow_html=True,
    )


with tech3:
    st.markdown(
        """
<div class="tech">
    🐍<br><br>
    <b>Python + Streamlit</b><br>
    AI Application Platform
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.divider()

st.caption(
    "💎 JewelVision AI • Intelligent Jewelry Visual Search • Demo"
)