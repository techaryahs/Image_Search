from pathlib import Path
import json
import uuid

import streamlit as st

from src.config import (
    GOLD_INDEX_FILE,
    PROTOTYPE_INDEX_FILE,
)
from src.build_index import build_all_indexes
from src.sidebar_style import apply_sidebar_style



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Add Jewelry | JewelVision AI",
    page_icon="✨",
    layout="wide",
)

apply_sidebar_style()
# ============================================================
# PATHS
# ============================================================

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
# FUNCTIONS
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


def save_catalog(catalog):

    with open(
        CATALOG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            catalog,
            file,
            indent=4,
            ensure_ascii=False
        )


def save_jewelry(
    uploaded_file,
    jewelry_name,
    gender,
    jewelry_type,
    jewelry_subtype,
    collection,
    description
):

    # --------------------------------------------------------
    # SELECT FOLDER
    # --------------------------------------------------------

    if collection == "Gold":

        save_folder = GOLD_DIR

    else:

        save_folder = PROTOTYPE_DIR


    save_folder.mkdir(
        parents=True,
        exist_ok=True
    )


    # --------------------------------------------------------
    # CREATE FILE NAME
    # --------------------------------------------------------

    extension = Path(
        uploaded_file.name
    ).suffix.lower()

    safe_name = (
        jewelry_name
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    unique_id = uuid.uuid4().hex[:8]

    filename = (
        f"{safe_name}_{unique_id}{extension}"
    )

    image_path = save_folder / filename


    # --------------------------------------------------------
    # SAVE IMAGE
    # --------------------------------------------------------

    with open(
        image_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )


    # --------------------------------------------------------
    # CREATE CATALOG RECORD
    # --------------------------------------------------------

    catalog = load_catalog()

    jewelry = {

        "id": str(uuid.uuid4()),

        "name": jewelry_name.strip(),

        "gender": gender,

        "type": jewelry_type,

        "subtype": jewelry_subtype,

        "collection": collection,

        "description": description.strip(),

        "image": str(
            image_path.relative_to(BASE_DIR)
        ),
    }


    catalog.append(
        jewelry
    )


    save_catalog(
        catalog
    )


    return jewelry


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [5, 1],
    vertical_alignment="center",
)

with header_left:

    st.title("✨ Add New Jewelry")

    st.caption(
        "Register a jewelry design and add it to your AI catalog."
    )

with header_right:

    st.success("● AI ONLINE")


# ============================================================
# INTRO
# ============================================================

st.divider()

st.subheader(
    "Create a Jewelry Record"
)

st.write(
    "Add the jewelry image and product information below. "
    "After saving, JewelVision will update the AI search index."
)


# ============================================================
# FORM
# ============================================================

