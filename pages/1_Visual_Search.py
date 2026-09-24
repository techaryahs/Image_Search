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
    TOP_K,
    SIMILARITY_THRESHOLD,
)

from src.sidebar_style import apply_sidebar_style


# ============================================================
# SIDEBAR STYLE
# ============================================================

apply_sidebar_style()


# ============================================================
# PAGE CONFIG
# ============================================================

CATALOG_FILE = BASE_DIR / "jewelry_catalog.json"


# ============================================================
# RELEVANCE THRESHOLD
# ============================================================

# Wrong / unrelated image reject करण्यासाठी.
#
# 0.80 = less strict
# 0.85 = strict
# 0.90 = very strict
#
RELEVANCE_THRESHOLD = SIMILARITY_THRESHOLD


# ============================================================
# PAGE CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ================================
       MAIN BACKGROUND
    ================================= */

    .stApp {
        background: #080B0F !important;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        padding-bottom: 4rem;
    }


    /* ================================
       HEADINGS
    ================================= */

    h1 {
        color: #F1F4F7 !important;
        font-weight: 800 !important;
    }

    h2 {
        color: #F1F4F7 !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #E8EDF2 !important;
    }


    /* ================================
       NORMAL TEXT
    ================================= */

    p,
    label,
    span {
        color: #D9DEE5;
    }


    /* ================================
       DIVIDER
    ================================= */

    hr {
        border-color: #29313A !important;
    }


    /* ================================
       BUTTON
    ================================= */

    .stButton > button {
        min-height: 48px;

        border-radius: 10px;

        background: #151B22;

        color: #F1F4F7;

        border: 1px solid #39424D;

        font-weight: 700;
    }

    .stButton > button:hover {
        border-color: #D8B45A;

        color: #D8B45A;
    }


    /* ================================
       FILE UPLOADER
    ================================= */

    [data-testid="stFileUploader"] {
        background: #10151C;

        border: 1px dashed #66542F;

        border-radius: 14px;

        padding: 8px;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #151B22;

        border-radius: 10px;
    }


    /* ================================
       METRIC
    ================================= */

    [data-testid="stMetric"] {
        background: #10151C;

        border: 1px solid #29313A;

        border-radius: 12px;

        padding: 12px;
    }


    /* ================================
       SUCCESS / WARNING / ERROR
    ================================= */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ================================
       RADIO
    ================================= */

    div[role="radiogroup"] label {
        color: #F1F4F7 !important;
    }


    /* ================================
       IMAGE
    ================================= */

    img {
        border-radius: 12px;
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
    Check whether FAISS indexes are available.
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

    except Exception as error:

        print(
            f"Catalog loading error: {error}"
        )

        return []


# ============================================================


def get_jewelry_details(image_path):
    """
    Get catalog details using image filename.
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
    Resolve image path safely.

    Handles:
    - Linux paths
    - Windows paths
    - Relative paths
    - Absolute paths
    - Gold directory
    - Prototype directory
    """

    if not image_path:
        return None

    try:

        raw_path = str(
            image_path
        ).strip()

        if not raw_path:
            return None

        # Convert Windows \ to /
        normalized = raw_path.replace(
            "\\",
            "/",
        )

        path = Path(normalized)


        # -----------------------------------------------
        # 1. Direct path
        # -----------------------------------------------

        if path.exists():
            return path


        # -----------------------------------------------
        # 2. Relative to project root
        # -----------------------------------------------

        project_path = (
            BASE_DIR / normalized
        )

        if project_path.exists():
            return project_path


        # -----------------------------------------------
        # 3. Filename only
        # -----------------------------------------------

        filename = Path(
            normalized
        ).name


        # -----------------------------------------------
        # 4. Gold folder
        # -----------------------------------------------

        gold_path = (
            GOLD_DIR / filename
        )

        if gold_path.exists():
            return gold_path


        # -----------------------------------------------
        # 5. Prototype folder
        # -----------------------------------------------

        prototype_path = (
            PROTOTYPE_DIR / filename
        )

        if prototype_path.exists():
            return prototype_path


        # -----------------------------------------------
        # 6. Recursive search
        # -----------------------------------------------

        for folder in (
            GOLD_DIR,
            PROTOTYPE_DIR,
        ):

            if not folder.exists():
                continue

            matches = list(
                folder.rglob(filename)
            )

            if matches:
                return matches[0]

    except Exception as error:

        print(
            f"Image resolution error: {error}"
        )

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
    Convert similarity score to percentage.
    """

    score = float(score)

    if score <= 1:
        return score * 100

    return score


# ============================================================


def is_relevant(best_similarity):
    """
    Check whether query image is relevant.
    """

    return (
        best_similarity
        >= RELEVANCE_THRESHOLD
    )


# ============================================================
# LOAD SEARCH ENGINE
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
# PAGE HEADER
# ============================================================


st.title(
    "🔎 Visual Search"
)

st.caption(
    "Upload a jewelry image and find visually similar "
    "designs from the JewelVision AI catalog."
)


# ============================================================
# INDEX STATUS
# ============================================================


st.divider()


if indexes_exist():

    st.success(
        "🟢 AI Search Indexes Ready"
    )

else:

    st.error(
        "🔴 AI Search Indexes Not Found"
    )

    st.info(
        "Please build the Gold and Prototype indexes "
        "before using Visual Search."
    )

    st.stop()


# ============================================================
# SEARCH COLLECTION
# ============================================================


st.subheader(
    "Search Collection"
)


search_mode = st.radio(
    "Select collection",
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


st.divider()

st.subheader(
    "Upload Jewelry Image"
)


uploaded_image = st.file_uploader(
    "Choose an image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
        "bmp",
    ],
    help=(
        "Upload a clear image of a ring, "
        "necklace, earring, bracelet, pendant, etc."
    ),
)


# ============================================================
# IMAGE PREVIEW
# ============================================================


if uploaded_image:

    preview_col1, preview_col2 = st.columns(
        [1, 2],
        gap="large",
    )

    with preview_col1:

        try:

            preview_image = Image.open(
                uploaded_image
            ).convert("RGB")

            st.image(
                preview_image,
                caption="Uploaded Image",
                use_container_width=True,
            )

        except Exception:

            st.error(
                "Unable to preview uploaded image."
            )


    with preview_col2:

        st.info(
            f"Selected file: {uploaded_image.name}"
        )

        st.write(
            "Click **Find Similar Jewelry** "
            "to start the visual search."
        )


# ============================================================
# SEARCH BUTTON
# ============================================================


st.write("")


search_button = st.button(
    "🔎 Find Similar Jewelry",
    type="primary",
    use_container_width=True,
)


# ============================================================
# SEARCH PROCESS
# ============================================================


if search_button:

    # --------------------------------------------------------
    # IMAGE REQUIRED
    # --------------------------------------------------------

    if uploaded_image is None:

        st.warning(
            "⚠️ Please upload an image first."
        )

        st.stop()


    try:

        # ====================================================
        # OPEN IMAGE
        # ====================================================

        with st.spinner(
            "Preparing image..."
        ):

            uploaded_image.seek(0)

            query_image = Image.open(
                uploaded_image
            ).convert("RGB")


        # ====================================================
        # LOAD AI ENGINE
        # ====================================================

        with st.spinner(
            "🤖 Loading JewelVision AI..."
        ):

            search_engine = (
                load_search_engine()
            )


        # ====================================================
        # PERFORM SEARCH
        # ====================================================

        with st.spinner(
            "🔍 Searching jewelry catalog..."
        ):


            # ------------------------------------------------
            # GOLD
            # ------------------------------------------------

            if search_mode == "Gold Collection":

                results = (
                    search_engine.search_gold(
                        query_image=query_image,
                        top_k=TOP_K,
                    )
                )


            # ------------------------------------------------
            # PROTOTYPE
            # ------------------------------------------------

            elif search_mode == "Prototype Collection":

                results = (
                    search_engine.search_prototype(
                        query_image=query_image,
                        top_k=TOP_K,
                    )
                )


            # ------------------------------------------------
            # ALL
            # ------------------------------------------------

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

                results = sorted(
                    results,
                    key=get_similarity,
                    reverse=True,
                )

                results = results[:TOP_K]


        # ====================================================
        # NO RESULT
        # ====================================================

        if not results:

            st.error(
                "❌ IRRELEVANT IMAGE"
            )

            st.warning(
                "No relevant jewelry was found "
                "for the uploaded image."
            )

            st.info(
                "Please upload a clear image of jewelry "
                "such as a ring, necklace, earring, "
                "bracelet, or pendant."
            )

            st.stop()


        # ====================================================
        # FIND BEST MATCH
        # ====================================================

        similarity_scores = [
            get_similarity(result)
            for result in results
        ]

        best_similarity = max(
            similarity_scores
        )


        # ====================================================
        # IRRELEVANT IMAGE CHECK
        # ====================================================

        if not is_relevant(
            best_similarity
        ):

            # IMPORTANT:
            # Do not display any search results.

            st.error(
                "❌ IRRELEVANT IMAGE"
            )

            st.warning(
                "The uploaded image does not appear "
                "to be a relevant jewelry image."
            )

            st.info(
                "Please upload a clear image of jewelry "
                "such as a ring, necklace, earring, "
                "bracelet, or pendant."
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Best Similarity",
                    f"{similarity_percentage(best_similarity):.1f}%",
                )

            with col2:

                st.metric(
                    "Required Similarity",
                    f"{similarity_percentage(RELEVANCE_THRESHOLD):.1f}%",
                )

            st.stop()


        # ====================================================
        # RELEVANT IMAGE
        # ====================================================

        st.divider()

        st.success(
            "✅ Relevant jewelry image detected."
        )

        st.subheader(
            "✨ Similar Jewelry"
        )

        st.caption(
            f"Best similarity: "
            f"{similarity_percentage(best_similarity):.1f}%"
        )


        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        for index, result in enumerate(
            results,
            start=1,
        ):

            image_path = result.get(
                "image_path",
                "",
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
            # RESULT LAYOUT
            # =================================================

            image_column, details_column = st.columns(
                [1, 2],
                gap="large",
            )


            # =================================================
            # RESULT IMAGE
            # =================================================

            with image_column:

                if resolved_path:

                    try:

                        st.image(
                            str(resolved_path),
                            caption=f"Result #{index}",
                            use_container_width=True,
                        )

                    except Exception as error:

                        st.warning(
                            "Image preview unavailable."
                        )

                        st.caption(
                            str(error)
                        )

                else:

                    st.warning(
                        "Image preview unavailable."
                    )

                    st.caption(
                        "The image file could not be "
                        "located on the server."
                    )


            # =================================================
            # RESULT DETAILS
            # =================================================

            with details_column:

                st.subheader(
                    f"Result #{index}"
                )


                # ---------------------------------------------
                # CATALOG DETAILS
                # ---------------------------------------------

                details = (
                    get_jewelry_details(
                        image_path
                    )
                )


                if details:

                    name = details.get(
                        "name",
                        "Jewelry",
                    )

                    st.markdown(
                        f"### 💎 {name}"
                    )


                    jewelry_type = details.get(
                        "type",
                        "-",
                    )

                    subtype = details.get(
                        "subtype",
                        "-",
                    )

                    gender = details.get(
                        "gender",
                        "-",
                    )

                    collection = details.get(
                        "collection",
                        "-",
                    )


                    st.write(
                        f"**Type:** {jewelry_type}"
                    )

                    st.write(
                        f"**Subtype:** {subtype}"
                    )

                    st.write(
                        f"**Gender:** {gender}"
                    )

                    st.write(
                        f"**Collection:** {collection}"
                    )


                    description = details.get(
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

                st.metric(
                    "Similarity",
                    f"{similarity_percentage(similarity):.1f}%",
                )


                # ---------------------------------------------
                # IMAGE PATH
                # ---------------------------------------------

                if resolved_path:

                    st.caption(
                        f"Image: {resolved_path.name}"
                    )

                else:

                    st.caption(
                        f"Path: {image_path}"
                    )


            st.divider()


    # ========================================================
    # ERROR HANDLING
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
    "💎 JewelVision AI • DINOv2 • FAISS Visual Search"
)