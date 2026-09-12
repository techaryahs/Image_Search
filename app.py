from pathlib import Path
import streamlit as st
from PIL import Image

from src.config import (
    GOLD_INDEX_FILE,
    PROTOTYPE_INDEX_FILE,
    SIMILARITY_THRESHOLD,
    TOP_K,
)
from src.build_index import build_all_indexes
from src.search import BidirectionalJewelrySearch


# --------------------------------------------------
# Page Configuration & CSS Styling
# --------------------------------------------------

st.set_page_config(
    page_title="AI Jewelry Visual Search",
    page_icon="💎",
    layout="wide"
)

# Custom CSS for polished product UI
st.markdown(
    """
    <style>
    /* Card Container Styling */
    .top-match-card {
        border: 2px solid #D4AF37;
        border-radius: 12px;
        padding: 20px;
        background-color: rgba(212, 175, 55, 0.05);
        margin-bottom: 25px;
    }
    .badge-top-match {
        background-color: #D4AF37;
        color: #000000;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 10px;
    }
    .badge-rank {
        background-color: #333333;
        color: #ffffff;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Automatic Index Validation
# --------------------------------------------------

if not GOLD_INDEX_FILE.exists() or not PROTOTYPE_INDEX_FILE.exists():
    st.error(
        "Search index not found. Please run:\n"
        "`python -m src.build_index`"
    )
    st.stop()


# --------------------------------------------------
# Load Search Engine (Cached)
# --------------------------------------------------

@st.cache_resource
def load_search_engine():
    return BidirectionalJewelrySearch()


# --------------------------------------------------
# Modal Dialog Image Viewer
# --------------------------------------------------

@st.dialog("🔍 Image Viewer", width="large")
def open_image_viewer(image_path: str, rank: int, similarity: float, item_name: str, search_mode: str):
    st.markdown(f"### `{item_name}`")
    img_p = Path(image_path)
    if img_p.exists():
        img = Image.open(img_p).convert("RGB")
        st.image(img, use_container_width=True)
    else:
        st.error("Image file missing")

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Rank:** #{rank}")
        st.markdown(f"**Search Direction:** {search_mode}")
    with c2:
        st.markdown(f"**Visual Similarity Score:** `{similarity:.4f}`")

    score_norm = max(0.0, min(float(similarity), 1.0))
    st.progress(score_norm)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("AI Jewelry Visual Search")
st.write(
    "Upload a jewelry image to perform bidirectional visual search "
    "between Prototype design concepts and Gold products."
)

st.divider()


# --------------------------------------------------
# Sidebar Settings & Index Rebuild
# --------------------------------------------------

st.sidebar.header("Search Settings")

top_k = st.sidebar.slider(
    "Number of results",
    min_value=1,
    max_value=5,
    value=TOP_K
)

st.sidebar.divider()
st.sidebar.header("Index Management")

if st.sidebar.button("🔨 Rebuild Search Index", use_container_width=True):
    with st.spinner("Rebuilding Gold and Prototype FAISS search indexes..."):
        build_all_indexes()
        st.cache_resource.clear()
        st.session_state.pop("search_results", None)
        st.sidebar.success("Search indexes rebuilt successfully!")


# --------------------------------------------------
# Search Mode Selection
# --------------------------------------------------

search_mode = st.radio(
    "Search Mode:",
    options=["Prototype → Gold", "Gold → Prototype"],
    index=0,
    horizontal=True
)

if search_mode == "Prototype → Gold":
    upload_label = "Upload Prototype Image"
    button_label = "Find Matching Gold Designs"
    target_label = "Gold Product"
    results_title = "Matching Gold Designs"
    top_match_header = "Top Match — Most Similar Gold Product"
    other_matches_header = "Other Matching Gold Products"
else:
    upload_label = "Upload Gold Image"
    button_label = "Find Matching Prototype Designs"
    target_label = "Prototype Concept"
    results_title = "Matching Prototype Designs"
    top_match_header = "Top Match — Most Similar Prototype"
    other_matches_header = "Other Matching Prototypes"


# --------------------------------------------------
# File Upload & Query Display
# --------------------------------------------------

uploaded_file = st.file_uploader(
    upload_label,
    type=["jpg", "jpeg", "png", "webp", "bmp"]
)

if uploaded_file is not None:
    query_image = Image.open(uploaded_file).convert("RGB")
    query_filename = uploaded_file.name

    st.subheader("Query Image")

    q_col1, q_col2 = st.columns([1, 2])

    with q_col1:
        st.image(
            query_image,
            caption=f"Uploaded Query ({query_filename})",
            use_container_width=True
        )

    with q_col2:
        st.info(
            f"**Search Direction:** `{search_mode}`\n\n"
            f"**Query File:** `{query_filename}`\n\n"
            f"The AI will search the target **{target_label}** FAISS vector index using DINOv2 1536-D features."
        )

    # Search Execution Trigger
    if st.button(f"🔎 {button_label}", type="primary"):
        with st.spinner(f"Extracting features and searching {target_label} catalog..."):
            search_engine = load_search_engine()

            if search_mode == "Prototype → Gold":
                raw_results = search_engine.search_gold(query_image, top_k=top_k)
            else:
                raw_results = search_engine.search_prototype(query_image, top_k=top_k)

            # Ensure results are sorted descending by similarity score
            sorted_results = sorted(raw_results, key=lambda x: x["similarity"], reverse=True)

            # Store in session state to persist state across interactions
            st.session_state["search_results"] = sorted_results
            st.session_state["query_filename"] = query_filename
            st.session_state["current_mode"] = search_mode


# --------------------------------------------------
# Render Results (If available in session state)
# --------------------------------------------------

if "search_results" in st.session_state and st.session_state.get("search_results"):
    results = st.session_state["search_results"]
    q_file = st.session_state.get("query_filename", "")
    curr_mode = st.session_state.get("current_mode", search_mode)

    st.divider()
    st.header(results_title)
    st.caption(
        f"**Search Direction:** {curr_mode} | "
        f"**Query File:** `{q_file}` | "
        f"**Results Displayed:** {len(results)}"
    )

    top_score = results[0]["similarity"] if results else 0.0
    if top_score < SIMILARITY_THRESHOLD:
        st.info("No strong visual match found. Showing closest candidates.")

    # --------------------------------------------------
    # 1. TOP MATCH SECTION (RANK #1 - PROMINENT & LARGE)
    # --------------------------------------------------
    top_result = results[0]
    top_path = Path(top_result["image_path"])

    st.subheader(top_match_header)

    with st.container():
        st.markdown('<div class="top-match-card">', unsafe_allow_html=True)

        top_col1, top_col2 = st.columns([2, 1])

        with top_col1:
            if top_path.exists():
                top_img = Image.open(top_path).convert("RGB")
                st.image(top_img, caption=f"Rank #1 — {top_path.name}", use_container_width=True)
            else:
                st.error("Top match image file not found.")

        with top_col2:
            st.markdown('<span class="badge-top-match">★ HIGHEST MATCH</span>', unsafe_allow_html=True)
            st.markdown("### Rank #1")
            st.markdown(f"**Item Name:** `{top_path.name}`")
            st.markdown(f"**Visual Similarity Score:** `{top_result['similarity']:.4f}`")

            # Score Progress bar
            score_norm = max(0.0, min(float(top_result["similarity"]), 1.0))
            st.progress(score_norm)

            st.write("")
            if st.button("🔍 View Large Image", key="btn_top_match", type="secondary", use_container_width=True):
                open_image_viewer(
                    image_path=top_result["image_path"],
                    rank=1,
                    similarity=top_result["similarity"],
                    item_name=top_path.name,
                    search_mode=curr_mode
                )

        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------
    # 2. OTHER MATCHES SECTION (RANKS #2 to #K)
    # --------------------------------------------------
    other_results = results[1:]

    if other_results:
        st.subheader(other_matches_header)

        # Responsive grid layout
        num_cols = min(len(other_results), 4)
        columns = st.columns(num_cols)

        for idx, res in enumerate(other_results, start=2):
            col_idx = (idx - 2) % num_cols
            res_path = Path(res["image_path"])

            with columns[col_idx]:
                with st.container(border=True):
                    if res_path.exists():
                        res_img = Image.open(res_path).convert("RGB")
                        st.image(res_img, use_container_width=True)
                    else:
                        st.warning("Image missing")

                    st.markdown(f"**Rank #{idx}**")
                    st.caption(f"`{res_path.name}`")
                    st.write(f"**Score:** `{res['similarity']:.4f}`")

                    # View button to open modal dialog
                    if st.button(f"🔍 View", key=f"btn_rank_{idx}", use_container_width=True):
                        open_image_viewer(
                            image_path=res["image_path"],
                            rank=idx,
                            similarity=res["similarity"],
                            item_name=res_path.name,
                            search_mode=curr_mode
                        )
