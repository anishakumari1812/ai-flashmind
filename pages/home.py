"""
pages/home.py – Home page for FlashMind AI.
Allows users to paste notes or upload a PDF, then generates flashcards.
"""

import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.pdf_reader import extract_text_from_pdf, truncate_text


def inject_home_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');

        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

        .stApp {
            background: linear-gradient(160deg, #f0fdf4 0%, #dcfce7 60%, #f9fafb 100%);
        }

        .home-hero {
            background: linear-gradient(135deg, #166534 0%, #16a34a 60%, #4ade80 100%);
            border-radius: 24px;
            padding: 2.4rem 2.8rem;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 8px 32px rgba(22, 101, 52, 0.25);
            position: relative;
            overflow: hidden;
        }
        .home-hero::before {
            content: "";
            position: absolute;
            right: 2rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 5rem;
            opacity: 0.18;
        }
        .home-hero h1 {
            font-family: 'Playfair Display', serif !important;
            font-size: 2.3rem !important;
            margin: 0 0 0.3rem !important;
            color: white !important;
        }
        .home-hero .welcome  { font-size: 1rem; opacity: 0.88; font-weight: 500; }
        .home-hero .subtitle { font-size: 1.05rem; margin-top: 0.7rem; opacity: 0.95; font-weight: 600; }

        .input-card {
            background: white;
            border-radius: 20px;
            padding: 1.8rem;
            border: 1px solid #bbf7d0;
            box-shadow: 0 4px 20px rgba(74,175,80,0.08);
            margin-bottom: 1.4rem;
        }
        .input-card h3 { color: #166534; font-size: 1.05rem; font-weight: 700; margin-bottom: 0.8rem; }

        .stTextArea textarea {
            border: 1.5px solid #bbf7d0 !important;
            border-radius: 14px !important;
            background: #f9fafb !important;
            font-size: 0.9rem !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .stTextArea textarea:focus {
            border-color: #4CAF50 !important;
            box-shadow: 0 0 0 3px rgba(74,175,80,0.15) !important;
        }

        .stFileUploader > div {
            border: 2px dashed #bbf7d0 !important;
            border-radius: 14px !important;
            background: #f0fdf4 !important;
        }

        /* Default button — Generate Flashcards */
        .stButton > button {
            background: linear-gradient(135deg, #4CAF50, #22c55e) !important;
            color: white !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 0.8rem 2.4rem !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            width: 100%;
            transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease !important;
            box-shadow: 0 4px 18px rgba(74,175,80,0.38) !important;
            letter-spacing: 0.03em;
        }
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 10px 28px rgba(74,175,80,0.45) !important;
            filter: brightness(1.07) !important;
        }
        .stButton > button:active { transform: translateY(0px) !important; }

        /* Settings button — frosted pill on hero */
        .settings-btn .stButton > button {
            background: rgba(255,255,255,0.18) !important;
            color: white !important;
            border: 1.5px solid rgba(255,255,255,0.5) !important;
            border-radius: 25px !important;
            padding: 0.4rem 1.1rem !important;
            font-size: 0.85rem !important;
            font-weight: 700 !important;
            width: auto !important;
            box-shadow: none !important;
            letter-spacing: 0;
        }
        .settings-btn .stButton > button:hover {
            background: rgba(255,255,255,0.32) !important;
            transform: none !important;
            box-shadow: none !important;
            filter: none !important;
        }

        /* Pull the settings column up to sit inside the hero */
        div[data-testid="column"]:nth-child(2) {
            position: relative;
            top: -102px;
            margin-bottom: -102px;
            display: flex;
            justify-content: flex-end;
            align-items: flex-start;
            padding-right: 1rem !important;
            z-index: 10;
        }

        .stInfo    { border-radius: 12px !important; }
        .stWarning { border-radius: 12px !important; }
        .stSuccess { border-radius: 12px !important; }

        section[data-testid="stSidebar"] {
            background: #f0fdf4 !important;
            border-right: 1px solid #bbf7d0;
        }
        #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("##  FlashMind AI")
        st.markdown("---")
        st.markdown(f" **{st.session_state.get('username', 'User')}**")
        st.markdown("---")

        if st.button(" My Flashcards"):
            if st.session_state.get("flashcards"):
                st.session_state.page = "flashcards"
                st.rerun()
            else:
                st.warning("Generate flashcards first!")

        if st.button(" Settings"):
            st.session_state.page = "settings"
            st.rerun()

        st.markdown("---")
        if st.button(" Logout"):
            for key in ["logged_in", "username", "flashcards", "study_text"]:
                st.session_state.pop(key, None)
            st.session_state.page = "auth"
            st.rerun()

        st.markdown("---")
        st.caption(" Tip: Upload a PDF or paste your notes to get started!")


def show_home_page():
    inject_home_styles()
    render_sidebar()

    username = st.session_state.get("username", "Student")

    # ── Hero + Settings button ─────────────────────────────────────────────────
    hero_col, btn_col = st.columns([6, 1])

    with hero_col:
        st.markdown(f"""
        <div class="home-hero">
            <h1> FlashMind AI</h1>
            <div class="welcome">Welcome, <strong>{username}</strong> </div>
            <div class="subtitle">How would you like to study today?</div>
        </div>
        """, unsafe_allow_html=True)

    with btn_col:
        st.markdown('<div class="settings-btn">', unsafe_allow_html=True)
        if st.button(" Settings", key="hero_settings_btn"):
            st.session_state.page = "settings"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Input section ──────────────────────────────────────────────────────────
    col1, col2 = st.columns([1.15, 1], gap="large")

    with col1:
        st.markdown("""<div class="input-card"><h3> Paste Your Notes</h3></div>""", unsafe_allow_html=True)
        notes_text = st.text_area(
            label="Your notes",
            placeholder="Paste your study notes, lecture summaries, or any text here…",
            height=240,
            label_visibility="collapsed",
        )

    with col2:
        st.markdown("""<div class="input-card"><h3> Upload a PDF</h3></div>""", unsafe_allow_html=True)
        pdf_file = st.file_uploader(
            label="Upload PDF",
            type=["pdf"],
            help="Upload lecture slides, textbook chapters, or any PDF.",
            label_visibility="collapsed",
        )
        if pdf_file:
            st.success(f" **{pdf_file.name}** uploaded successfully!")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Generate ───────────────────────────────────────────────────────────────
    if st.button(" Generate Flashcards", key="generate_btn"):
        study_text = ""

        if pdf_file:
            with st.spinner(" Extracting text from PDF…"):
                try:
                    study_text = extract_text_from_pdf(pdf_file.read())
                    if not study_text:
                        st.error(" Could not extract text from this PDF. Try pasting the content manually.")
                        return
                    study_text = truncate_text(study_text, max_chars=4000)
                    st.info(f" Extracted **{len(study_text):,}** characters from PDF.")
                except RuntimeError as e:
                    st.error(str(e))
                    return

        elif notes_text.strip():
            study_text = truncate_text(notes_text.strip(), max_chars=4000)

        else:
            st.warning(" Please paste some notes or upload a PDF first.")
            return

        st.session_state.study_text  = study_text
        st.session_state.flashcards  = None
        st.session_state.quiz_data   = None
        st.session_state.card_idx    = 0
        st.session_state.card_flipped = False
        st.session_state.page        = "flashcards"
        st.rerun()