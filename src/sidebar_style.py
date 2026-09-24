import streamlit as st


def apply_sidebar_style():

    st.markdown(
        """
        <style>

        /* =====================================================
           SIDEBAR BACKGROUND
        ===================================================== */

        section[data-testid="stSidebar"] {
            background: #0B1220 !important;
            color: #F1F4F7 !important;
            border-right: 1px solid #263247 !important;
        }

        section[data-testid="stSidebar"] > div {
            background: #0B1220 !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            background: #0B1220 !important;
        }


        /* =====================================================
           SIDEBAR FONT
        ===================================================== */

        section[data-testid="stSidebar"] * {
            font-family:
                "Inter",
                "Segoe UI",
                Arial,
                sans-serif !important;
        }


        /* =====================================================
           SIDEBAR NAVIGATION
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] {
            background: #0B1220 !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] ul {
            background: #0B1220 !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] li {
            background: transparent !important;
        }


        /* =====================================================
           NAVIGATION ITEMS
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a {

            display: flex !important;

            align-items: center !important;

            background: #111A2B !important;

            color: #F1F4F7 !important;

            border: 1px solid #202D43 !important;

            border-radius: 12px !important;

            font-size: 15px !important;

            font-weight: 600 !important;

            padding: 14px 15px !important;

            margin: 7px 8px !important;

            opacity: 1 !important;

            box-shadow: none !important;

            transition:
                background 0.2s ease,
                border-color 0.2s ease,
                color 0.2s ease !important;
        }


        /* =====================================================
           NAVIGATION TEXT
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a span {

            color: #F1F4F7 !important;

            opacity: 1 !important;

            font-weight: 600 !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a p {

            color: #F1F4F7 !important;

            opacity: 1 !important;
        }


        /* =====================================================
           HOVER
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a:hover {

            background: #182337 !important;

            border-color: #D8B45A !important;

            color: #D8B45A !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a:hover span {

            color: #D8B45A !important;
        }


        /* =====================================================
           ACTIVE PAGE
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] {

            background: #182337 !important;

            color: #D8B45A !important;

            border: 1px solid #D8B45A !important;

            border-left: 4px solid #D8B45A !important;

            font-weight: 700 !important;

            box-shadow:
                0 0 12px rgba(216, 180, 90, 0.08) !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] span {

            color: #D8B45A !important;

            font-weight: 700 !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] p {

            color: #D8B45A !important;
        }


        /* =====================================================
           NAVIGATION ICONS
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a svg {

            color: #AEB9C8 !important;

            fill: #AEB9C8 !important;

            opacity: 1 !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] svg {

            color: #D8B45A !important;

            fill: #D8B45A !important;
        }


        /* =====================================================
           IMPORTANT
           HIDE STREAMLIT SIDEBAR COLLAPSE ARROW
           
           This hides:
           keyboard_double_arrow_left
        ===================================================== */

        button[data-testid="stSidebarCollapseButton"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }


        /* Streamlit alternate header button */

        button[kind="headerNoPadding"] {
            display: none !important;
        }


        /* =====================================================
           SIDEBAR HEADER
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarHeader"] {

            background: #0B1220 !important;

            min-height: 0 !important;
        }


        /* =====================================================
           DIVIDER
        ===================================================== */

        section[data-testid="stSidebar"] hr {

            border-color: #263247 !important;

            opacity: 1 !important;
        }


        /* =====================================================
           SIDEBAR BUTTONS
        ===================================================== */

        section[data-testid="stSidebar"] button {

            background: #111A2B !important;

            color: #F1F4F7 !important;

            border: 1px solid #263247 !important;

            border-radius: 9px !important;
        }

        section[data-testid="stSidebar"] button:hover {

            background: #182337 !important;

            color: #D8B45A !important;

            border-color: #D8B45A !important;
        }


        /* =====================================================
           INPUTS
        ===================================================== */

        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea {

            background: #111A2B !important;

            color: #F1F4F7 !important;

            border: 1px solid #334158 !important;
        }


        /* =====================================================
           SCROLLBAR
        ===================================================== */

        section[data-testid="stSidebar"] ::-webkit-scrollbar {
            width: 6px;
        }

        section[data-testid="stSidebar"] ::-webkit-scrollbar-track {
            background: #0B1220;
        }

        section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
            background: #334158;
            border-radius: 10px;
        }

        section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb:hover {
            background: #D8B45A;
        }


        /* =====================================================
           GOLD TOP LINE
        ===================================================== */

        section[data-testid="stSidebar"]::before {

            content: "";

            display: block;

            height: 3px;

            width: 100%;

            background:
                linear-gradient(
                    90deg,
                    #8F6D2F,
                    #D8B45A,
                    #8F6D2F
                );
        }


        /* =====================================================
           MOBILE
        ===================================================== */

        @media (max-width: 768px) {

            section[data-testid="stSidebar"] {
                background: #0B1220 !important;
            }

            section[data-testid="stSidebar"]
            [data-testid="stSidebarNav"] a {

                background: #111A2B !important;

                color: #F1F4F7 !important;

                margin: 6px 5px !important;

                padding: 13px 12px !important;
            }

            section[data-testid="stSidebar"]
            [data-testid="stSidebarNav"]
            a[aria-current="page"] {

                background: #182337 !important;

                color: #D8B45A !important;

                border-color: #D8B45A !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )