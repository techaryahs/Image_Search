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

GOLD_DIR = BASE_DIR / "data" / "gold"

PROTOTYPE_DIR = BASE_DIR / "data" / "prototype"


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

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def indexes_exist():
    """
    Check whether required FAISS indexes exist.
    """

    return (
        GOLD_INDEX_FILE.exists()
        and PROTOTYPE_INDEX_FILE.exists()
    )


def load_catalog():
    """
    Load jewelry catalog.
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
    Find catalog record using image filename.
    """

    if not image_path:
        return None

    catalog = load_catalog()

    target_filename = Path(
        str(image_path)
    ).name

    for item in catalog:

        catalog_image = item.get(
            "image",
            ""
        )

        if not catalog_image:
            continue

        catalog_filename = Path(
            str(catalog_image)
        ).name

        if catalog_filename == target_filename:

            return item

    return None


def resolve_image_path(image_path):
    """
    Convert the path returned by FAISS/search.py
    into a valid local path on Render.
    """

    if not image_path:
        return None

    try:

        raw_path = str(image_path).strip()

        if not raw_path:
            return None

        path = Path(raw_path)

        # ----------------------------------------------------
        # 1. Absolute path
        # ----------------------------------------------------

        if path.is_absolute() and path.exists():

            return path


        # ----------------------------------------------------
        # 2. Path relative to project root
        # ----------------------------------------------------

        project_path = BASE_DIR / path

        if project_path.exists():

            return project_path


        # ----------------------------------------------------
        # 3. Filename only
        # ----------------------------------------------------

        filename = path.name


        # Gold folder
        gold_path = GOLD_DIR / filename

        if gold_path.exists():

            return gold_path


        # Prototype folder
        prototype_path = PROTOTYPE_DIR / filename

        if prototype_path.exists():

            return prototype_path


        # ----------------------------------------------------
        # 4. Search recursively
        # ----------------------------------------------------

        for folder in [
            GOLD_DIR,
            PROTOTYPE_DIR,
        ]:

            if not folder.exists():
                continue

            matches = list(
                folder.rglob(filename)
            )

            if matches:

                return matches[0]


    except Exception:

        return None

    return None


# ============================================================
# LAZY LOAD SEARCH ENGINE
# ============================================================

@st.cache_resource(
    show_spinner=False
)
def load_search_engine():

    # Heavy AI libraries are loaded only when search starts.
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
        "Upload a jewelry image and find visually similar "
        "designs from the JewelVision AI catalog."
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
    "Upload a jewelry image below. JewelVision uses "
    "DINOv2 visual embeddings and FAISS similarity "
    "search to find matching jewelry designs."
)


# ============================================================
# INDEX CHECK
# ============================================================

if not indexes_exist():

    st.warning(
        "⚠️ AI search indexes are not available yet."
    )

    st.info(
        "Please build the Gold and Prototype indexes "
        "before using Visual Search."
    )

    st.stop()


# ============================================================
# SEARCH SETTINGS
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


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.write("")