with st.container(border=True):

    st.write("### Jewelry Information")

    st.caption(
        "Fields marked with * are required."
    )

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    jewelry_image = st.file_uploader(
        "Jewelry Image *",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
            "bmp",
        ],
        help="Upload a clear image of the jewelry."
    )

    st.write("")


    # --------------------------------------------------------
    # IMAGE PREVIEW
    # --------------------------------------------------------

    if jewelry_image:

        preview_col1, preview_col2 = st.columns(
            [1, 2],
            gap="large"
        )

        with preview_col1:

            st.image(
                jewelry_image,
                use_container_width=True
            )

        with preview_col2:

            st.success(
                "Image ready"
            )

            st.caption(
                jewelry_image.name
            )

            st.caption(
                "The image will be stored in the selected collection."
            )


    st.divider()


    # --------------------------------------------------------
    # NAME + GENDER
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        jewelry_name = st.text_input(
            "Jewelry Name *",
            placeholder="Example: Gold Diamond Ring",
        )

    with col2:

        gender = st.selectbox(
            "Category / Gender *",
            [
                "Female",
                "Male",
                "Unisex",
            ],
        )


    # --------------------------------------------------------
    # TYPE + SUBTYPE
    # --------------------------------------------------------

    col3, col4 = st.columns(2)

    with col3:

        jewelry_type = st.selectbox(
            "Jewelry Type *",
            [
                "Ring",
                "Necklace",
                "Earrings",
                "Bracelet",
                "Bangle",
                "Pendant",
                "Chain",
                "Anklet",
                "Nose Pin",
                "Other",
            ],
        )


    subtype_options = {

        "Ring": [
            "Solitaire Ring",
            "Engagement Ring",
            "Wedding Ring",
            "Cocktail Ring",
            "Band Ring",
            "Statement Ring",
            "Other",
        ],

        "Necklace": [
            "Chain Necklace",
            "Choker",
            "Pendant Necklace",
            "Bridal Necklace",
            "Layered Necklace",
            "Statement Necklace",
            "Other",
        ],

        "Earrings": [
            "Stud Earrings",
            "Hoop Earrings",
            "Drop Earrings",
            "Jhumka",
            "Chandbali",
            "Dangle Earrings",
            "Other",
        ],

        "Bracelet": [
            "Chain Bracelet",
            "Charm Bracelet",
            "Tennis Bracelet",
            "Cuff Bracelet",
            "Beaded Bracelet",
            "Other",
        ],

        "Bangle": [
            "Gold Bangle",
            "Diamond Bangle",
            "Bridal Bangle",
            "Open Bangle",
            "Stackable Bangle",
            "Other",
        ],

        "Pendant": [
            "Heart Pendant",
            "Diamond Pendant",
            "Gold Pendant",
            "Initial Pendant",
            "Religious Pendant",
            "Other",
        ],

        "Chain": [
            "Gold Chain",
            "Box Chain",
            "Rope Chain",
            "Figaro Chain",
            "Singapore Chain",
            "Other",
        ],

        "Anklet": [
            "Gold Anklet",
            "Diamond Anklet",
            "Traditional Anklet",
            "Other",
        ],

        "Nose Pin": [
            "Nose Stud",
            "Nose Ring",
            "Diamond Nose Pin",
            "Gold Nose Pin",
            "Other",
        ],

        "Other": [
            "Other",
        ],
    }


    with col4:

        jewelry_subtype = st.selectbox(
            "Jewelry Subtype *",
            subtype_options[jewelry_type],
        )


    # --------------------------------------------------------
    # COLLECTION
    # --------------------------------------------------------

    collection = st.selectbox(
        "Collection *",
        [
            "Gold",
            "Prototype",
        ],
    )


    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    description = st.text_area(
        "Description",
        placeholder="Describe the jewelry design...",
        height=110,
    )


    st.write("")


    # --------------------------------------------------------
    # SUBMIT
    # --------------------------------------------------------

    submit_jewelry = st.button(
        "✨  Add Jewelry & Update AI",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# SAVE
# ============================================================

if submit_jewelry:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if jewelry_image is None:

        st.error(
            "Please upload a jewelry image."
        )

        st.stop()


    if not jewelry_name.strip():

        st.error(
            "Please enter the jewelry name."
        )

        st.stop()


    # --------------------------------------------------------
    # SAVE IMAGE + METADATA
    # --------------------------------------------------------

    try:

        with st.spinner(
            "Saving jewelry information..."
        ):

            saved_jewelry = save_jewelry(

                uploaded_file=jewelry_image,

                jewelry_name=jewelry_name,

                gender=gender,

                jewelry_type=jewelry_type,

                jewelry_subtype=jewelry_subtype,

                collection=collection,

                description=description,
            )


        st.success(
            "✨ Jewelry information saved successfully!"
        )


        # ----------------------------------------------------
        # UPDATE AI INDEX
        # ----------------------------------------------------

        with st.spinner(
            "🤖 Updating DINOv2 and FAISS search index..."
        ):

            build_all_indexes()

        st.success(
            "🚀 AI search index updated. "
            "This jewelry is now searchable."
        )


        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "Jewelry Added Successfully"
        )


        result_col1, result_col2 = st.columns(
            [1, 1],
            gap="large"
        )


        with result_col1:

            st.image(
                jewelry_image,
                use_container_width=True
            )


        with result_col2:

            st.caption(
                "NEW CATALOG ITEM"
            )

            st.subheader(
                saved_jewelry["name"]
            )

            st.write(
                f"**Gender:** {saved_jewelry['gender']}"
            )

            st.write(
                f"**Type:** {saved_jewelry['type']}"
            )

            st.write(
                f"**Subtype:** {saved_jewelry['subtype']}"
            )

            st.write(
                f"**Collection:** {saved_jewelry['collection']}"
            )

            if saved_jewelry["description"]:

                st.write(
                    f"**Description:** "
                    f"{saved_jewelry['description']}"
                )

            st.success(
                "Available for AI visual search"
            )


    except Exception as e:

        st.error(
            f"Unable to add jewelry: {e}"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "💎 JewelVision AI  •  Jewelry Catalog Management  •  DINOv2 + FAISS"
)