import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from database import create_user, login_user, init_db

init_db()

def show_login_page():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

#MainMenu,footer,header{visibility:hidden!important;}
section[data-testid="stSidebar"]{display:none!important;}
.stApp{background:#eef2ee!important;}
.block-container{padding:0!important;max-width:100%!important;margin:0!important;}
div[data-testid="stVerticalBlock"]{gap:0!important;}

/* ── Two columns full height ── */
div[data-testid="stHorizontalBlock"]{
    gap:0!important;flex-wrap:nowrap!important;
    min-height:100vh!important;align-items:stretch!important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]{
    padding:0!important;min-height:100vh!important;
}

/* ── LEFT col: soft green bg, flex center ── */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child{
    background:#eef2ee!important;
    display:flex!important;align-items:center!important;
    justify-content:center!important;flex-direction:column!important;
}

/* ── RIGHT col: dark green gradient ── */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child{
    background:linear-gradient(150deg,#2d6a30 0%,#1a5c20 55%,#0f3d14 100%)!important;
}

/* ── Inner vertical stack — center all children ── */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child
> div[data-testid="stVerticalBlock"]{
    display:flex!important;flex-direction:column!important;
    align-items:center!important;gap:0!important;
    padding:0!important;width:100%!important;
}

/* ── Fix all widgets to 360px centered ── */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stTextInput,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stButton,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stAlert,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .element-container{
    width:360px!important;max-width:360px!important;
}

/* ── Input label: left-aligned, bold, dark ── */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stTextInput label,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stTextInput label p,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stTextInput label span,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child [data-testid="stTextInputRootElement"] label,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child [data-testid="stTextInputRootElement"] label p{
    font-family:'Nunito',sans-serif!important;
    font-weight:700!important;
    color:#2d3748!important;
    font-size:0.87rem!important;
    text-align:left!important;
    display:block!important;
    width:100%!important;
}

/* ── Input box ── */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stTextInput input,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child [data-testid="stTextInputRootElement"] input{
    font-family:'Nunito',sans-serif!important;
    border:1.5px solid #c6dbc6!important;
    border-radius:10px!important;
    background:#ffffff!important;
    font-size:0.93rem!important;
    padding:0.68rem 1rem!important;
    color:#374151!important;
    text-align:left!important;
    width:100%!important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stTextInput input::placeholder,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child [data-testid="stTextInputRootElement"] input::placeholder{
    color:#a0aec0!important;
    text-align:left!important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stTextInput input:focus,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child [data-testid="stTextInputRootElement"] input:focus{
    border-color:#4CAF50!important;
    box-shadow:0 0 0 3px rgba(74,175,80,0.15)!important;
    background:#fff!important;
}

/* ── Login button: full width, green ── */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stButton > button{
    font-family:'Nunito',sans-serif!important;
    background:linear-gradient(135deg,#4CAF50,#38a169)!important;
    color:white!important;border:none!important;border-radius:10px!important;
    padding:0.75rem 1.4rem!important;font-size:0.97rem!important;
    font-weight:700!important;width:100%!important;cursor:pointer!important;
    letter-spacing:0.02em!important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stButton > button:hover{
    filter:brightness(1.08)!important;
}

/* ── Create account: outline style ── */
.outline-btn .stButton > button{
    background:#ffffff!important;
    color:#38a169!important;
    border:1.5px solid #4CAF50!important;
    font-weight:700!important;
}
.outline-btn .stButton > button:hover{
    background:#f0fdf4!important;
}

/* ── Right panel ── */
.rp-wrap{width:100%;min-height:100vh;display:flex;flex-direction:column;
    align-items:center;justify-content:center;padding:2.5rem 2rem;
    position:relative;overflow:hidden;}
.rp-b1{position:absolute;width:260px;height:260px;background:rgba(255,255,255,0.06);
    border-radius:50%;top:-70px;right:-70px;}
.rp-b2{position:absolute;width:160px;height:160px;background:rgba(255,255,255,0.05);
    border-radius:50%;bottom:-40px;left:-40px;}
.rp-card{background:rgba(255,255,255,0.13);border:1.5px solid rgba(255,255,255,0.28);
    border-radius:24px;padding:2rem 1.8rem;text-align:center;
    width:100%;max-width:290px;position:relative;z-index:2;}
.rp-notes{height:76px;position:relative;display:flex;align-items:center;
    justify-content:center;margin-bottom:1.3rem;}
.rp-ny{width:52px;height:48px;background:#fef08a;border-radius:7px;
    transform:rotate(-9deg);position:absolute;left:calc(50% - 48px);top:8px;
    box-shadow:2px 4px 12px rgba(0,0,0,0.2);}
.rp-ng{width:52px;height:48px;background:#86efac;border-radius:7px;
    transform:rotate(6deg);position:absolute;left:calc(50% - 4px);top:8px;
    box-shadow:2px 4px 12px rgba(0,0,0,0.2);}
.rp-nb{width:54px;height:50px;background:#7dd3fc;border-radius:9px;
    transform:rotate(-1deg);position:absolute;left:calc(50% - 27px);top:2px;
    display:flex;align-items:center;justify-content:center;font-size:1.5rem;
    box-shadow:2px 4px 12px rgba(0,0,0,0.2);}
.rp-card h2{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:800;
    color:#fff;margin:0 0 0.4rem;line-height:1.3;}
.rp-sub{font-size:0.82rem;color:rgba(255,255,255,0.85);line-height:1.6;margin:0 0 1.2rem;}
.rp-pills{display:flex;flex-direction:column;gap:10px;text-align:left;margin-bottom:1.2rem;}
.rp-pill{background:rgba(255,255,255,0.18);border-radius:25px;padding:0.48rem 0.9rem;
    color:#fff;font-size:0.79rem;font-weight:700;display:flex;align-items:center;gap:7px;}
.rp-dots{display:flex;justify-content:center;gap:5px;}
.rp-dl{width:20px;height:6px;background:#fff;border-radius:3px;}
.rp-d{width:6px;height:6px;background:rgba(255,255,255,0.35);border-radius:50%;}
.rp-pw{margin-top:1.6rem;font-size:0.65rem;font-weight:700;color:rgba(255,255,255,0.5);
    letter-spacing:0.12em;text-transform:uppercase;font-family:'Nunito',sans-serif;
    position:relative;z-index:2;}

/* ── Left panel decorative ── */
.brand-txt{
    font-family:'Playfair Display',serif;
    font-size:1.1rem;color:#2f6b35;font-weight:700;
    width:360px;text-align:left;
    margin-top:2rem;
    margin-bottom:1.2rem;
    display:block;
}
.login-hdr{
    background:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:18px;
    box-shadow:0 2px 20px rgba(0,0,0,0.07);
    padding:1.8rem 2rem 1.5rem;
    width:360px;text-align:center;
    margin-bottom:1.2rem;
}
.login-hdr h1{
    font-family:'Playfair Display',serif;
    font-size:1.9rem;font-weight:800;color:#1a202c;margin:0 0 0.35rem;
}
.login-hdr p{font-size:0.84rem;color:#a0aec0;margin:0;}
.or-row{display:flex;align-items:center;gap:10px;width:360px;margin:1.2rem 0 0.8rem;}
.or-line{flex:1;height:1px;background:#e2e8f0;}
.or-txt{font-size:0.78rem;color:#a0aec0;font-family:'Nunito',sans-serif;}
.no-acct{text-align:center;color:#718096;font-size:0.83rem;
    margin-top:0;margin-bottom:0.8rem;font-family:'Nunito',sans-serif;width:360px;}
.stAlert{border-radius:10px!important;}

/* ── Spacing for inputs and buttons in left col ── */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stTextInput{
    margin-bottom:0.8rem!important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child .stButton{
    margin-top:0.8rem!important;
    margin-bottom:0.4rem!important;
}
</style>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="small")

    # ── RIGHT: completely unchanged ───────────────────────────────────────────
    with col2:
        st.markdown("""<div class="rp-wrap">
<div class="rp-b1"></div><div class="rp-b2"></div>
<div class="rp-card">
<div class="rp-notes"><div class="rp-ny"></div><div class="rp-ng"></div>
<div class="rp-nb">&#129504;</div></div>
<h2>Smarter studying<br>starts here</h2>
<p class="rp-sub">Turn your notes into powerful<br>insights with AI</p>
<div class="rp-pills">
<div class="rp-pill">&#128196; Paste notes or upload PDF</div>
<div class="rp-pill">&#9889; Instant AI flashcards</div>
<div class="rp-pill">&#127919; 5&#8211;10 targeted Q&amp;A cards</div>
</div>
<div class="rp-dots"><div class="rp-dl"></div><div class="rp-d"></div>
<div class="rp-d"></div></div>
</div>
<p class="rp-pw">Turn your notes into quizzes & flashcards instantly using AI</p>
</div>""", unsafe_allow_html=True)

    # ── LEFT: exactly matching reference screenshot ────────────────────────────
    with col1:
        # Top spacer — pushes content down from top
        st.markdown("<div style='height:2vh'></div>", unsafe_allow_html=True)

        st.markdown('<span class="brand-txt">FlashMind AI</span>',
                    unsafe_allow_html=True)

        # Space between brand and card
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        st.markdown("""<div class="login-hdr">
<h1>Welcome!</h1>
<p>Please enter your details to continue.</p>
</div>""", unsafe_allow_html=True)

        # Space between card and inputs
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        username = st.text_input("Email / Username",
            placeholder="Enter your username", key="signup_user")

        # Space between username and password
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        password = st.text_input("Password", type="password",
            placeholder="Enter your password", key="signup_pass")

        # Space between password and login button
        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

        if st.button("Login →", key="login_btn"):
            if not username or not password:
                st.warning("Please fill in all fields.")
            else:
                result = login_user(username, password)
                if result["success"]:
                    st.session_state.logged_in = True
                    st.session_state.username = result["username"]
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.error(result["message"])

        # Space + or divider
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        st.markdown("""<div class="or-row">
<div class="or-line"></div><span class="or-txt">or</span><div class="or-line"></div>
</div>""", unsafe_allow_html=True)

        # Space between or and "Don't have account"
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        st.markdown('<p class="no-acct">Don\'t have an account?</p>', unsafe_allow_html=True)

        # Space between text and create account button
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

        st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
        if st.button("✨ Create account", key="to_signup"):
            st.session_state.auth_mode = "signup"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Bottom spacer — equal to top for vertical centering
        st.markdown("<div style='height:2vh'></div>", unsafe_allow_html=True)


# ── SIGNUP PAGE: completely unchanged ────────────────────────────────────────
def show_signup_page():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Playfair+Display:wght@700;800&display=swap');
#MainMenu,footer,header{visibility:hidden!important;}
section[data-testid="stSidebar"]{display:none!important;}
.stApp{background:linear-gradient(135deg,#f0fdf4,#dcfce7,#f0fdf4)!important;}
.block-container{max-width:460px!important;padding:2rem 1rem!important;margin:0 auto!important;}
div[data-testid="stVerticalBlock"]{gap:0!important;}
.stTextInput label{font-family:'Nunito',sans-serif!important;font-weight:700!important;
    color:#374151!important;font-size:0.85rem!important;}
.stTextInput input{font-family:'Nunito',sans-serif!important;
    border:1.5px solid #d1fae5!important;border-radius:9px!important;
    background:#f9fafb!important;font-size:0.92rem!important;
    padding:0.62rem 0.9rem!important;color:#1b1b1b!important;}
.stTextInput input:focus{border-color:#4CAF50!important;
    box-shadow:0 0 0 3px rgba(74,175,80,0.15)!important;background:#fff!important;}
.stButton>button{font-family:'Nunito',sans-serif!important;
    background:linear-gradient(135deg,#4CAF50,#22c55e)!important;color:white!important;
    border:none!important;border-radius:10px!important;padding:0.72rem!important;
    font-size:0.95rem!important;font-weight:700!important;width:100%!important;cursor:pointer!important;}
.outline-btn .stButton>button{background:#fff!important;color:#16a34a!important;
    border:2px solid #4CAF50!important;}
.stAlert{border-radius:10px!important;}
</style>
""", unsafe_allow_html=True)

    st.markdown("""<div style="background:white;border-radius:24px;
padding:2.2rem 2rem 1.2rem;border:1.5px solid #d1fae5;
box-shadow:0 8px 40px rgba(22,101,52,0.13);text-align:center;margin-bottom:1rem;">
<div style="width:52px;height:52px;background:linear-gradient(135deg,#4CAF50,#22c55e);
border-radius:14px;display:inline-flex;align-items:center;justify-content:center;
font-size:1.6rem;margin-bottom:0.5rem;">&#129504;</div>
<div style="font-family:'Playfair Display',serif;font-size:1.1rem;color:#166534;font-weight:700;">
FlashMind AI</div>
<div style="font-size:0.68rem;color:#9ca3af;letter-spacing:0.12em;text-transform:uppercase;
font-weight:700;margin:2px 0 0.8rem;">Study Smarter, Not Harder</div>
<h1 style="font-family:'Playfair Display',serif;font-size:1.45rem;font-weight:800;
color:#14532d;margin:0 0 0.15rem;">Create Account</h1>
<p style="color:#9ca3af;font-size:0.84rem;margin:0;">
"Transform your notes into interactive learning"</p>
</div>""", unsafe_allow_html=True)

    new_user = st.text_input("Username", placeholder="Enter username", key="su_user")
    new_pass = st.text_input("Password", type="password",
        placeholder="At least 6 characters", key="su_pass")
    confirm = st.text_input("Confirm Password", type="password",
        placeholder="Repeat your password", key="su_conf")
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    if st.button("Register", key="reg_btn"):
        if not new_user or not new_pass or not confirm:
            st.warning("Please fill in all fields.")
        elif len(new_pass) < 6:
            st.error("Password must be at least 6 characters.")
        elif new_pass != confirm:
            st.error("Passwords do not match.")
        else:
            result = create_user(new_user, new_pass)
            if result["success"]:
                st.success("Account created! Please log in.")
                st.session_state.auth_mode = "login"
                st.rerun()
            else:
                st.error(result["message"])

    st.markdown("""<div style="background:#f0fdf4;border:1px solid #bbf7d0;
border-radius:12px;padding:0.8rem 1rem;margin:0.8rem 0 0.6rem;">
<div style="font-weight:800;font-size:0.86rem;color:#166634;font-family:'Nunito',sans-serif;">
&#128273; Returning User?</div>
<div style="font-size:0.79rem;color:#6b7280;margin-top:2px;font-family:'Nunito',sans-serif;">
Login with your Username &amp; Password</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
    if st.button("Login →", key="back_login"):
        st.session_state.auth_mode = "login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def show_auth_page():
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"
    if st.session_state.auth_mode == "signup":
        show_signup_page()
    else:
        show_login_page()

show_auth_page()