with st.container(border=True):

    st.write("### Upload Jewelry Image")

    uploaded_image = st.file_uploader(
        "Choose a jewelry image",
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
                "The AI will compare this image with "
                "the jewelry catalog."
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
        # PREPARE QUERY IMAGE
        # ----------------------------------------------------

        with st.spinner(
            "Preparing image..."
        ):

            query_image = Image.open(
                uploaded_image
            ).convert("RGB")


        # ----------------------------------------------------
        # LOAD SEARCH ENGINE
        # ----------------------------------------------------

        with st.spinner(
            "🤖 Loading JewelVision AI..."
        ):

            search_engine = load_search_engine()


        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        with st.spinner(
            "🔍 Searching for visually similar jewelry..."
        ):

            if search_mode == "Gold Collection":

                results = search_engine.search_gold(
                    query_image=query_image,
                    top_k=TOP_K,
                )


            elif search_mode == "Prototype Collection":

                results = search_engine.search_prototype(
                    query_image=query_image,
                    top_k=TOP_K,
                )


            else:

                gold_results = search_engine.search_gold(
                    query_image=query_image,
                    top_k=TOP_K,
                )

                prototype_results = search_engine.search_prototype(
                    query_image=query_image,
                    top_k=TOP_K,
                )

                results = (
                    gold_results +
                    prototype_results
                )

                # ------------------------------------------------
                # SORT RESULTS
                # ------------------------------------------------

                def get_similarity(item):

                    try:

                        return float(
                            item.get(
                                "similarity",
                                0
                            )
                        )

                    except Exception:

                        return 0


                results = sorted(
                    results,
                    key=get_similarity,
                    reverse=True,
                )

                results = results[:TOP_K]


        # ====================================================
        # RESULTS
        # ====================================================

        st.divider()

        st.subheader(
            "✨ Search Results"
        )


        if not results:

            st.info(
                "No visually similar jewelry was found."
            )

            st.caption(
                "Try another image with a clearer view "
                "of the jewelry."
            )

            st.stop()


        st.caption(
            f"Found {len(results)} visually similar jewelry designs."
        )


        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        for index, result in enumerate(
            results,
            start=1
        ):

            # ------------------------------------------------
            # GET RESULT DATA
            # ------------------------------------------------

            image_path = result.get(
                "image_path"
            )

            similarity = result.get(
                "similarity"
            )


            # ------------------------------------------------
            # RESOLVE IMAGE
            # ------------------------------------------------

            resolved_path = resolve_image_path(
                image_path
            )


            # ------------------------------------------------
            # RESULT LAYOUT
            # ------------------------------------------------

            result_col1, result_col2 = st.columns(
                [1, 2],
                gap="large"
            )


            # ------------------------------------------------
            # IMAGE
            # ------------------------------------------------

            with result_col1:

                if resolved_path:

                    try:

                        st.image(
                            str(resolved_path),
                            caption=f"Result #{index}",
                            use_container_width=True,
                        )

                    except Exception as image_error:

                        st.warning(
                            "Image preview unavailable."
                        )

                        st.caption(
                            str(image_error)
                        )

                else:

                    st.warning(
                        "Image preview unavailable."
                    )

                    st.caption(
                        f"Path returned by search: "
                        f"{image_path}"
                    )


            # ------------------------------------------------
            # DETAILS
            # ------------------------------------------------

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
                )


                if jewelry_details:

                    st.markdown(
                        f"### "
                        f"{jewelry_details.get('name', 'Jewelry')}"
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

                else:

                    st.caption(
                        "Catalog information not available."
                    )


                # --------------------------------------------
                # SIMILARITY SCORE
                # --------------------------------------------

                if similarity is not None:

                    try:

                        similarity_value = float(
                            similarity
                        )

                        # Handle both 0-1 and 0-100 formats
                        if similarity_value <= 1:

                            similarity_percent = (
                                similarity_value * 100
                            )

                        else:

                            similarity_percent = (
                                similarity_value
                            )


                        if similarity_value <= 1:

                            threshold_check = (
                                similarity_value
                                >= SIMILARITY_THRESHOLD
                            )

                        else:

                            threshold_check = (
                                similarity_percent
                                >= SIMILARITY_THRESHOLD * 100
                            )


                        if threshold_check:

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
                            f"Similarity score: "
                            f"{similarity}"
                        )


                # --------------------------------------------
                # IMAGE PATH
                # --------------------------------------------

                if resolved_path:

                    st.caption(
                        f"Image: "
                        f"{resolved_path.name}"
                    )

                elif image_path:

                    st.caption(
                        f"Image path: "
                        f"{image_path}"
                    )


            st.divider()


    # ========================================================
    # ERROR HANDLING
    # ========================================================

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
    "💎 JewelVision AI  •  DINOv2 Visual Search  •  "
    "FAISS Similarity Engine"
)