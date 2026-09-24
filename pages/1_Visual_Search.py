from pathlib import Path
import json

import streamlit as st
from PIL import Image

from src.config import (
    BASE_DIR,
    GOLD_DIR,
    PROTOTYPE_DIR,
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


CATALOG_FILE = BASE_DIR / "jewelry_catalog.json"


# ============================================================
# PAGE CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================================
       MAIN APP
    ========================================= */

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(216, 180, 90, 0.07),
                transparent 25%
            ),
            #080B0F;
    }


    .main .block-container {
        max-width: 1250px;
        padding: 2.5rem 3rem 4rem;
    }


    /* =========================================
       HEADINGS
    ========================================= */

    h1 {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        color: #F1F4F7 !important;
    }


    h2 {
        color: #F1F4F7 !important;
        font-weight: 750 !important;
    }


    h3 {
        color: #E8EDF2 !important;
        font-weight: 700 !important;
    }


    /* =========================================
       CONTAINERS
    ========================================= */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background: #10151C !important;

        border: 1px solid #2C343E !important;

        border-radius: 16px !important;
    }


    /* =========================================
       DIVIDER
    ========================================= */

    hr {
        border-color: #29313A !important;
    }


    /* =========================================
       BUTTON
    ========================================= */

    .stButton > button {

        min-height: 48px;

        border-radius: 10px;

        border: 1px solid #39424D;

        background: #151B22;

        color: #F1F4F7;

        font-weight: 700;
    }


    .stButton > button:hover {

        border-color: #D8B45A;

        color: #E1BD67;
    }


    /* Primary button */

    div[data-testid="stButton"]
    button[kind="primary"] {

        background:
            linear-gradient(
                135deg,
                #B98A3D,
                #E1C071
            ) !important;

        color: #111111 !important;

        border: none !important;

        font-weight: 800 !important;
    }


    /* =========================================
       FILE UPLOADER
    ========================================= */

    [data-testid="stFileUploader"] {

        background: #10151C;

        border: 1px dashed #66542F;

        border-radius: 14px;

        padding: 0.5rem;
    }


    [data-testid="stFileUploaderDropzone"] {

        background: #151B22;

        border-radius: 10px;
    }


    /* =========================================
       METRIC / SCORE
    ========================================= */

    .similarity-box {

        padding: 12px 16px;

        border-radius: 10px;

        background: rgba(216, 180, 90, 0.10);

        border: 1px solid rgba(216, 180, 90, 0.30);

        color: #E1BD67;

        font-weight: 700;
    }


    /* =========================================
       RESULT CARD
    ========================================= */

    .result-title {

        color: #D8B45A;

        font-size: 20px;

        font-weight: 800;

        margin-bottom: 10px;
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
    Check whether both FAISS indexes exist.
    """

    return (
        GOLD_INDEX_FILE.exists()
        and PROTOTYPE_INDEX_FILE.exists()
    )


# ============================================================


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
            encoding="utf-8",
        ) as file:

            data = json.load(file)


        if isinstance(data, list):

            return data


        return []


    except Exception:

        return []


# ============================================================


def get_jewelry_details(image_path):
    """
    Find jewelry information using image filename.
    """

    if not image_path:

        return None


    filename = Path(
        str(image_path)
    ).name.lower()


    catalog = load_catalog()


    for item in catalog:

        catalog_image = item.get(
            "image",
            "",
        )


        if not catalog_image:

            continue


        catalog_filename = Path(
            str(catalog_image)
        ).name.lower()


        if catalog_filename == filename:

            return item


    return None


# ============================================================


def resolve_image_path(image_path):
    """
    Resolve image paths created on another machine.

    Handles:
    - Windows paths
    - Linux paths
    - relative paths
    - filenames
    - Gold folder
    - Prototype folder
    """

    if not image_path:

        return None


    try:

        raw_path = str(
            image_path
        ).strip()


        if not raw_path:

            return None


        # Convert Windows separators
        normalized = raw_path.replace(
            "\\",
            "/",
        )


        path = Path(normalized)


        # ----------------------------------------------------
        # 1. Existing absolute path
        # ----------------------------------------------------

        if path.is_absolute():

            if path.exists():

                return path


        # ----------------------------------------------------
        # 2. Relative to project
        # ----------------------------------------------------

        project_path = (
            BASE_DIR / normalized
        )


        if project_path.exists():

            return project_path


        # ----------------------------------------------------
        # 3. Filename
        # ----------------------------------------------------

        filename = Path(
            normalized
        ).name


        # Gold
        gold_path = (
            GOLD_DIR / filename
        )


        if gold_path.exists():

            return gold_path


        # Prototype
        prototype_path = (
            PROTOTYPE_DIR / filename
        )


        if prototype_path.exists():

            return prototype_path


        # ----------------------------------------------------
        # 4. Recursive search
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


def get_similarity(result):
    """
    Safely get similarity score.
    """

    try:

        return float(
            result.get(
                "similarity",
                0.0,
            )
        )

    except Exception:

        return 0.0


# ============================================================


def similarity_percentage(score):
    """
    Convert similarity to percentage.
    """

    if score <= 1:

        return score * 100


    return score


# ============================================================


def is_relevant(score):
    """
    Check whether result passes similarity threshold.
    """

    # Similarity from FAISS is normally 0-1.
    return score >= SIMILARITY_THRESHOLD


# ============================================================
# SEARCH ENGINE
# ============================================================

@st.cache_resource(
    show_spinner=False
)
def load_search_engine():

    from src.search import (
        BidirectionalJewelrySearch
    )

    return BidirectionalJewelrySearch()


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [5, 1],
    vertical_alignment="center",
)


with header_left:

    st.title(
        "🔎 Visual Search"
    )

    st.caption(
        "Upload a jewelry image and find visually similar "
        "designs from the JewelVision AI catalog."
    )


with header_right:

    if indexes_exist():

        st.success(
            "● AI READY"
        )

    else:

        st.warning(
            "● INDEX MISSING"
        )


# ============================================================
# INTRO
# ============================================================

st.divider()


st.subheader(
    "Find Similar Jewelry"
)


st.write(
    "Upload a jewelry image below. JewelVision AI "
    "uses DINOv2 visual embeddings and FAISS similarity "
    "search to identify visually similar jewelry."
)


# ============================================================
# INDEX CHECK
# ============================================================

if not indexes_exist():

    st.warning(
        "⚠️ AI search indexes are not available."
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

    st.write(
        "### Search Collection"
    )


    search_mode = st.radio(
        "Select collection",
        [
            "All Jewelry",
            "Gold Collection",
            "Prototype Collection",
        ],
        horizontal=True,
        label_visibility="collapsed",
    )


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.write("")


with st.container(border=True):

    st.write(
        "### Upload Jewelry Image"
    )


    uploaded_image = st.file_uploader(
        "Choose a jewelry image",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
            "bmp",
        ],
        help=(
            "Upload a clear jewelry image "
            "for visual similarity search."
        ),
    )


    if uploaded_image:

        st.write("")


        preview_col1, preview_col2 = st.columns(
            [1, 2],
            gap="large",
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
                "The AI will compare this image "
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
# SEARCH PROCESS
# ============================================================

if search_button:

    # --------------------------------------------------------
    # CHECK UPLOAD
    # --------------------------------------------------------

    if uploaded_image is None:

        st.error(
            "Please upload a jewelry image first."
        )

        st.stop()


    try:

        # ----------------------------------------------------
        # OPEN IMAGE
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

            search_engine = (
                load_search_engine()
            )


        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        with st.spinner(
            "🔍 Searching jewelry catalog..."
        ):


            if search_mode == "Gold Collection":

                results = (
                    search_engine.search_gold(
                        query_image=query_image,
                        top_k=TOP_K,
                    )
                )


            elif search_mode == "Prototype Collection":

                results = (
                    search_engine.search_prototype(
                        query_image=query_image,
                        top_k=TOP_K,
                    )
                )


            else:

                gold_results = (
                    search_engine.search_gold(
                        query_image=query_image,
                        top_k=TOP_K,
                    )
                )


                prototype_results = (
                    search_engine.search_prototype(
                        query_image=query_image,
                        top_k=TOP_K,
                    )
                )


                results = (
                    gold_results
                    + prototype_results
                )


                # Sort by similarity
                results = sorted(
                    results,
                    key=get_similarity,
                    reverse=True,
                )


                # Keep top results
                results = results[:TOP_K]


        # ====================================================
        # NO RESULTS
        # ====================================================

        if not results:

            st.warning(
                "⚠️ No matching jewelry found."
            )

            st.info(
                "Please upload a clear jewelry image "
                "and try again."
            )

            st.stop()


        # ====================================================
        # BEST SIMILARITY
        # ====================================================

        best_similarity = max(
            get_similarity(result)
            for result in results
        )


        # ====================================================
        # IMPORTANT:
        # IRRELEVANT IMAGE CHECK
        # ====================================================

        if not is_relevant(
            best_similarity
        ):

            st.error(
                "❌ Irrelevant Image"
            )


            st.warning(
                "The uploaded image does not appear "
                "to be a relevant jewelry image."
            )


            st.info(
                "Please upload a clear image of "
                "jewelry such as a ring, necklace, "
                "earring, bracelet, or other jewelry."
            )


            st.caption(
                f"Best similarity score: "
                f"{best_similarity:.2f}  |  "
                f"Required threshold: "
                f"{SIMILARITY_THRESHOLD:.2f}"
            )


            st.stop()


        # ====================================================
        # RELEVANT RESULTS
        # ====================================================

        st.divider()


        st.subheader(
            "✨ Similar Jewelry"
        )


        st.success(
            "Relevant jewelry image detected."
        )


        st.caption(
            f"Best similarity: "
            f"{similarity_percentage(best_similarity):.1f}%"
        )


        st.write("")


        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        for index, result in enumerate(
            results,
            start=1,
        ):

            image_path = result.get(
                "image_path"
            )


            original_image_path = result.get(
                "original_image_path",
                image_path,
            )


            similarity = get_similarity(
                result
            )


            resolved_path = (
                resolve_image_path(
                    image_path
                )
            )


            # =================================================
            # RESULT CARD
            # =================================================

            result_col1, result_col2 = st.columns(
                [1, 2],
                gap="large",
            )


            # =================================================
            # IMAGE
            # =================================================

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
                        "The search result was found, "
                        "but the image file could not "
                        "be located on the server."
                    )


                    # Debug path
                    st.code(
                        str(original_image_path)
                    )


            # =================================================
            # DETAILS
            # =================================================

            with result_col2:

                st.markdown(
                    f"""
                    <div class="result-title">
                        Result #{index}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


                # ---------------------------------------------
                # CATALOG DETAILS
                # ---------------------------------------------

                jewelry_details = (
                    get_jewelry_details(
                        image_path
                    )
                )


                if jewelry_details:

                    name = jewelry_details.get(
                        "name",
                        "Jewelry",
                    )


                    st.markdown(
                        f"### {name}"
                    )


                    gender = jewelry_details.get(
                        "gender",
                        "-",
                    )


                    jewelry_type = jewelry_details.get(
                        "type",
                        "-",
                    )


                    subtype = jewelry_details.get(
                        "subtype",
                        "-",
                    )


                    collection = jewelry_details.get(
                        "collection",
                        "-",
                    )


                    st.write(
                        f"**Gender:** {gender}"
                    )


                    st.write(
                        f"**Type:** {jewelry_type}"
                    )


                    st.write(
                        f"**Subtype:** {subtype}"
                    )


                    st.write(
                        f"**Collection:** {collection}"
                    )


                    description = jewelry_details.get(
                        "description",
                        "",
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


                # ---------------------------------------------
                # SIMILARITY
                # ---------------------------------------------

                percentage = (
                    similarity_percentage(
                        similarity
                    )
                )


                st.markdown(
                    f"""
                    <div class="similarity-box">
                        ✨ Similarity: {percentage:.1f}%
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


                st.write("")


                # ---------------------------------------------
                # IMAGE FILE
                # ---------------------------------------------

                if resolved_path:

                    st.caption(
                        f"Image: "
                        f"{resolved_path.name}"
                    )

                else:

                    st.caption(
                        f"Original path: "
                        f"{original_image_path}"
                    )


            st.divider()


    # ========================================================
    # ERROR
    # ========================================================

    except Exception as error:

        st.error(
            "❌ Unable to perform visual search."
        )

        st.exception(
            error
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "💎 JewelVision AI  •  DINOv2 Visual Search  •  "
    "FAISS Similarity Engine"
)