import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from database import get_user_profile, update_profile, update_password, delete_account


def show_settings_page():
    username = st.session_state.get("username", "")

    # ── CSS ──────────────────────────────────────────────────────────────────
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

#MainMenu, footer, header { visibility: hidden !important; }
section[data-testid="stSidebar"] { display: none !important; }
.stApp { background: #f0fdf4 !important; font-family: 'Nunito', sans-serif; }
.block-container { max-width: 680px !important; padding: 2rem 1.5rem !important; margin: 0 auto !important; }
div[data-testid="stVerticalBlock"] { gap: 0.3rem !important; }

/* Section card */
.settings-card {
    background: white;
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    border: 1.5px solid #d1fae5;
    box-shadow: 0 2px 12px rgba(22,101,52,0.06);
}
.settings-card h3 {
    font-family: 'Playfair Display', serif;
    color: #14532d;
    font-size: 1.05rem;
    margin: 0 0 0.2rem;
}
.settings-card p {
    color: #9ca3af;
    font-size: 0.82rem;
    margin: 0 0 1.2rem;
}

/* Avatar circle */
.avatar {
    width: 72px; height: 72px;
    background: linear-gradient(135deg, #4CAF50, #22c55e);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.9rem;
    margin: 0 auto 0.8rem;
    box-shadow: 0 4px 16px rgba(74,175,80,0.35);
}

/* Inputs */
.stTextInput > label, .stNumberInput > label {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: #374151 !important;
    font-size: 0.84rem !important;
}
.stTextInput input, .stNumberInput input {
    font-family: 'Nunito', sans-serif !important;
    border: 1.5px solid #d1fae5 !important;
    border-radius: 10px !important;
    background: #f9fafb !important;
    font-size: 0.92rem !important;
    padding: 0.62rem 1rem !important;
    color: #1b1b1b !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #4CAF50 !important;
    box-shadow: 0 0 0 3px rgba(74,175,80,0.15) !important;
    background: #fff !important;
}

/* Primary green button */
.stButton > button {
    font-family: 'Nunito', sans-serif !important;
    background: linear-gradient(135deg, #4CAF50, #22c55e) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.62rem 1.6rem !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    width: auto !important;
    cursor: pointer !important;
    transition: filter 0.2s !important;
}
.stButton > button:hover { filter: brightness(1.08) !important; }

/* Danger button */
.danger-btn .stButton > button {
    background: #fff !important;
    color: #dc2626 !important;
    border: 2px solid #fca5a5 !important;
}
.danger-btn .stButton > button:hover {
    background: #fef2f2 !important;
}

/* Logout button */
.logout-btn .stButton > button {
    background: #fff !important;
    color: #374151 !important;
    border: 2px solid #e5e7eb !important;
}
.logout-btn .stButton > button:hover {
    background: #f9fafb !important;
}

/* Back button */
.back-btn .stButton > button {
    background: transparent !important;
    color: #16a34a !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.3rem 0 !important;
    font-size: 0.9rem !important;
}

.stAlert { border-radius: 10px !important; font-family: 'Nunito', sans-serif !important; }
div[data-testid="stExpander"] {
    border: 1.5px solid #fca5a5 !important;
    border-radius: 12px !important;
    background: #fff5f5 !important;
}
</style>
""", unsafe_allow_html=True)

    # ── Back button ───────────────────────────────────────────────────────────
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Back to App", key="back_to_app"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Page title ────────────────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center;margin:0.5rem 0 1.8rem;">
    <div class="avatar">&#9881;</div>
    <h1 style="font-family:'Playfair Display',serif;color:#14532d;
        font-size:1.6rem;margin:0 0 0.2rem;">Account Settings</h1>
    <p style="color:#9ca3af;font-size:0.87rem;font-family:'Nunito',sans-serif;margin:0;">
        Manage your FlashMind AI profile</p>
</div>
""", unsafe_allow_html=True)

    # ── Load profile ──────────────────────────────────────────────────────────
    profile = get_user_profile(username)
    if not profile["success"]:
        st.error("Could not load profile.")
        return

    # ══════════════════════════════════════════════════════════════════════════
    #  1. PROFILE INFO
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
<div class="settings-card">
    <h3>&#128100; Profile Information</h3>
    <p>Update your display name and age</p>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1.6, 1])
    with col1:
        new_name = st.text_input("Full Name",
            value=profile["full_name"],
            placeholder="e.g. Anisha Kumar",
            key="s_name")
    with col2:
        new_age = st.number_input("Age",
            min_value=0, max_value=120,
            value=int(profile["age"]) if profile["age"] else 0,
            key="s_age")

    st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
    if st.button("Save Profile \U0001f4be", key="save_profile"):
        result = update_profile(username, new_name, new_age)
        if result["success"]:
            st.success("✅ " + result["message"])
            st.session_state["full_name"] = new_name
        else:
            st.error(result["message"])

    # ── Username display (read-only) ──────────────────────────────────────────
    st.markdown(f"""
<div style="background:#f0fdf4;border-radius:10px;padding:0.7rem 1rem;
    margin:0.8rem 0 0;border:1px solid #bbf7d0;">
    <span style="font-size:0.8rem;color:#6b7280;font-family:'Nunito',sans-serif;">Username (cannot be changed)</span><br>
    <span style="font-weight:700;color:#166534;font-size:0.95rem;font-family:'Nunito',sans-serif;">@{username}</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  2. CHANGE PASSWORD
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
<div class="settings-card">
    <h3>&#128274; Change Password</h3>
    <p>Use a strong password with at least 6 characters</p>
</div>
""", unsafe_allow_html=True)

    old_pass  = st.text_input("Current Password", type="password", placeholder="Enter current password", key="s_old_pass")
    new_pass  = st.text_input("New Password", type="password", placeholder="At least 6 characters", key="s_new_pass")
    conf_pass = st.text_input("Confirm New Password", type="password", placeholder="Repeat new password", key="s_conf_pass")

    st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
    if st.button("Update Password \U0001f510", key="update_pass"):
        if not old_pass or not new_pass or not conf_pass:
            st.warning("Please fill in all password fields.")
        elif len(new_pass) < 6:
            st.error("New password must be at least 6 characters.")
        elif new_pass != conf_pass:
            st.error("New passwords do not match.")
        else:
            result = update_password(username, old_pass, new_pass)
            if result["success"]:
                st.success("✅ " + result["message"])
            else:
                st.error("❌ " + result["message"])

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  3. LOGOUT
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
<div class="settings-card">
    <h3>&#128682; Session</h3>
    <p>Sign out of your FlashMind AI account</p>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("Logout \U0001f6aa", key="logout_btn"):
        for key in ["logged_in", "username", "full_name", "age", "page"]:
            st.session_state.pop(key, None)
        st.session_state.auth_mode = "login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  4. DELETE ACCOUNT (danger zone)
    # ══════════════════════════════════════════════════════════════════════════
    with st.expander("⚠️ Danger Zone — Delete Account"):
        st.markdown("""
<p style="color:#dc2626;font-size:0.88rem;font-family:'Nunito',sans-serif;
    margin:0 0 0.8rem;font-weight:700;">
    This action is permanent and cannot be undone. All your data will be lost.
</p>
""", unsafe_allow_html=True)
        del_pass = st.text_input("Enter your password to confirm", type="password",
                                  placeholder="Your current password", key="del_pass")

        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
        if st.button("Delete My Account Permanently \U0001f5d1", key="delete_account"):
            if not del_pass:
                st.warning("Please enter your password to confirm.")
            else:
                result = delete_account(username, del_pass)
                if result["success"]:
                    st.success("Account deleted. Goodbye!")
                    import time; time.sleep(1.5)
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error("❌ " + result["message"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
