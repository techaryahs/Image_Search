from pathlib import Path
import json
import streamlit as st
from PIL import Image

from src.config import (
    GOLD_INDEX_FILE,
    PROTOTYPE_INDEX_FILE,
    SIMILARITY_THRESHOLD,
    TOP_K,
)
from src.search import BidirectionalJewelrySearch
from src.sidebar_style import apply_sidebar_style

apply_sidebar_style()

CATALOG_FILE = Path(__file__).resolve().parent.parent / "jewelry_catalog.json"


def get_jewelry_details(image_path):
    if not CATALOG_FILE.exists():
        return None

    try:
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            catalog = json.load(f)

        image_path = str(Path(image_path).as_posix())

        for item in catalog:
            catalog_image = str(
                Path(item.get("image", "")).as_posix()
            )

            if Path(catalog_image).name == Path(image_path).name:
                return item

    except Exception:
        return None

    return None

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Visual Search | JewelVision AI",
    page_icon="🔎",
    layout="wide",
)

apply_sidebar_style()
# ============================================================
# FUNCTIONS
# ============================================================

def indexes_exist():
    return (
        GOLD_INDEX_FILE.exists()
        and PROTOTYPE_INDEX_FILE.exists()
    )


@st.cache_resource
def load_search_engine():
    return BidirectionalJewelrySearch()


# ============================================================
# PAGE STYLING
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(211, 174, 96, 0.06),
                transparent 25%
            ),
            #08090d;
    }

        /* PROFESSIONAL SIDEBAR */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #171b27 0%,
            #10131d 100%
        );
        border-right: 1px solid #292e3a;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

        /* SIDEBAR MENU */

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
        border-radius: 10px;
        margin: 4px 8px;
        padding: 10px 12px;
        color: #d8dbe3;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
        background: rgba(225, 192, 113, 0.10);
        color: #e1c071;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(
            90deg,
            rgba(225, 192, 113, 0.20),
            rgba(225, 192, 113, 0.06)
        );
        color: #e1c071;
        border-left: 3px solid #e1c071;
    }

    .main .block-container {
        max-width: 1400px;
        padding: 2.2rem 3rem 4rem;
    }

    h1 {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        font-weight: 750 !important;
    }

    h3 {
        font-weight: 700 !important;
    }

    hr {
        border-color: #282d36 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #101319;
        border: 1px solid #292e38;
        border-radius: 15px;
    }

    .stButton > button {
        min-height: 48px;
        border-radius: 10px;
        border: 1px solid #353a45;
        background: #15181f;
        color: #ffffff;
        font-weight: 700;
    }

    .stButton > button:hover {
        border-color: #caa55c;
        color: #e3c57d;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(
            135deg,
            #b98a3d,
            #e1c071
        );
        color: #111111;
        border: none;
        font-weight: 800;
    }

    [data-testid="stFileUploader"] {
        background: #101319;
        border: 1px dashed #66542f;
        border-radius: 14px;
        padding: 0.5rem;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #15181f;
        border-radius: 10px;
    }

    div[role="radiogroup"] {
        gap: 0.8rem;
    }

    div[role="radiogroup"] label {
        background: #11141a;
        border: 1px solid #292e38;
        border-radius: 11px;
        padding: 0.7rem 1rem;
    }

    [data-testid="stMetric"] {
        background: #101319;
        border: 1px solid #292e38;
        border-radius: 12px;
        padding: 1rem;
    }

    [data-testid="stImage"] img {
        border-radius: 13px;
        border: 1px solid #292e38;
    }

    @media (max-width: 700px) {

        .main .block-container {
        padding: 0.5rem;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
    }

        h1 {
            font-size: 1.8rem !important;
        }

        div[role="radiogroup"] {
            flex-direction: column;
        }

        div[role="radiogroup"] label {
            width: 100%;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [5, 1],
    vertical_alignment="center",
)

with header_left:

    st.title("🔎 Visual Jewelry Search")

    st.caption(
        "Find visually similar designs using AI-powered image search."
    )

with header_right:

    if indexes_exist():
        st.success("● AI ONLINE")
    else:
        st.warning("● INDEX REQUIRED")


# ============================================================
# INDEX CHECK
# ============================================================

if not indexes_exist():

    st.divider()

    st.warning(
        "Search indexes are not available. "
        "Please rebuild the indexes before searching."
    )

    st.stop()


# ============================================================
# SEARCH DIRECTION
# ============================================================

st.divider()

st.subheader("01  •  Search Direction")

st.caption(
    "Select which jewelry collection you want to search."
)

search_mode = st.radio(
    "Search Direction",
    [
        "Prototype → Gold",
        "Gold → Prototype",
    ],
    horizontal=True,
    label_visibility="collapsed",
)


# ============================================================
# SEARCH SETTINGS
# ============================================================

st.divider()

settings_col1, settings_col2 = st.columns(2)

with settings_col1:

    top_k = st.slider(
        "Number of results",
        min_value=1,
        max_value=10,
        value=TOP_K,
    )

with settings_col2:

    st.write("")

    st.caption(
        f"Similarity threshold: {SIMILARITY_THRESHOLD:.2f}"
    )


# ============================================================
# UPLOAD
# ============================================================

st.divider()

st.subheader("02  •  Upload Jewelry Image")

if search_mode == "Prototype → Gold":

    st.caption(
        "Upload a prototype image to find similar Gold designs."
    )

    uploader_label = "Prototype Jewelry Image"

else:

    st.caption(
        "Upload a Gold image to find similar Prototype designs."
    )

    uploader_label = "Gold Jewelry Image"


uploaded_file = st.file_uploader(
    uploader_label,
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
        "bmp",
    ],
    help="Upload a clear jewelry image.",
)


# ============================================================
# SEARCH
# ============================================================

if uploaded_file:

    query_image = Image.open(
        uploaded_file
    ).convert("RGB")

    st.write("")

    preview_col, action_col = st.columns(
        [1.35, 1],
        gap="large",
    )

    # --------------------------------------------------------
    # PREVIEW
    # --------------------------------------------------------

    with preview_col:

        with st.container(border=True):

            st.caption("UPLOADED IMAGE")

            st.image(
                query_image,
                use_container_width=True,
            )

    # --------------------------------------------------------
    # SEARCH PANEL
    # --------------------------------------------------------

    with action_col:

        with st.container(border=True):

            st.caption("SEARCH CONFIGURATION")

            st.subheader(
                "Ready to search"
            )

            st.write(
                f"**Direction:** {search_mode}"
            )

            st.write(
                f"**Results:** {top_k}"
            )

            st.write(
                "**Engine:** DINOv2 + FAISS"
            )

            st.write("")

            search_clicked = st.button(
                "✨  Find Similar Jewelry",
                type="primary",
                use_container_width=True,
            )

    # ========================================================
    # RUN SEARCH
    # ========================================================

    if search_clicked:

        with st.spinner(
            "AI is analyzing your jewelry image..."
        ):

            search_engine = load_search_engine()

            if search_mode == "Prototype → Gold":

                raw_results = search_engine.search_gold(
                    query_image,
                    top_k=top_k,
                )

            else:

                raw_results = search_engine.search_prototype(
                    query_image,
                    top_k=top_k,
                )
        similar_results = raw_results

        st.session_state.visual_search_similar_results = similar_results

        results = [
             result
            for result in raw_results
            if float(result["similarity"]) >= SIMILARITY_THRESHOLD
        ]

        results = sorted(
             results,
            key=lambda x: x["similarity"],
            reverse=True,
        )

        st.session_state.visual_search_results = results

        if not results:
            st.warning(
                "⚠️ Similar prototype not available for this jewelry."
            )

        st.session_state.visual_search_mode = search_mode


# ============================================================
# DISPLAY RESULTS
# ============================================================

results = st.session_state.get(
    "visual_search_results"
)

result_mode = st.session_state.get(
    "visual_search_mode",
    search_mode,
)

similar_results = st.session_state.get(
    "visual_search_similar_results",
    []
)

