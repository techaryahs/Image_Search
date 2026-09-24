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

from src.sidebar_style import apply_sidebar_style


# ============================================================
# PAGE SETUP
# ============================================================

apply_sidebar_style()

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOG_FILE = BASE_DIR / "jewelry_catalog.json"


# ============================================================
# STYLING
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

    .main .block-container {
        max-width: 1250px;
        padding: 2.5rem 3rem 4rem;
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
        border-color: #292e38 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #101319;
        border: 1px solid #292e38;
        border-radius: 16px;
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
        background:
            linear-gradient(
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

    .result-card {
        background: #101319;
        border: 1px solid #292e38;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 18px;
    }

    .gold-text {
        color: #e1c071;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNCTIONS
# ============================================================

def indexes_exist():
    """
    Check whether both FAISS indexes exist.
    """

    return (
        GOLD_INDEX_FILE.exists()
        and PROTOTYPE_INDEX_FILE.exists()
    )


def load_catalog():
    """
    Load jewelry catalog JSON.
    """

    if not CATALOG_FILE.exists():
        return []

    try:

        with open(
            CATALOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def get_jewelry_details(image_path):
    """
    Find jewelry metadata using image filename.
    """

    catalog = load_catalog()

    if not catalog:
        return None

    target_name = Path(
        str(image_path)
    ).name

    for item in catalog:

        item_image = item.get(
            "image",
            ""
        )

        if not item_image:
            continue

        catalog_image_name = Path(
            str(item_image)
        ).name

        if catalog_image_name == target_name:
            return item

    return None


@st.cache_resource(
    show_spinner=False
)
def load_search_engine():
    """
    IMPORTANT:
    Heavy DINOv2 / Torch / FAISS code is imported
    only when the user actually starts a search.
    """

    from src.search import BidirectionalJewelrySearch

    return BidirectionalJewelrySearch()


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [5, 1],
    vertical_alignment="center",
)

with header_left:

    st.title("🔎 Visual Search")

    st.caption(
        "Upload a jewelry image and find visually similar designs "
        "from the JewelVision AI catalog."
    )

with header_right:

    if indexes_exist():

        st.success("● AI READY")

    else:

        st.warning("● INDEX MISSING")


# ============================================================
# INTRO
# ============================================================

st.divider()

st.subheader(
    "Find Similar Jewelry"
)

st.write(
    "Upload a jewelry image below. JewelVision uses DINOv2 "
    "visual embeddings and FAISS similarity search to find "
    "matching jewelry designs."
)


# ============================================================
# INDEX STATUS
# ============================================================

if not indexes_exist():

    st.warning(
        "⚠️ AI search indexes are not available yet."
    )

    st.info(
        "Please build the Gold and Prototype indexes before "
        "using Visual Search."
    )

    st.stop()


# ============================================================
# SEARCH OPTIONS
# ============================================================

with st.container(border=True):

    st.write("### Search Settings")

    search_mode = st.radio(
        "Search Collection",
        [
            "All Jewelry",
            "Gold Collection",
            "Prototype Collection",
        ],
        horizontal=True,
    )

    st.write("")


# ============================================================
# IMAGE UPLOAD
# ============================================================

with st.container(border=True):

    st.write("### Upload Jewelry Image")

    uploaded_image = st.file_uploader(
        "Choose an image",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
            "bmp",
        ],
        help="Upload a clear jewelry image for visual similarity search.",
    )

    if uploaded_image:

        st.write("")

        preview_col1, preview_col2 = st.columns(
            [1, 2],
            gap="large"
        )

        with preview_col1:

            st.image(
                uploaded_image,
                caption="Query Image",
                use_container_width=True,
            )

        with preview_col2:

            st.success(
                "Image ready for visual search."
            )

            st.caption(
                f"File: {uploaded_image.name}"
            )

            st.caption(
                "The AI will compare the uploaded image "
                "with the jewelry catalog."
            )


# ============================================================
# SEARCH BUTTON
# ============================================================

st.write("")

search_button = st.button(
    "🔎  Find Similar Jewelry",
    type="primary",
    use_container_width=True,
)


# ============================================================
# SEARCH
# ============================================================

if search_button:

    if uploaded_image is None:

        st.error(
            "Please upload a jewelry image first."
        )

        st.stop()

    try:

        # ----------------------------------------------------
        # LOAD IMAGE
        # ----------------------------------------------------

        with st.spinner(
            "Preparing image..."
        ):

            query_image = Image.open(
                uploaded_image
            ).convert("RGB")


        # ----------------------------------------------------
        # LOAD AI SEARCH ENGINE
        # ----------------------------------------------------

        with st.spinner(
            "🤖 Loading JewelVision AI..."
        ):

            search_engine = load_search_engine()


        # ----------------------------------------------------
        # SELECT SEARCH INDEX
        # ----------------------------------------------------

        if search_mode == "Gold Collection":

            search_index = "gold"

        elif search_mode == "Prototype Collection":

            search_index = "prototype"

        else:

            search_index = "all"


        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        with st.spinner(
            "🔍 Searching for visually similar jewelry..."
        ):

            if search_index == "gold":

                results = search_engine.search_gold(
                    query_image,
                    top_k=TOP_K,
                )

            elif search_index == "prototype":

                results = search_engine.search_prototype(
                    query_image,
                    top_k=TOP_K,
                )

            else:

                results = search_engine.search(
                    query_image,
                    top_k=TOP_K,
                )


        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "✨ Search Results"
        )


        if not results:

            st.info(
                "No visually similar jewelry was found."
            )

            st.caption(
                "Try another image with a clearer view of the jewelry."
            )

            st.stop()


        # ----------------------------------------------------
        # RESULT COUNT
        # ----------------------------------------------------

        st.caption(
            f"Found {len(results)} visually similar jewelry designs."
        )


        # ----------------------------------------------------
        # DISPLAY RESULTS
        # ----------------------------------------------------

        for index, result in enumerate(
            results,
            start=1
        ):

            # ------------------------------------------------
            # RESULT FORMAT
            # ------------------------------------------------

            if isinstance(result, dict):

                image_path = (
                    result.get("image_path")
                    or result.get("path")
                    or result.get("image")
                )

                score = (
                    result.get("similarity")
                    or result.get("score")
                    or result.get("distance")
                )

            elif isinstance(result, (list, tuple)):

                image_path = result[0]

                score = (
                    result[1]
                    if len(result) > 1
                    else None
                )

            else:

                image_path = result

                score = None


            # ------------------------------------------------
            # RESULT CARD
            # ------------------------------------------------

            result_col1, result_col2 = st.columns(
                [1, 2],
                gap="large"
            )

            with result_col1:

                try:

                    st.image(
                        str(image_path),
                        use_container_width=True,
                    )

                except Exception:

                    st.warning(
                        "Image preview unavailable."
                    )


            with result_col2:

                st.markdown(
                    f"### #{index}"
                )


                # --------------------------------------------
                # CATALOG DETAILS
                # --------------------------------------------

                jewelry_details = (
                    get_jewelry_details(
                        image_path
                    )
                    if image_path
                    else None
                )


                if jewelry_details:

                    st.markdown(
                        f"### {jewelry_details.get('name', 'Jewelry')}"
                    )

                    st.write(
                        f"**Gender:** "
                        f"{jewelry_details.get('gender', '-')}"
                    )

                    st.write(
                        f"**Type:** "
                        f"{jewelry_details.get('type', '-')}"
                    )

                    st.write(
                        f"**Subtype:** "
                        f"{jewelry_details.get('subtype', '-')}"
                    )

                    st.write(
                        f"**Collection:** "
                        f"{jewelry_details.get('collection', '-')}"
                    )

                    description = jewelry_details.get(
                        "description",
                        ""
                    )

                    if description:

                        st.write(
                            f"**Description:** "
                            f"{description}"
                        )


                # --------------------------------------------
                # SIMILARITY SCORE
                # --------------------------------------------

                if score is not None:

                    try:

                        score_value = float(
                            score
                        )

                        if score_value <= 1:

                            similarity_percent = (
                                score_value * 100
                            )

                        else:

                            similarity_percent = score_value


                        if similarity_percent >= (
                            SIMILARITY_THRESHOLD * 100
                        ):

                            st.success(
                                f"Similarity: "
                                f"{similarity_percent:.1f}%"
                            )

                        else:

                            st.info(
                                f"Similarity: "
                                f"{similarity_percent:.1f}%"
                            )

                    except Exception:

                        st.caption(
                            f"Similarity score: {score}"
                        )


                if image_path:

                    st.caption(
                        f"Image: {Path(str(image_path)).name}"
                    )


            st.divider()


    except Exception as e:

        st.error(
            "❌ Unable to perform visual search."
        )

        st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "💎 JewelVision AI  •  DINOv2 Visual Search  •  FAISS Similarity Engine"
)