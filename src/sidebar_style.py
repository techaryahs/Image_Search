import streamlit as st


def apply_sidebar_style():

    st.markdown(
        """
        <style>

        /* =====================================================
           MAIN SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {
            background: #0B1220 !important;
            color: #F5F7FA !important;
            border-right: 1px solid #263247 !important;
        }

        section[data-testid="stSidebar"] > div {
            background: #0B1220 !important;
        }


        /* =====================================================
           SIDEBAR ALL TEXT
        ===================================================== */

        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] * {
            font-family:
                "Inter",
                "Segoe UI",
                Arial,
                sans-serif !important;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] div {
            color: #F1F4F7 !important;
        }


        /* =====================================================
           SIDEBAR NAVIGATION
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] {
            background: #0B1220 !important;
        }


        /* Every navigation item */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] li {
            background: transparent !important;
        }


        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a {

            background: #111A2B !important;

            color: #F1F4F7 !important;

            border: 1px solid #202D43 !important;

            border-radius: 12px !important;

            font-size: 15px !important;

            font-weight: 600 !important;

            padding: 14px 15px !important;

            margin: 7px 8px !important;

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

            border-color: #8F6D2F !important;

            color: #D8B45A !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a:hover span {

            color: #D8B45A !important;
        }


        /* =====================================================
           ACTIVE PAGE
           
           IMPORTANT:
           Keep this DARK - no light/grey background
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


        /* Active text */

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


        /* Active icon */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] svg {

            color: #D8B45A !important;

            fill: #D8B45A !important;
        }


        /* =====================================================
           SIDEBAR HEADER
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarHeader"] {

            background: #0B1220 !important;
        }


        /* =====================================================
           SIDEBAR COLLAPSE BUTTON
        ===================================================== */

        button[data-testid="stSidebarCollapseButton"] {

            display: flex !important;

            visibility: visible !important;

            opacity: 1 !important;

            background: #111A2B !important;

            color: #D8B45A !important;

            border: 1px solid #334158 !important;

            border-radius: 8px !important;
        }


        button[data-testid="stSidebarCollapseButton"]:hover {

            background: #182337 !important;

            border-color: #D8B45A !important;
        }


        button[data-testid="stSidebarCollapseButton"] svg {

            color: #D8B45A !important;

            fill: #D8B45A !important;
        }


        /* =====================================================
           DIVIDERS
        ===================================================== */

        section[data-testid="stSidebar"] hr {

            border-color: #263247 !important;

            opacity: 1 !important;
        }


        /* =====================================================
           BUTTONS
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
           TOP GOLD LINE
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
           MOBILE SIDEBAR
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