"""
pages/flashcards.py – Flashcard display page for FlashMind AI.
UI: Centered flip cards with prev/next navigation + 10-question quiz tab.
"""

import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.llm import generate_flashcards_safe, generate_quiz_safe


def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(160deg,#f0fdf4 0%,#dcfce7 60%,#f9fafb 100%); }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background:#f0fdf4 !important; border-right:1px solid #bbf7d0; }

/* ── Header ── */
.fc-header {
    background: linear-gradient(135deg,#14532d 0%,#166534 50%,#15803d 100%);
    border-radius: 20px; padding: 1.8rem 2.2rem;
    margin-bottom: 1.6rem; color: white;
    box-shadow: 0 6px 28px rgba(20,83,45,0.28);
}
.fc-header h1 { font-family:'Playfair Display',serif !important; font-size:1.9rem !important; margin:0 !important; color:white !important; }
.fc-header p  { margin:0.3rem 0 0 !important; opacity:0.88; font-size:0.95rem; }
.badge { display:inline-block; background:rgba(255,255,255,0.22); border:1px solid rgba(255,255,255,0.35); border-radius:30px; padding:0.22rem 0.85rem; font-size:0.8rem; font-weight:700; margin-top:0.5rem; }

/* ── Flip Card ── */
.flip-card-wrap {
    perspective: 1200px;
    width: 100%; max-width: 560px;
    height: 300px;
    margin: 0 auto 1.2rem;
    cursor: pointer;
}
.flip-card-inner {
    position: relative; width: 100%; height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.55s cubic-bezier(0.4,0.2,0.2,1);
}
.flip-card-inner.flipped { transform: rotateY(180deg); }
.flip-card-front, .flip-card-back {
    position: absolute; inset: 0;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 22px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 2.2rem;
    text-align: center;
}
.flip-card-front {
    background: white;
    border: 1.5px solid #bbf7d0;
    box-shadow: 0 8px 32px rgba(74,175,80,0.13);
}
.flip-card-back {
    background: linear-gradient(135deg,#166534,#15803d);
    transform: rotateY(180deg);
    box-shadow: 0 8px 32px rgba(20,83,45,0.22);
}
.flip-card-front .q-label {
    font-size:0.75rem; font-weight:700; color:#4CAF50;
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.8rem;
}
.flip-card-front .q-text {
    font-size:1.15rem; font-weight:700; color:#14532d; line-height:1.5;
}
.flip-card-front .hint {
    position:absolute; bottom:1.1rem;
    font-size:0.75rem; color:#9ca3af;
}
.flip-card-back .a-label {
    font-size:0.75rem; font-weight:700; color:rgba(255,255,255,0.7);
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.8rem;
}
.flip-card-back .a-text {
    font-size:1.05rem; color:white; line-height:1.6; font-weight:500;
}

/* ── Card counter ── */
.card-counter {
    text-align:center; font-size:0.9rem; font-weight:700;
    color:#166534; margin-bottom:0.8rem;
}
.progress-dots {
    display:flex; justify-content:center; gap:6px; margin-bottom:1.4rem;
}
.dot { width:8px; height:8px; border-radius:50%; background:#d1fae5; transition:background 0.2s; }
.dot.active { background:#4CAF50; width:22px; border-radius:4px; }

/* ── Nav buttons ── */
.nav-row .stButton > button {
    border-radius:12px !important; font-weight:700 !important;
    padding:0.6rem 1.4rem !important; font-size:0.92rem !important;
    transition:all 0.18s !important;
}

/* ── Quiz styles ── */
.quiz-question {
    background:white; border-radius:18px; padding:1.8rem 2rem;
    border:1.5px solid #bbf7d0;
    box-shadow:0 4px 18px rgba(74,175,80,0.1);
    margin-bottom:1.2rem;
}
.quiz-q-text { font-size:1.1rem; font-weight:700; color:#14532d; margin-bottom:1.2rem; line-height:1.5; }
.quiz-counter { font-size:0.8rem; color:#9ca3af; font-weight:600; float:right; }

.stRadio > label { font-weight:600 !important; color:#166534 !important; }
div[data-testid="stRadio"] > div { gap:0.3rem !important; }
div[data-testid="stRadio"] label {
    background:#f0fdf4 !important; border:1.5px solid #d1fae5 !important;
    border-radius:10px !important; padding:0.55rem 1rem !important;
    font-size:0.93rem !important; cursor:pointer !important;
    transition:background 0.15s !important;
}
div[data-testid="stRadio"] label:hover { background:#dcfce7 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background:#e8f5e9; border-radius:12px; padding:4px; gap:4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius:9px !important; font-weight:700 !important;
    color:#4b7a53 !important; padding:0.45rem 1.4rem !important;
    font-size:0.92rem !important;
}
.stTabs [aria-selected="true"] {
    background:#2e7d32 !important; color:#fff !important;
}
.stTabs [data-baseweb="tab-border"] { display:none !important; }

/* ── Buttons ── */
.stButton > button {
    border-radius:14px !important; font-weight:700 !important;
    transition:all 0.18s !important;
}
.primary-btn .stButton > button {
    background:linear-gradient(135deg,#4CAF50,#22c55e) !important;
    color:white !important; border:none !important;
    box-shadow:0 4px 16px rgba(74,175,80,0.35) !important;
}
.primary-btn .stButton > button:hover { filter:brightness(1.07) !important; transform:translateY(-2px) !important; }
.outline-btn .stButton > button {
    background:white !important; color:#166534 !important;
    border:2px solid #4CAF50 !important;
}
.outline-btn .stButton > button:hover { background:#f0fdf4 !important; }

.stAlert { border-radius:12px !important; }
</style>
""", unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🧠 FlashMind AI")
        st.markdown("---")
        st.markdown(f"👤 **{st.session_state.get('username','User')}**")
        st.markdown("---")
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.rerun()
        if st.button("⚙️ Settings"):
            st.session_state.page = "settings"
            st.rerun()
        st.markdown("---")
        if st.button("🚪 Logout"):
            for k in ["logged_in","username","flashcards","study_text","quiz_data"]:
                st.session_state.pop(k, None)
            st.session_state.page = "auth"
            st.rerun()
        cards = st.session_state.get("flashcards")
        if cards:
            st.markdown("---")
            st.markdown("### 📊 Stats")
            st.metric("Flashcards", len(cards))
            quiz = st.session_state.get("quiz_data")
            if quiz:
                st.metric("Quiz Questions", len(quiz))


def show_flashcards_page():
    inject_styles()
    render_sidebar()

    # ── Generate flashcards if needed ─────────────────────────────────────────
    if not st.session_state.get("flashcards"):
        study_text = st.session_state.get("study_text","")
        if not study_text:
            st.warning("No study content found. Please go back to Home and add your notes.")
            if st.button("← Back to Home"):
                st.session_state.page = "home"
                st.rerun()
            return
        with st.spinner("🤖 AI is generating your flashcards (min 15)…"):
            try:
                st.session_state.flashcards = generate_flashcards_safe(study_text)
                st.session_state.card_idx = 0
                st.session_state.card_flipped = False
            except RuntimeError as e:
                st.error(f"❌ {e}")
                if st.button("← Back to Home"):
                    st.session_state.page = "home"
                    st.rerun()
                return

    # ── Generate quiz if needed ───────────────────────────────────────────────
    if not st.session_state.get("quiz_data"):
        study_text = st.session_state.get("study_text","")
        if study_text:
            with st.spinner("🧪 Generating 10 quiz questions…"):
                try:
                    st.session_state.quiz_data = generate_quiz_safe(study_text)
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                except Exception:
                    st.session_state.quiz_data = []

    flashcards = st.session_state.flashcards
    quiz_data  = st.session_state.get("quiz_data", [])

    # ── Init nav state ────────────────────────────────────────────────────────
    if "card_idx" not in st.session_state:
        st.session_state.card_idx = 0
    if "card_flipped" not in st.session_state:
        st.session_state.card_flipped = False

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(f"""
<div class="fc-header">
    <h1>📚 Your Flashcards</h1>
    <p>Click a card to flip and reveal the answer.</p>
    <span class="badge">✅ {len(flashcards)} cards</span>
    {'<span class="badge" style="margin-left:0.5rem;">🧪 10 quiz questions</span>' if quiz_data else ''}
</div>
""", unsafe_allow_html=True)

    if not os.getenv("GROQ_API_KEY"):
        st.markdown("""
<div style="background:#fef9c3;border:1px solid #fde047;border-radius:14px;
    padding:0.9rem 1.3rem;margin-bottom:1.2rem;font-size:0.88rem;color:#713f12;">
    🟡 <strong>Demo Mode</strong> – No <code>GROQ_API_KEY</code> found. Set it in your .env to generate real cards.
</div>
""", unsafe_allow_html=True)

    # ── Tabs: Flashcards | Quiz ───────────────────────────────────────────────
    tab_fc, tab_quiz = st.tabs(["📖  Flashcards", "🧪  Quiz"])

    # ══════════════════════════════════════════════════════════════════════════
    #  FLASHCARDS TAB
    # ══════════════════════════════════════════════════════════════════════════
    with tab_fc:
        idx     = st.session_state.card_idx
        flipped = st.session_state.card_flipped
        card    = flashcards[idx]
        total   = len(flashcards)

        # Counter
        st.markdown(f'<div class="card-counter">{idx+1} / {total}</div>', unsafe_allow_html=True)

        # Progress dots (show up to 15, then abbreviate)
        dots_html = '<div class="progress-dots">'
        show = min(total, 15)
        for i in range(show):
            dots_html += f'<div class="dot {"active" if i==idx else ""}"></div>'
        if total > 15:
            dots_html += '<span style="font-size:0.7rem;color:#9ca3af;align-self:center;">…</span>'
        dots_html += '</div>'
        st.markdown(dots_html, unsafe_allow_html=True)

        # ── Flip card (HTML + JS) ─────────────────────────────────────────────
        flipped_class = "flipped" if flipped else ""
        q = card['question'].replace("'","&#39;").replace('"','&quot;')
        a = card['answer'].replace("'","&#39;").replace('"','&quot;')

        st.markdown(f"""
<div class="flip-card-wrap" onclick="
    var inner = this.querySelector('.flip-card-inner');
    inner.classList.toggle('flipped');
" title="Click to flip">
    <div class="flip-card-inner {flipped_class}">
        <div class="flip-card-front">
            <div class="q-label">Question {idx+1}</div>
            <div class="q-text">{q}</div>
            <div class="hint">👆 Click to reveal answer</div>
        </div>
        <div class="flip-card-back">
            <div class="a-label">Answer</div>
            <div class="a-text">{a}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

        # ── Navigation buttons ────────────────────────────────────────────────
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])

        with c1:
            st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
            if st.button("← Prev", key="prev_btn", use_container_width=True,
                         disabled=(idx == 0)):
                st.session_state.card_idx = idx - 1
                st.session_state.card_flipped = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
<div style="text-align:center;padding:0.5rem 0;">
    <span style="font-size:0.85rem;color:#6b7280;font-weight:600;">
        {idx+1} of {total} cards
    </span>
</div>""", unsafe_allow_html=True)

        with c3:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            if st.button("Next →", key="next_btn", use_container_width=True,
                         disabled=(idx == total - 1)):
                st.session_state.card_idx = idx + 1
                st.session_state.card_flipped = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Flip toggle button
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            flip_label = "👁 Show Answer" if not flipped else "🔄 Show Question"
            if st.button(flip_label, key="flip_btn", use_container_width=True):
                st.session_state.card_flipped = not st.session_state.card_flipped
                st.rerun()

        st.markdown("---")
        col_back, col_regen = st.columns(2)
        with col_back:
            st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
            if st.button("← Back to Home", use_container_width=True, key="back_home"):
                st.session_state.page = "home"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_regen:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            if st.button("🔄 Regenerate", use_container_width=True, key="regen"):
                st.session_state.flashcards = None
                st.session_state.quiz_data   = None
                st.session_state.card_idx    = 0
                st.session_state.card_flipped = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  QUIZ TAB
    # ══════════════════════════════════════════════════════════════════════════
    with tab_quiz:
        if not quiz_data:
            st.info("Quiz questions could not be generated. Try regenerating.")
        else:
            if "quiz_answers" not in st.session_state:
                st.session_state.quiz_answers = {}
            if "quiz_submitted" not in st.session_state:
                st.session_state.quiz_submitted = False

            submitted = st.session_state.quiz_submitted

            st.markdown(f"""
<div style="background:white;border-radius:16px;padding:1.2rem 1.6rem;
    border:1.5px solid #bbf7d0;margin-bottom:1.4rem;
    box-shadow:0 2px 12px rgba(74,175,80,0.08);">
    <span style="font-weight:700;color:#14532d;font-size:1rem;">
        🧪 Quiz — {len(quiz_data)} Questions
    </span><br>
    <span style="font-size:0.85rem;color:#6b7280;">
        Answer all questions then click Submit to see your score.
    </span>
</div>
""", unsafe_allow_html=True)

            for i, q in enumerate(quiz_data):
                ans_key = f"q_{i}"
                user_ans = st.session_state.quiz_answers.get(ans_key)
                correct  = q["answer"]

                with st.container():
                    st.markdown(f"""
<div class="quiz-question">
    <span class="quiz-counter">{i+1}/{len(quiz_data)}</span>
    <div class="quiz-q-text">Q{i+1}. {q['question']}</div>
</div>
""", unsafe_allow_html=True)

                    chosen = st.radio(
                        label=f"q{i+1}",
                        options=q["options"],
                        index=q["options"].index(user_ans) if user_ans in q["options"] else None,
                        key=f"radio_{i}",
                        label_visibility="collapsed",
                        disabled=submitted,
                    )
                    st.session_state.quiz_answers[ans_key] = chosen

                    # Show result after submit
                    if submitted and chosen:
                        if chosen == correct:
                            st.success(f"✅ Correct! — {q['explanation']}")
                        else:
                            st.error(f"❌ Incorrect. Correct answer: **{correct}**\n\n{q['explanation']}")

                    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

            if not submitted:
                _, mid, _ = st.columns([1, 2, 1])
                with mid:
                    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                    if st.button("Submit Quiz ✅", key="submit_quiz", use_container_width=True):
                        answered = sum(1 for v in st.session_state.quiz_answers.values() if v)
                        if answered < len(quiz_data):
                            st.warning(f"Please answer all {len(quiz_data)} questions first. ({answered}/{len(quiz_data)} answered)")
                        else:
                            st.session_state.quiz_submitted = True
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Score
                score = sum(
                    1 for i, q in enumerate(quiz_data)
                    if st.session_state.quiz_answers.get(f"q_{i}") == q["answer"]
                )
                pct = int(score / len(quiz_data) * 100)
                color = "#16a34a" if pct >= 70 else "#d97706" if pct >= 40 else "#dc2626"
                st.markdown(f"""
<div style="background:white;border-radius:18px;padding:1.6rem 2rem;text-align:center;
    border:2px solid {color};margin:1rem 0;box-shadow:0 4px 18px rgba(0,0,0,0.07);">
    <div style="font-size:2.5rem;font-weight:800;color:{color};">{score}/{len(quiz_data)}</div>
    <div style="font-size:1.1rem;font-weight:700;color:#374151;margin-top:0.3rem;">{pct}% Score</div>
    <div style="font-size:0.88rem;color:#6b7280;margin-top:0.3rem;">
        {"🎉 Excellent work!" if pct>=80 else "👍 Good effort!" if pct>=60 else "📖 Keep studying!"}
    </div>
</div>
""", unsafe_allow_html=True)

                _, mid, _ = st.columns([1, 2, 1])
                with mid:
                    st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
                    if st.button("🔄 Retake Quiz", key="retake", use_container_width=True):
                        st.session_state.quiz_answers   = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)