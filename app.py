"""
app.py  –  FlashMind AI entry point.

Page routing via st.query_params so the top-nav links work:
    ?page=home | flashcards | quiz | history | logout | settings
"""

import streamlit as st
import os

st.set_page_config(
    page_title  = "FlashMind AI – AI Flashcard Generator",
    page_icon   = "🧠",
    layout      = "wide",
    initial_sidebar_state = "collapsed",
)

from database import init_db
init_db()

# ── Session defaults ──────────────────────────────────────────────────────────
def _init_state():
    for key, default in [
        ("logged_in",   False),
        ("username",    ""),
        ("page",        "auth"),
        ("flashcards",  None),
        ("study_text",  ""),
        ("study_topic", "General"),
        ("quiz_idx",    0),
        ("quiz_score",  0),
        ("quiz_shown",  False),
        ("quiz_done",   False),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

_init_state()

# ── Sync URL params → session page ───────────────────────────────────────────
params   = st.query_params
url_page = params.get("page", "")

if url_page == "logout":
    for k in ["logged_in","username","flashcards","study_text","study_topic",
              "quiz_idx","quiz_score","quiz_shown","quiz_done"]:
        st.session_state[k] = (False if k == "logged_in" else
                                ""    if k in ["username","study_text","study_topic"] else
                                None  if k == "flashcards" else 0)
    st.session_state.page = "auth"
    st.query_params.clear()
    st.rerun()

if url_page and url_page != "logout":
    if st.session_state.logged_in or url_page == "auth":
        st.session_state.page = url_page

# ── Guard unauthenticated access ─────────────────────────────────────────────
if not st.session_state.logged_in:
    st.session_state.page = "auth"

# ── Import pages ──────────────────────────────────────────────────────────────
from auth              import show_auth_page
from pages.home        import show_home_page
from pages.flashcards  import show_flashcards_page
from settings          import show_settings_page   # ← added
# from pages.quiz_page     import show_quiz_page
# from pages.history_page  import show_history_page

# ── Route ─────────────────────────────────────────────────────────────────────
PAGE_MAP = {
    "auth":       show_auth_page,
    "home":       show_home_page,
    "flashcards": show_flashcards_page,
    "settings":   show_settings_page,    # ← added
    # "quiz":       show_quiz_page,
    # "history":    show_history_page,
}

render_fn = PAGE_MAP.get(st.session_state.page, show_auth_page)
render_fn()