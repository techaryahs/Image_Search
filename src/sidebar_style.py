import streamlit as st


def apply_sidebar_style():

    st.markdown(
        """
        <style>

        /* =========================================
           SIDEBAR
        ========================================= */

        section[data-testid="stSidebar"] {
            background: #0B0F14 !important;
            border-right: 1px solid #303640 !important;
        }

        section[data-testid="stSidebar"] > div {
            background: #0B0F14 !important;
        }


        /* =========================================
           SIDEBAR FONT
        ========================================= */

        section[data-testid="stSidebar"] * {
            font-family:
                "Inter",
                "Segoe UI",
                Arial,
                sans-serif !important;
        }


        /* =========================================
           NAVIGATION LINKS
        ========================================= */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a {

            color: #E8EDF2 !important;

            font-size: 15px !important;

            font-weight: 600 !important;

            border-radius: 10px !important;

            padding: 0.65rem 0.8rem !important;

            margin: 4px 0 !important;

            background: transparent !important;
        }


        /* =========================================
           HOVER
        ========================================= */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a:hover {

            background: #171D25 !important;

            color: #D8B45A !important;
        }


        /* =========================================
           ACTIVE PAGE
        ========================================= */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] {

            background: rgba(216, 180, 90, 0.15) !important;

            color: #D8B45A !important;

            border-left: 3px solid #D8B45A !important;

            font-weight: 750 !important;
        }


        /* =========================================
           NAVIGATION ICONS
        ========================================= */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a svg {

            color: #AEB7C2 !important;

            fill: #AEB7C2 !important;
        }


        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] svg {

            color: #D8B45A !important;

            fill: #D8B45A !important;
        }


        /* =========================================
           SIDEBAR HEADER
        ========================================= */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarHeader"] {

            background: #0B0F14 !important;
        }


        /* =========================================
           IMPORTANT:
           DO NOT HIDE COLLAPSE BUTTON
        ========================================= */

        button[data-testid="stSidebarCollapseButton"] {

            display: flex !important;

            visibility: visible !important;

            opacity: 1 !important;

            color: #D8B45A !important;

            background: #151B22 !important;

            border: 1px solid #303944 !important;

            border-radius: 8px !important;
        }


        button[data-testid="stSidebarCollapseButton"]:hover {

            background: #1D252E !important;

            border-color: #D8B45A !important;
        }


        button[data-testid="stSidebarCollapseButton"] svg {

            color: #D8B45A !important;

            fill: #D8B45A !important;
        }


        /* =========================================
           DIVIDER
        ========================================= */

        section[data-testid="stSidebar"] hr {

            border-color: #29313A !important;
        }


        /* =========================================
           SCROLLBAR
        ========================================= */

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

        </style>
        """,
        unsafe_allow_html=True,
    )