# src/sidebar_style.py

import streamlit as st


def apply_sidebar_style():

    st.markdown(
        """
        <style>

        /* =====================================================
           SIDEBAR MAIN
           ===================================================== */

        section[data-testid="stSidebar"] {
            background: #0b0f14 !important;
            border-right: 1px solid #2d333b !important;
        }


        /* Sidebar inner container */

        section[data-testid="stSidebar"] > div {
            background: #0b0f14 !important;
        }


        /* =====================================================
           SIDEBAR TEXT
           ===================================================== */

        section[data-testid="stSidebar"] * {
            font-family:
                "Inter",
                "Segoe UI",
                Arial,
                sans-serif !important;
        }


        /* Normal text */

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {
            color: #e8edf2 !important;
        }


        /* =====================================================
           SIDEBAR TITLE / BRAND
           ===================================================== */

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #d8b45a !important;
            font-weight: 800 !important;
            letter-spacing: 0.3px !important;
        }


        /* =====================================================
           NAVIGATION
           ===================================================== */

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }


        /* Navigation links */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a {
            color: #dfe5eb !important;
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

            margin: 3px 0 !important;

            transition:
                background 0.2s ease,
                color 0.2s ease !important;
        }


        /* Navigation hover */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a:hover {
            background: #171d25 !important;
            color: #e1bd67 !important;
        }


        /* Active navigation */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] {
            background:
                linear-gradient(
                    90deg,
                    rgba(216, 180, 90, 0.18),
                    rgba(216, 180, 90, 0.05)
                ) !important;

            color: #e1bd67 !important;

            border-left: 3px solid #d8b45a !important;

            font-weight: 750 !important;
        }


        /* Active navigation icon */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] svg {
            fill: #d8b45a !important;
            color: #d8b45a !important;
        }


        /* Normal navigation icons */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        svg {
            color: #aeb7c2 !important;
        }


        /* =====================================================
           SIDEBAR DIVIDER
           ===================================================== */

        section[data-testid="stSidebar"] hr {
            border-color: #29313a !important;
            margin: 1rem 0 !important;
        }


        /* =====================================================
           SIDEBAR BUTTONS
           ===================================================== */

        section[data-testid="stSidebar"] button {
            background: #151b22 !important;
            color: #e8edf2 !important;

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
            background: #1c242d !important;
            border-color: #d8b45a !important;
            color: #e1bd67 !important;
        }


        /* =====================================================
           SELECTBOX / INPUTS
           ===================================================== */

        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea {
            background: #121820 !important;
            color: #f1f4f7 !important;

            border: 1px solid #303944 !important;

            font-family:
                "Inter",
                "Segoe UI",
                Arial,
                sans-serif !important;
        }


        /* =====================================================
           SCROLLBAR
           ===================================================== */

        section[data-testid="stSidebar"] ::-webkit-scrollbar {
            width: 6px;
        }

        section[data-testid="stSidebar"] ::-webkit-scrollbar-track {
            background: #0b0f14;
        }

        section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
            background: #39424d;
            border-radius: 10px;
        }

        section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb:hover {
            background: #d8b45a;
        }


        /* =====================================================
           SIDEBAR COLLAPSE BUTTON
           ===================================================== */

        button[data-testid="stBaseButton-headerNoPadding"] {
            color: #d8b45a !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )