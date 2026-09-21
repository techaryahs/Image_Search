import streamlit as st


def apply_sidebar_style():

    st.markdown(
        """
        <style>

        /* =========================================
           PROFESSIONAL JEWELVISION AI SIDEBAR
           ========================================= */

        /* Sidebar background */

        section[data-testid="stSidebar"] {
            background: linear-gradient(
            180deg,
            #182033 0%,
            #0b101c 100%
        );

            border-right: 1px solid #292e3a;
            width: 260px;
            min-width: 260px;
        }


        /* Sidebar inner spacing */

        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem;
        }


        /* =========================================
           BRAND HEADER
           ========================================= */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]::before {

            content: "💎  JewelVision AI";

            display: block;

            color: #e1c071;

            font-size: 1.35rem;

            font-weight: 800;

            padding: 0.5rem 1rem 1.2rem;

            margin-bottom: 0.8rem;

            border-bottom: 1px solid #292e3a;

            letter-spacing: 0.3px;
            text-shadow: 0 0 12px rgba(225, 192, 113, 0.25);
        }


        /* =========================================
           SIDEBAR MENU
           ========================================= */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a {

            border-radius: 16px;

            margin: 8px 8px;

            padding: 16px 14px;

            min-height: 56px;

            background: rgba(255, 255, 255, 0.025);

            border: 1px solid rgba(255, 255, 255, 0.06);

            color: #e5e7eb;

            font-weight: 600;

            transition:
                background 0.2s ease,
                color 0.2s ease,
                border 0.2s ease,
                box-shadow 0.2s ease;
        }

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a > span:first-child {

        width: 38px;
        height: 38px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background: rgba(225, 192, 113, 0.10);

        margin-right: 10px;
        }

        /* =========================================
           MENU HOVER
           ========================================= */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"] a:hover {

            background: rgba(
                225,
                192,
                113,
                0.15
            );

            color: #e1c071;
        }


        /* =========================================
           ACTIVE PAGE
           ========================================= */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNav"]
        a[aria-current="page"] {

        background: linear-gradient(
            135deg,
            rgba(225, 192, 113, 0.22),
            rgba(225, 192, 113, 0.08)
        );

        color: #e1c071;

        border: 1px solid rgba(225, 192, 113, 0.35);

        border-left: 3px solid #e1c071;

        box-shadow:
        0 0 18px rgba(225, 192, 113, 0.12);
        }


        /* =========================================
           MOBILE SIDEBAR
           ========================================= */

        @media (max-width: 700px) {

            section[data-testid="stSidebar"] {
                width: 230px;
            }

            section[data-testid="stSidebar"]
            [data-testid="stSidebarNav"] a {

                margin: 4px 5px;

                padding: 10px;

                font-size: 0.95rem;
            }

            section[data-testid="stSidebar"]
            [data-testid="stSidebarNav"]::before {

                font-size: 1.15rem;

                padding:
                    0.4rem
                    0.7rem
                    1rem;
            }
        }


        </style>
        """,
        unsafe_allow_html=True,
    )