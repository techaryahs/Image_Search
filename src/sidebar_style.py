import streamlit as st


def apply_sidebar_style():

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL SIDEBAR
           ===================================================== */

        section[data-testid="stSidebar"] {
            background: #0B0F14 !important;
            border-right: 1px solid #29313A !important;
        }

        section[data-testid="stSidebar"] > div {
            background: #0B0F14 !important;
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
           SIDEBAR NORMAL TEXT
           ===================================================== */

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {
            color: #E8EDF2 !important;
        }


        /* =====================================================
           SIDEBAR HEADINGS
           ===================================================== */

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #D8B45A !important;
            font-weight: 800 !important;
            letter-spacing: 0.3px !important;
        }


        /* =====================================================
           NAVIGATION CONTAINER
           ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] {
            padding-top: 1rem !important;
        }


        /* =====================================================
           NAVIGATION LINKS
           ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a {
            display: flex !important;
            align-items: center !important;

            color: #DDE4EA !important;

            background: transparent !important;

            border-radius: 10px !important;

            font-family:
                "Inter",
                "Segoe UI",
                Arial,
                sans-serif !important;

            font-size: 15px !important;

            font-weight: 600 !important;

            padding: 0.65rem 0.8rem !important;

            margin: 4px 0 !important;

            transition:
                background 0.2s ease,
                color 0.2s ease,
                border 0.2s ease !important;
        }


        /* =====================================================
           NAVIGATION HOVER
           ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a:hover {
            background: #171D25 !important;

            color: #E1BD67 !important;
        }


        /* =====================================================
           ACTIVE PAGE
           ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] {

            background:
                linear-gradient(
                    90deg,
                    rgba(216, 180, 90, 0.20),
                    rgba(216, 180, 90, 0.05)
                ) !important;

            color: #E1BD67 !important;

            border-left: 3px solid #D8B45A !important;

            font-weight: 750 !important;
        }


        /* =====================================================
           NAVIGATION ICONS
           ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a svg {

            color: #AEB7C2 !important;

            fill: #AEB7C2 !important;
        }


        /* Active icon */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] svg {

            color: #D8B45A !important;

            fill: #D8B45A !important;
        }


        /* =====================================================
           SIDEBAR DIVIDER
           ===================================================== */

        section[data-testid="stSidebar"] hr {

            border-color: #29313A !important;

            margin: 1rem 0 !important;
        }


        /* =====================================================
           SIDEBAR BUTTONS
           ===================================================== */

        section[data-testid="stSidebar"] button {

            background: #151B22 !important;

            color: #E8EDF2 !important;

            border: 1px solid #303944 !important;

            border-radius: 9px !important;

            font-family:
                "Inter",
                "Segoe UI",
                Arial,
                sans-serif !important;

            font-weight: 600 !important;
        }


        section[data-testid="stSidebar"] button:hover {

            background: #1C242D !important;

            border-color: #D8B45A !important;

            color: #E1BD67 !important;
        }


        /* =====================================================
           INPUTS
           ===================================================== */

        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea {

            background: #121820 !important;

            color: #F1F4F7 !important;

            border: 1px solid #303944 !important;

            font-family:
                "Inter",
                "Segoe UI",
                Arial,
                sans-serif !important;
        }


        /* =====================================================
           SIDEBAR SCROLLBAR
           ===================================================== */

        section[data-testid="stSidebar"] ::-webkit-scrollbar {

            width: 6px;
        }


        section[data-testid="stSidebar"] ::-webkit-scrollbar-track {

            background: #0B0F14;
        }


        section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {

            background: #39424D;

            border-radius: 10px;
        }


        section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb:hover {

            background: #D8B45A;
        }


        /* =====================================================
           HIDE STREAMLIT SIDEBAR COLLAPSE ICON
           
           This hides:
           keyboard_double_arrow_left
           ===================================================== */

        button[data-testid="stSidebarCollapseButton"] {

            display: none !important;
        }


        /* =====================================================
           HIDE OLD SIDEBAR COLLAPSE BUTTON
           ===================================================== */

        button[kind="headerNoPadding"] {

            display: none !important;
        }


        /* =====================================================
           SIDEBAR HEADER AREA
           ===================================================== */

        section[data-testid="stSidebar"]
        div[data-testid="stSidebarHeader"] {

            background: #0B0F14 !important;
        }


        /* =====================================================
           SIDEBAR TOP BORDER
           ===================================================== */

        section[data-testid="stSidebar"]::before {

            content: "";

            display: block;

            height: 3px;

            width: 100%;

            background:
                linear-gradient(
                    90deg,
                    #9B7430,
                    #D8B45A,
                    #9B7430
                );
        }

        </style>
        """,
        unsafe_allow_html=True,
    )