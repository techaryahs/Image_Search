from pathlib import Path
import json

import streamlit as st
from PIL import Image
from src.sidebar_style import apply_sidebar_style

apply_sidebar_style()

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Jewelry Catalog | JewelVision AI",
    page_icon="📦",
    layout="wide",
)


# ============================================================
# PATHS
# ============================================================

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
        border-color: #292e38 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #101319;
        border: 1px solid #292e38;
        border-radius: 15px;
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

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD CATALOG
# ============================================================

def load_catalog():

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


catalog = load_catalog()


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [5, 1],
    vertical_alignment="center",
)

with header_left:

    st.title("📦 Jewelry Catalog")

    st.caption(
        "Browse, search and filter your registered jewelry designs."
    )

with header_right:

    st.success("● CATALOG")


# ============================================================
# EMPTY CATALOG
# ============================================================

if not catalog:

    st.divider()

    with st.container(border=True):

        st.subheader(
            "No Jewelry Designs Yet"
        )

        st.write(
            "Your jewelry catalog is currently empty."
        )

        st.info(
            "Go to Add Jewelry to register your first design."
        )

    st.stop()


# ============================================================
# SUMMARY
# ============================================================

st.divider()

total_items = len(catalog)

gold_items = sum(
    1
    for item in catalog
    if item.get("collection") == "Gold"
)

prototype_items = sum(
    1
    for item in catalog
    if item.get("collection") == "Prototype"
)

female_items = sum(
    1
    for item in catalog
    if item.get("gender") == "Female"
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.metric(
        "Total Designs",
        total_items
    )

with metric2:

    st.metric(
        "Gold",
        gold_items
    )

with metric3:

    st.metric(
        "Prototype",
        prototype_items
    )

with metric4:

    st.metric(
        "Female",
        female_items
    )


# ============================================================
# FILTERS
# ============================================================

st.write("")

st.subheader("Catalog Filters")

filter1, filter2, filter3 = st.columns(3)

with filter1:

    search_text = st.text_input(
        "Search",
        placeholder="Search jewelry name...",
    )

with filter2:

    gender_options = sorted(
        set(
            item.get("gender", "")
            for item in catalog
            if item.get("gender")
        )
    )

    gender_filter = st.selectbox(
        "Gender",
        ["All"] + gender_options,
    )

with filter3:

    collection_filter = st.selectbox(
        "Collection",
        [
            "All",
            "Gold",
            "Prototype",
        ],
    )


type_options = sorted(
    set(
        item.get("type", "")
        for item in catalog
        if item.get("type")
    )
)

type_filter = st.selectbox(
    "Jewelry Type",
    ["All"] + type_options,
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_catalog = []

for item in catalog:

    # Search
    if search_text:

        if search_text.lower() not in item.get(
            "name",
            ""
        ).lower():

            continue

    # Gender
    if (
        gender_filter != "All"
        and item.get("gender") != gender_filter
    ):

        continue

    # Collection
    if (
        collection_filter != "All"
        and item.get("collection") != collection_filter
    ):

        continue

    # Type
    if (
        type_filter != "All"
        and item.get("type") != type_filter
    ):

        continue

    filtered_catalog.append(item)


# ============================================================
# RESULT COUNT
# ============================================================

st.write("")

st.caption(
    f"Showing {len(filtered_catalog)} of {total_items} jewelry designs"
)


# ============================================================
# CATALOG GRID
# ============================================================

if filtered_catalog:

    columns_count = 4

    catalog_columns = st.columns(
        columns_count,
        gap="medium"
    )

    for index, item in enumerate(
        filtered_catalog
    ):

        column = catalog_columns[
            index % columns_count
        ]

        with column:

            with st.container(
                border=True
            ):

                # --------------------------------------------
                # IMAGE
                # --------------------------------------------

                image_path = BASE_DIR / item.get(
                    "image",
                    ""
                )

                if image_path.exists():

                    try:

                        jewelry_image = Image.open(
                            image_path
                        )

                        st.image(
                            jewelry_image,
                            use_container_width=True
                        )

                    except Exception:

                        st.warning(
                            "Unable to load image."
                        )

                else:

                    st.warning(
                        "Image not found."
                    )


                # --------------------------------------------
                # NAME
                # --------------------------------------------

                st.subheader(
                    item.get(
                        "name",
                        "Unnamed Jewelry"
                    )
                )


                # --------------------------------------------
                # COLLECTION + GENDER
                # --------------------------------------------

                st.caption(
                    f"{item.get('collection', 'N/A')}  •  "
                    f"{item.get('gender', 'N/A')}"
                )


                # --------------------------------------------
                # TYPE
                # --------------------------------------------

                st.write(
                    f"**Type:** "
                    f"{item.get('type', 'N/A')}"
                )


                # --------------------------------------------
                # SUBTYPE
                # --------------------------------------------

                st.write(
                    f"**Subtype:** "
                    f"{item.get('subtype', 'N/A')}"
                )


                # --------------------------------------------
                # DESCRIPTION
                # --------------------------------------------

                description = item.get(
                    "description",
                    ""
                )

                if description:

                    st.caption(
                        description
                    )

else:

    st.info(
        "No jewelry designs match your selected filters."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "💎 JewelVision AI  •  Jewelry Catalog Management"
)