if not results and similar_results:
    st.divider()

    st.subheader("🔎 Similar Designs")

    st.caption(
        "No design met the exact match threshold. "
        "Here are the closest available designs."
    )

    similar_columns = st.columns(
        min(3, len(similar_results))
    )

    for index, result in enumerate(similar_results[:3]):

        result_path = Path(result["image_path"])
        similarity = float(result["similarity"])

        with similar_columns[index % len(similar_columns)]:

            with st.container(border=True):

                try:
                    result_image = Image.open(result_path)

                    st.image(
                        result_image,
                        width="stretch",
                    )

                except Exception:
                    st.warning("Image unavailable")

                jewelry = get_jewelry_details(result_path)

                if jewelry:
                    st.write(
                        f"**{jewelry.get('name', result_path.stem)}**"
                    )
                else:
                    st.write(
                        f"**{result_path.stem}**"
                    )

                st.caption(
                    f"Similarity • {similarity:.1%}"
                )

                st.progress(
                    min(max(similarity, 0.0), 1.0)
                )


if results:

    st.divider()

    st.subheader("03  •  Search Results")

    st.caption(
        f"AI matches from the {result_mode.split('→')[-1].strip()} catalog."
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    best_result = results[0]

    best_score = float(
        best_result["similarity"]
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:

        st.metric(
            "Matches Found",
            len(results),
        )

    with metric2:

        st.metric(
            "Best Similarity",
            f"{best_score:.1%}",
        )

    with metric3:

        catalog_name = (
            "Gold"
            if result_mode == "Prototype → Gold"
            else "Prototype"
        )

        st.metric(
            "Catalog",
            catalog_name,
        )

    # --------------------------------------------------------
    # BEST MATCH
    # --------------------------------------------------------

    st.write("")

    st.subheader("⭐ Best Visual Match")

    best_path = Path(
        best_result["image_path"]
    )

    jewelry = get_jewelry_details(best_path)

    if jewelry:
        display_name = jewelry.get("name", best_path.name)
    else:
        display_name = best_path.name

    best_image_col, best_details_col = st.columns(
        [1.4, 1],
        gap="large",
    )

    with best_image_col:

        try:

            best_image = Image.open(
                best_path
            )

            st.image(
                best_image,
                width="stretch",
            )

        except Exception:

            st.warning(
                "Unable to display the image."
            )

    with best_details_col:

        with st.container(border=True):

            st.caption(
                "HIGHEST VISUAL SIMILARITY"
            )

            st.subheader(
                display_name
            )

            st.metric(
                "Similarity Score",
                f"{best_score:.1%}",
            )

            st.progress(
                min(
                    max(
                        best_score,
                        0.0
                    ),
                    1.0
                )
            )

            st.caption(
                "Higher scores indicate stronger visual similarity."
            )

    # --------------------------------------------------------
    # OTHER RESULTS
    # --------------------------------------------------------

    if len(results) > 1:

        st.write("")

        st.subheader(
            "More Similar Designs"
        )

        remaining_results = results[1:]

        number_of_columns = min(
            2,
            len(remaining_results)
        )

        result_columns = st.columns(
            number_of_columns,
            gap="medium",
        )

        for index, result in enumerate(
            remaining_results
        ):

            column = result_columns[
                index % number_of_columns
            ]

            result_path = Path(
                result["image_path"]
            )

            similarity = float(
                result["similarity"]
            )

            with column:

                with st.container(
                    border=True
                ):

                    try:

                        result_image = Image.open(
                            result_path
                        )

                        st.image(
                            result_image,
                            use_container_width=True,
                        )

                    except Exception:

                        st.warning(
                            "Image unavailable"
                        )

                    jewelry = get_jewelry_details(result_path)

                    if jewelry:
                        st.write(
                            f"**{jewelry.get('name', result_path.stem)}**"
                        )
                    else:
                        st.write(
                            f"**{result_path.stem}**"
                        )

                    st.caption(
                        f"Similarity • {similarity:.1%}"
                    )

                    st.progress(
                        min(
                            max(
                                similarity,
                                0.0
                            ),
                            1.0
                        )
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "💎 JewelVision AI  •  DINOv2 + FAISS  •  Visual Search"
)