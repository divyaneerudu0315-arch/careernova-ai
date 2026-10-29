
import streamlit as st
import pymupdf

from modules.chatbot import get_career_response
from modules.learning_roadmap import generate_learning_roadmap

from modules.recommender import (
    load_careers,
    split_items,
    calculate_recommendations,
    calculate_career_readiness,
)

from modules.database import (
    initialize_database,
    save_profile,
)

from modules.resume_analyzer import (
    extract_skills,
    analyze_skill_gap,
)



# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="CareerNova AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_database()

# --------------------------------------------------
# 2. Premium Dark UI Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    :root {
        --cc-bg: #080D1A;
        --cc-panel: #111A2E;
        --cc-border: #2B3856;
        --cc-purple: #8B5CF6;
        --cc-text: #F1F5F9;
        --cc-muted: #A7B4CC;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 15% 0%, rgba(91,58,165,.20), transparent 35%),
            radial-gradient(ellipse at 90% 8%, rgba(56,189,248,.10), transparent 30%),
            var(--cc-bg);
        color: var(--cc-text);
    }
    .block-container { max-width:1360px; padding-top:1.15rem; padding-bottom:2rem; }
    [data-testid="stHeader"] { background:rgba(8,13,26,.75); }
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
        background:#090F1E; border-right:1px solid var(--cc-border);
    }
    [data-testid="stSidebar"] * { color:var(--cc-text); }
    h1,h2,h3,h4 { color:#F8FAFC !important; letter-spacing:-.025em; }
    p,label,[data-testid="stCaptionContainer"] { color:var(--cc-muted); }
    .main-title {
        font-size:clamp(2.2rem,5vw,3.5rem); line-height:1.12; font-weight:850;
        text-align:center; letter-spacing:-.045em;
        background:linear-gradient(95deg,#C4B5FD 8%,#A78BFA 45%,#67E8F9 95%);
        -webkit-background-clip:text; background-clip:text;
        -webkit-text-fill-color:transparent; margin:.2rem 0 .65rem 0;
    }
    .subtitle {
        max-width:760px; margin:0 auto 1.5rem auto; text-align:center;
        font-size:1.05rem; line-height:1.8; color:#A7B4CC;
    }
    .hero-panel {
        padding:1.35rem 1.5rem; border:1px solid #354365; border-radius:20px;
        background:linear-gradient(120deg,rgba(139,92,246,.13),rgba(56,189,248,.06));
        margin:.5rem 0 1.25rem 0;
    }
    .hero-kicker {
        color:#C4B5FD; font-size:.78rem; font-weight:800;
        letter-spacing:.13em; text-transform:uppercase; margin-bottom:.4rem;
    }
    .hero-copy { color:#D7E1F2; font-size:1rem; line-height:1.7; margin:0; }
    .career-card {
        padding:18px; border-radius:16px; border:1px solid var(--cc-border);
        background:var(--cc-panel); margin-bottom:12px;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color:var(--cc-border); border-radius:18px;
        background:rgba(17,26,46,.78);
    }
    [data-testid="stMetric"] {
        background:linear-gradient(145deg,#151F35,#10182A);
        border:1px solid #2D3A59; border-radius:14px; padding:10px 13px;
    }
    [data-testid="stMetricLabel"] { color:#A5B4FC !important; }
    [data-testid="stMetricValue"] { color:#F8FAFC !important; font-weight:800; }
    .stTextInput input,.stTextArea textarea {
        background:#111B30 !important; color:#F8FAFC !important;
        border:1px solid #354363 !important; border-radius:11px !important;
    }
    [data-baseweb="select"] > div {
        background:#111B30 !important; border-color:#354363 !important;
        color:#F8FAFC !important; border-radius:11px !important;
    }
    [data-testid="stFileUploader"] {
        background:rgba(17,26,46,.8) !important;
        border:1px dashed #8B5CF6 !important;
        border-radius:16px; padding:14px;
        color:#F1F5F9 !important;
    }
    /* Keep the PDF uploader drop zone dark instead of Streamlit's white default. */
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploaderDropzone"] > div {
        background:#111B30 !important;
        color:#F1F5F9 !important;
        border-color:#354363 !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background:#263451 !important;
        color:#F8FAFC !important;
        border:1px solid #5966A2 !important;
    }
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] label {
        color:#D7E1F2 !important;
    }
    .stButton > button,.stFormSubmitButton > button {
        color:white !important; background:linear-gradient(100deg,#7C3AED,#6366F1) !important;
        border:1px solid rgba(196,181,253,.25) !important; border-radius:11px !important;
        min-height:2.7rem; font-weight:750 !important;
        transition:transform .15s ease,filter .15s ease;
    }
    .stButton > button:hover,.stFormSubmitButton > button:hover {
        filter:brightness(1.12); transform:translateY(-1px); border-color:#A78BFA !important;
    }
    [data-testid="stProgressBar"] > div { background:#27334D; border-radius:999px; }
    [data-testid="stProgressBar"] > div > div {
        background:linear-gradient(90deg,#8B5CF6,#38BDF8); border-radius:999px;
    }
    [data-testid="stChatMessage"] {
        background:rgba(17,26,46,.88); border:1px solid #2B3856;
        border-radius:15px; padding:12px 14px; margin-bottom:10px;
    }
    /* Style the entire fixed chat-input area, not just the text field. */
    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"] {
        background:rgba(8,13,26,.97) !important;
        background-color:rgba(8,13,26,.97) !important;
    }
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="textarea"] > div {
        background:#111B30 !important;
        background-color:#111B30 !important;
        border-color:#5966A2 !important;
        border-radius:12px !important;
        box-shadow:none !important;
    }
    [data-testid="stChatInput"] textarea {
        background:transparent !important;
        background-color:transparent !important;
        color:#F8FAFC !important;
        -webkit-text-fill-color:#F8FAFC !important;
        caret-color:#C4B5FD !important;
        border:0 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color:#A7B4CC !important;
        -webkit-text-fill-color:#A7B4CC !important;
        opacity:1 !important;
    }
    [data-testid="stChatInput"] button {
        background:#263451 !important;
        color:#F8FAFC !important;
        border-color:#354363 !important;
    }
    [data-testid="stExpander"] {
        background:rgba(17,26,46,.8); border:1px solid var(--cc-border); border-radius:13px;
    }
    [data-testid="stAlert"] { border-radius:13px; }
    hr { border-color:#293550 !important; }
    .sidebar-brand { font-size:1.2rem; font-weight:850; letter-spacing:-.03em; color:#C4B5FD; padding:.4rem 0 .1rem; }
    .sidebar-caption { color:#8291AE; font-size:.82rem; line-height:1.5; margin-bottom:1rem; }
    [data-testid="stVerticalBlock"] { gap: .8rem; }
    .footer { text-align:center; color:#71809D; padding:24px 0 8px; font-size:.82rem; }
    @media(max-width:768px) {
        .block-container { padding:1rem 1rem 2rem; }
        .subtitle { font-size:.95rem; }
        .hero-panel { padding:1rem; }
    }
    
/* Improve readability of tables and roadmap content */
.stApp [data-testid="stMarkdownContainer"] table {
    color: #E5E7EB !important;
    background-color: #111827 !important;
    border-collapse: collapse !important;
}

.stApp [data-testid="stMarkdownContainer"] th {
    background-color: #263449 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

.stApp [data-testid="stMarkdownContainer"] td {
    background-color: #111827 !important;
    color: #E5E7EB !important;
    border-color: #374151 !important;
}

.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li {
    color: #D1D5DB;
}

.stApp [data-testid="stMarkdownContainer"] strong {
    color: #FFFFFF !important;
}

    </style>
    """,
    unsafe_allow_html=True,
)
# --------------------------------------------------
# CareerNova AI — Welcome Screen
# --------------------------------------------------

if (
    not st.session_state.get("welcome_started", False)
    and not st.session_state.get("student_name")
):
    st.markdown(
        """
        <div class="hero-panel" style="text-align:center;padding:3rem 2rem;">
            <div class="hero-kicker">YOUR FUTURE STARTS HERE</div>
            <h1 class="main-title">
                Welcome to CareerNova AI
            </h1>
            <p class="hero-copy" style="max-width:750px;margin:1rem auto;">
                Discover careers that fit your interests, identify skill gaps,
                build personalized learning roadmaps, and prepare for your
                next career opportunity with AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h2 style='text-align:center;'>Explore Your Career Journey</h2>",
        unsafe_allow_html=True,
    )

    feature_cols = st.columns(3)

    with feature_cols[0]:
        with st.container(border=True):
            st.markdown("### 🎯 Career Intelligence")
            st.write(
                "Discover career paths matched to your skills, "
                "education, and interests."
            )

    with feature_cols[1]:
        with st.container(border=True):
            st.markdown("### 📚 Adaptive Skill Growth")
            st.write(
                "Identify missing skills and create a personalized "
                "learning roadmap."
            )

    with feature_cols[2]:
        with st.container(border=True):
            st.markdown("### 🚀 Job Readiness")
            st.write(
                "Evaluate your career readiness and prepare "
                "for interviews."
            )

    st.write("")

    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        if st.button(
            "✨ Get Started",
            key="welcome_get_started",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["welcome_started"] = True
            st.session_state["active_page"] = "profile"
            st.rerun()

    st.markdown(
        "<p style='text-align:center;color:#A7B4CC;'>"
        "Career guidance powered by AI. Recommendations are guidance, "
        "not guarantees of employment."
        "</p>",
        unsafe_allow_html=True,
    )

    st.stop()



# --------------------------------------------------
# CareerNova AI — Sidebar Navigation
# --------------------------------------------------

if (
    st.session_state.get("welcome_started", False)
    or st.session_state.get("student_name")
):

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-brand">✦ CareerNova AI</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-caption">'
            'Your personal AI-powered career guide'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown("#### QUICK NAVIGATION")

        navigation_items = [
            ("▦ Dashboard", "career-dashboard"),
            ("👤 My Profile", "student-profile"),
            ("🧠 Career Intelligence", "career-intelligence"),
            ("🎯 Career Matches", "career-recommendations"),
            ("🧩 Skill Gap Analysis", "skill-gap-analysis"),
            ("📈 Adaptive Skill Growth", "adaptive-skill-growth"),
            ("🧪 Job Readiness & Simulation", "job-readiness-simulation"),
            ("📄 Resume Analysis", "resume-analyzer"),
            ("🗺️ Learning Roadmap", "learning-roadmap"),
            ("🤖 Career Coach", "career-chatbot"),
        ]

        for label, section_id in navigation_items:
            st.markdown(
                f'<a href="#{section_id}" '
                'style="display:block; padding:9px 10px; '
                'margin:3px 0; border-radius:9px; '
                'background:rgba(139,92,246,0.08); '
                'color:#C4B5FD; text-decoration:none; '
                'font-size:0.92rem;">'
                f'{label}</a>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.caption(
            "Build skills. Explore possibilities. Move forward."
        )


# --------------------------------------------------
# 4. Load Career Dataset
# --------------------------------------------------

try:
    careers_df = load_careers()

except Exception as error:
    st.error(f"Could not load the career dataset: {error}")
    st.stop()


all_skills = sorted({
    skill
    for value in careers_df["skills"]
    for skill in split_items(value)
})

all_interests = sorted({
    interest
    for value in careers_df["interests"]
    for interest in split_items(value)
})

# --------------------------------------------------
# CareerNova AI — Step 2: Profile Creation
# --------------------------------------------------

if st.session_state.get("active_page") == "profile":

    st.markdown(
        '<div class="hero-panel" style="text-align:center;">'
        '<div class="hero-kicker">YOUR CAREER JOURNEY</div>'
        '<h1 class="main-title">Let\'s Build Your Profile</h1>'
        '<p class="hero-copy">Tell us about yourself so we can '
        'recommend career paths that fit you.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    education_options = [
        "btech", "bsc", "bca", "mtech",
        "msc", "bba", "bcom",
    ]

    saved_education = st.session_state.get(
        "student_education", "btech"
    )
    education_index = (
        education_options.index(saved_education)
        if saved_education in education_options
        else 0
    )

    with st.form("careernova_profile_form"):

        name = st.text_input(
            "Your name",
            value=st.session_state.get("student_name", ""),
        )

        education = st.selectbox(
            "Education",
            education_options,
            index=education_index,
            format_func=lambda value: value.upper(),
        )

        skills = st.multiselect(
            "Skills you currently have",
            options=all_skills,
            default=[
                item for item in
                st.session_state.get("student_skills", [])
                if item in all_skills
            ],
            placeholder="Choose your skills",
        )

        interests = st.multiselect(
            "Areas that interest you",
            options=all_interests,
            default=[
                item for item in
                st.session_state.get("student_interests", [])
                if item in all_interests
            ],
            placeholder="Choose your interests",
        )

        submitted_profile = st.form_submit_button(
            "🚀 Generate My Career Dashboard",
            use_container_width=True,
        )

    if submitted_profile:

        if not name.strip():
            st.warning("Please enter your name.")

        elif not skills and not interests:
            st.warning(
                "Please select at least one skill or interest."
            )

        else:
            try:
                results = calculate_recommendations(
                    skills=skills,
                    interests=interests,
                    education=education,
                    top_n=5,
                )

                if not results:
                    st.warning(
                        "No recommendations were generated. "
                        "Please review your profile and try again."
                    )

                else:
                    profile_id = save_profile(
                        name=name.strip(),
                        education=education,
                        skills=skills,
                        interests=interests,
                        results=results,
                    )

                    st.session_state["student_name"] = name.strip()
                    st.session_state["student_education"] = education
                    st.session_state["student_skills"] = list(skills)
                    st.session_state["student_interests"] = list(interests)
                    st.session_state["career_results"] = results
                    st.session_state["profile_id"] = profile_id

                    for key in (
                        "resume_analysis",
                        "resume_analysis_career",
                        "resume_file_name",
                        "resume_detected_count",
                    ):
                        st.session_state.pop(key, None)

                    st.session_state["welcome_started"] = True
                    st.session_state["active_page"] = "dashboard"

                    st.rerun()

            except Exception as error:
                st.error(f"Could not save your profile: {error}")

    # Do not display the dashboard underneath the profile screen.
    st.stop()



# --------------------------------------------------
# 5. Interactive Career Analytics Dashboard
# --------------------------------------------------

st.markdown('<div id="career-dashboard"></div>', unsafe_allow_html=True)

profile_name = st.session_state.get("student_name", "")
profile_skills = st.session_state.get("student_skills", [])
profile_interests = st.session_state.get("student_interests", [])
profile_education = st.session_state.get("student_education", "Not added yet")
career_results = st.session_state.get("career_results", [])

# Header inspired by the provided premium dark dashboard reference.
st.markdown(
    f'<div style="display:flex;justify-content:space-between;align-items:center;gap:16px;'
    f'flex-wrap:wrap;padding:4px 0 14px 0">'
    f'<div><div style="font-size:1.8rem;font-weight:800;color:#F8FAFC">'
    f"Good to see you{', ' + profile_name if profile_name else ''}! 👋"
    f'</div><div style="color:#A7B4CC;margin-top:5px">'
    f"{'Your career journey is ready to continue.' if profile_name else 'Build your profile to unlock personalized career insights.'}"
    f'</div></div>'
    f'<div style="padding:10px 15px;border:1px solid #354365;border-radius:14px;'
    f'background:rgba(17,26,46,.85);color:#C4B5FD;font-weight:700">✦ CAREERNOVA AI</div>'
    f'</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div style="font-size:1.8rem;font-weight:850;letter-spacing:-.035em;color:#F8FAFC;margin:0 0 2px 0">'
    'Your Career <span style="background:linear-gradient(90deg,#A78BFA,#38BDF8);'
    '-webkit-background-clip:text;-webkit-text-fill-color:transparent">Dashboard</span></div>',
    unsafe_allow_html=True,
)
st.caption("Your skills, career matches, and next steps — all in one place.")

# Real metrics only; show a clear setup state before a profile exists.
if career_results:
    top_result = career_results[0]
    try:
        top_readiness = calculate_career_readiness(profile_skills, top_result["career"])
        readiness_value = top_readiness["readiness_score"] if top_readiness else 0
    except Exception:
        readiness_value = 0
    match_value = top_result.get("match_score", 0)
    top_career_name = top_result.get("career", "Not available")
else:
    readiness_value = 0
    match_value = 0
    top_career_name = "Not generated yet"


# --------------------------------------------------
# Premium Dashboard Metric Cards
# --------------------------------------------------

st.markdown("""
<style>
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #111A2E, #151F38);
    border: 1px solid #293653;
    padding: 18px 20px;
    border-radius: 16px;
    min-height: 115px;
}
div[data-testid="stMetricLabel"] {
    color: #A7B4CC;
    font-size: 0.9rem;
}
div[data-testid="stMetricValue"] {
    color: #F8FAFC;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4, gap="medium")

with m1:
    st.metric(
        label="🧠 Profile Skills",
        value=len(profile_skills),
        help="Skills saved in your student profile."
    )

with m2:
    st.metric(
        label="🎯 Career Matches",
        value=len(career_results),
        help="Career recommendations generated from your profile."
    )

with m3:
    st.metric(
        label="✨ Best Career Match",
        value=f"{match_value:.0f}%" if career_results else "—",
        help="Match score for your highest-ranked career."
    )

with m4:
    st.metric(
        label="📈 Career Readiness",
        value=f"{readiness_value:.0f}%" if career_results else "—",
        help="Readiness score based on the top recommended career."
    )


left, right = st.columns([1, 1], gap="medium")
with left:
    with st.container(border=True):
        st.markdown("#### Your profile")
        if profile_name:
            st.write(f"**Student:** {profile_name}")
            st.write(f"**Education:** {str(profile_education).upper()}")
            st.write(f"**Interests:** {', '.join(i.title() for i in profile_interests) if profile_interests else 'Not added yet'}")
            st.write(f"**Current skills:** {', '.join(skill.title() for skill in profile_skills) if profile_skills else 'No skills added yet'}")
        else:
            st.write("Your personalized snapshot will appear here after you submit the Student Profile form below.")
            st.info("Start by adding your education, skills, and interests.")
with right:
    with st.container(border=True):
        st.markdown("#### Top career match")
        if career_results:
            st.markdown(
                f'<div style="font-size:1.35rem;font-weight:800;color:#C4B5FD">{top_career_name}</div>',
                unsafe_allow_html=True,
            )
            st.progress(min(1.0, max(0.0, float(match_value) / 100)))
            st.caption(f"Career match: {match_value}% · Based on your submitted profile")
            st.write("Explore the complete ranked recommendations below to compare career options.")
        else:
            st.write("Your top career match will be shown here after recommendations are generated.")
            if st.button("Build my student profile", key="dashboard_profile_button", use_container_width=True):
                st.session_state["dashboard_profile_prompt"] = True
                st.rerun()


# --------------------------------------------------
# Premium Top Career Match Cards
# --------------------------------------------------

if career_results:
    st.markdown("### ✨ Your Best Career Matches")
    st.caption(
        "Explore your highest-ranked careers and compare how well "
        "they align with your profile."
    )

    card_cols = st.columns(min(3, len(career_results)), gap="medium")

    for idx, result in enumerate(career_results[:3]):
        with card_cols[idx]:
            with st.container(border=True):
                career_name = result.get("career", "Career")
                domain_name = result.get("domain", "Career domain")
                score = float(result.get("match_score", 0))

                st.markdown(
                    f'<div style="color:#A78BFA;font-size:.8rem;'
                    f'font-weight:700;letter-spacing:.08em;">'
                    f'CAREER MATCH #{idx + 1}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(f"#### {career_name}")
                st.caption(domain_name)

                st.markdown(
                    f'<div style="font-size:2rem;font-weight:850;'
                    f'color:#C4B5FD;margin:8px 0 2px 0;">'
                    f'{score:.0f}%</div>',
                    unsafe_allow_html=True,
                )

                st.progress(min(1.0, max(0.0, score / 100)))

                if idx == 0:
                    st.caption("⭐ Your highest-ranked match")
                else:
                    st.caption("Recommended career option")

else:
    st.markdown(
        '<div class="hero-panel">'
        '<div class="hero-kicker">YOUR NEXT STEP</div>'
        '<p class="hero-copy">'
        'Complete your student profile to discover career matches, '
        'readiness insights, and personalized learning opportunities.'
        '</p></div>',
        unsafe_allow_html=True,
    )

st.markdown("---")



# --------------------------------------------------
# 6. Profile Management
# --------------------------------------------------

st.markdown('<div id="student-profile"></div>', unsafe_allow_html=True)
st.header("👤 My Profile")

if st.session_state.get("student_name"):

    st.write(f"**Name:** {st.session_state['student_name']}")
    st.write(
        f"**Education:** "
        f"{st.session_state.get('student_education', '').upper()}"
    )
    st.write(
        "**Skills:** "
        + (
            ", ".join(st.session_state.get("student_skills", []))
            or "None added"
        )
    )
    st.write(
        "**Interests:** "
        + (
            ", ".join(st.session_state.get("student_interests", []))
            or "None added"
        )
    )

    if st.button("✏️ Update My Profile", key="update_profile"):
        st.session_state["active_page"] = "profile"
        st.rerun()

else:
    st.info("Create your profile to get personalized career recommendations.")
    if st.button("Create My Profile", key="create_profile_from_dashboard"):
        st.session_state["welcome_started"] = True
        st.session_state["active_page"] = "profile"
        st.rerun()

# --------------------------------------------------
# 8. Display Career Recommendations and Readiness
# --------------------------------------------------

if "career_results" in st.session_state:

    results = st.session_state["career_results"]
    student_skills = st.session_state.get("student_skills", [])

    st.divider()

    st.markdown('<div id="career-recommendations"></div>', unsafe_allow_html=True)
    st.header(
        f"🚀 Career Recommendations for "
        f"{st.session_state['student_name']}"
    )

    st.caption(
        "Career Match Score considers skills, interests, and education. "
        "Career Readiness Score measures required skill coverage. "
        "Neither score predicts placement probability."
    )

    for rank, result in enumerate(results, start=1):

        with st.container(border=True):

            st.subheader(f"{rank}. {result['career']}")
            st.caption(f"Domain: {result['domain']}")

            st.metric(
                "Career Match Score",
                f"{result['match_score']}%",
            )

            st.progress(
                min(
                    1.0,
                    max(0.0, result["match_score"] / 100),
                )
            )

            readiness = calculate_career_readiness(
                student_skills,
                result["career"],
            )

            if readiness is not None:

                st.metric(
                    "🎯 Career Readiness Score",
                    f"{readiness['readiness_score']} / 100",
                )

                st.progress(
                    min(
                        1.0,
                        max(
                            0.0,
                            readiness["readiness_score"] / 100,
                        ),
                    )
                )

                st.caption(
                    f"Required skills matched: "
                    f"{readiness['total_matched_skills']} of "
                    f"{readiness['total_required_skills']}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Skills you already have**")

                    if readiness["matched_skills"]:
                        st.write(
                            ", ".join(
                                skill.title()
                                for skill in readiness["matched_skills"]
                            )
                        )
                    else:
                        st.write("No direct skill matches yet.")

                with col2:
                    st.write("**Skills to learn next**")

                    if readiness["missing_skills"]:
                        st.write(
                            ", ".join(
                                skill.title()
                                for skill in readiness["missing_skills"]
                            )
                        )
                    else:
                        st.write(
                            "All listed skills in this career profile "
                            "are covered."
                        )

            else:
                st.warning(
                    "Could not calculate readiness for this career."
                )

            st.write(
                f"**Interest coverage:** {result['interest_score']}%"
            )

            st.write(
                f"**Education match:** {result['education_score']}%"
            )

    st.success(
        "Use these recommendations to explore suitable career paths "
        "and plan your next learning steps."
    )

# --------------------------------------------------
# CareerNova AI — Career Intelligence Engine
# --------------------------------------------------

st.divider()
st.markdown('<div id="career-intelligence"></div>', 
            unsafe_allow_html=True
)

st.header("🧠 Career Intelligence")
st.write(
    "Understand why careers match your profile, compare career options, "
    "and discover practical steps to improve your career fit."
)

if not st.session_state.get("student_name"):
    st.info("Create your student profile to unlock personalized career intelligence.")

elif not st.session_state.get("career_results"):
    st.info("Generate your career recommendations first.")

else:
    intelligence_results = st.session_state["career_results"]

    # Compare the recommended careers without changing the original results.
    career_names = [
        result["career"]
        for result in intelligence_results
        if result.get("career")
    ]

    default_careers = career_names[:min(3, len(career_names))]

    selected_intelligence_careers = st.multiselect(
        "Choose careers to compare",
        options=career_names,
        default=default_careers,
        key="career_intelligence_compare",
        help="Select up to three careers for a focused comparison.",
    )

    selected_intelligence_careers = selected_intelligence_careers[:3]

    if not selected_intelligence_careers:
        st.info("Select at least one career to see your insights.")

    else:
        comparison_rows = []

        for result in intelligence_results:
            if result["career"] not in selected_intelligence_careers:
                continue

            career_name = result["career"]

            match_score = float(result.get("match_score", 0))
            interest_score = float(result.get("interest_score", 0))
            education_score = float(result.get("education_score", 0))

            readiness = calculate_career_readiness(
                st.session_state.get("student_skills", []),
                career_name,
            )

            readiness_score = (
                float(readiness.get("readiness_score", 0))
                if readiness else 0
            )

            comparison_rows.append({
                "Career": career_name,
                "Domain": result.get("domain", "Not specified"),
                "Career Match (%)": round(match_score, 1),
                "Interest Match (%)": round(interest_score, 1),
                "Education Match (%)": round(education_score, 1),
                "Skill Readiness (%)": round(readiness_score, 1),
            })

        st.subheader("📊 Career Comparison")

        if comparison_rows:
            st.dataframe(
                comparison_rows,
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Career match reflects the existing recommendation model. "
                "Skill readiness reflects required-skill coverage. "
                "These scores are not job or placement probabilities."
            )

        st.subheader("🔍 Personalized Career Insights")

        insight_columns = st.columns(
            min(2, len(selected_intelligence_careers))
        )

        for index, career_name in enumerate(
            selected_intelligence_careers
        ):
            result = next(
                item for item in intelligence_results
                if item["career"] == career_name
            )

            readiness = calculate_career_readiness(
                st.session_state.get("student_skills", []),
                career_name,
            )

            match_score = float(result.get("match_score", 0))
            interest_score = float(result.get("interest_score", 0))
            education_score = float(result.get("education_score", 0))

            with insight_columns[index % len(insight_columns)]:
                with st.container(border=True):
                    st.markdown(f"### 🎯 {career_name}")
                    st.metric("Career Match", f"{match_score:.1f}%")

                    # Explain the existing model's component scores.
                    st.markdown("**Why this career appears in your matches**")

                    if interest_score >= 60:
                        st.write(
                            f"✅ Strong interest alignment ({interest_score:.0f}%)."
                        )
                    elif interest_score > 0:
                        st.write(
                            f"🔎 Interest alignment: {interest_score:.0f}%. "
                            "Explore the role to confirm your interest."
                        )
                    else:
                        st.write(
                            "💡 Your selected interests have limited "
                            "overlap with this career's dataset."
                        )

                    if education_score >= 60:
                        st.write(
                            f"✅ Education alignment ({education_score:.0f}%)."
                        )
                    else:
                        st.write(
                            f"📚 Education alignment: {education_score:.0f}%. "
                            "Check the qualifications expected for this role."
                        )

                    if readiness:
                        missing_skills = readiness.get("missing_skills", [])
                        matched_skills = readiness.get("matched_skills", [])

                        st.markdown("**Your next improvement steps**")

                        if matched_skills:
                            st.write(
                                "Existing strengths: "
                                + ", ".join(
                                    str(skill).title()
                                    for skill in matched_skills[:5]
                                )
                            )

                        if missing_skills:
                            st.write(
                                "Skills to prioritize: "
                                + ", ".join(
                                    str(skill).title()
                                    for skill in missing_skills[:5]
                                )
                            )
                            st.caption(
                                "Use the Learning Roadmap section to plan "
                                "how to develop these skills."
                            )
                        else:
                            st.success(
                                "Your profile covers all skills listed "
                                "for this career in the current dataset."
                            )

                        st.progress(
                            max(
                                0.0,
                                min(
                                    1.0,
                                    readiness["readiness_score"] / 100,
                                ),
                            )
                        )
                        st.caption(
                            f"Required-skill coverage: "
                            f"{readiness['readiness_score']}%"
                        )

                    st.caption(
                        "These insights use your profile and the existing "
                        "career dataset. They are guidance, not a guarantee "
                        "of career success."
                    )



# --------------------------------------------------
# 9. AI Resume Analyzer
# --------------------------------------------------

# --------------------------------------------------
# CareerNova AI — Dedicated Skill Gap Analysis
# --------------------------------------------------

st.divider()

st.markdown(
    '<div id="skill-gap-analysis"></div>',
    unsafe_allow_html=True,
)

st.header("🧩 Skill Gap Analysis")

st.write(
    "Compare your current skills with the skills required for "
    "your target career. Discover what you already know and "
    "what you should learn next."
)

student_skills_for_gap = st.session_state.get(
    "student_skills", []
)

available_gap_careers = (
    careers_df["career"]
    .dropna()
    .astype(str)
    .drop_duplicates()
    .tolist()
)

if not st.session_state.get("student_name"):

    st.info(
        "Create your student profile first to analyze your "
        "personal skill gaps."
    )

else:

    recommended_careers = [
        result.get("career")
        for result in st.session_state.get("career_results", [])
    ]

    preferred_career = next(
        (
            career
            for career in recommended_careers
            if career in available_gap_careers
        ),
        available_gap_careers[0] if available_gap_careers else None,
    )

    if available_gap_careers:

        default_index = available_gap_careers.index(
            preferred_career
        )

        selected_gap_career = st.selectbox(
            "Choose your target career",
            options=available_gap_careers,
            index=default_index,
            key="dedicated_skill_gap_career",
        )

        if st.button(
            "🔍 Analyze My Skill Gaps",
            key="dedicated_skill_gap_button",
            use_container_width=True,
        ):

            selected_row = careers_df[
                careers_df["career"] == selected_gap_career
            ].iloc[0]

            required_gap_skills = split_items(
                selected_row["skills"]
            )

            gap_results = analyze_skill_gap(
                student_skills_for_gap,
                required_gap_skills,
            )

            st.session_state["dedicated_gap_results"] = gap_results
            st.session_state["dedicated_gap_career"] = (
                selected_gap_career
            )

        gap_results = st.session_state.get(
            "dedicated_gap_results"
        )

        saved_gap_career = st.session_state.get(
            "dedicated_gap_career"
        )

        if gap_results and saved_gap_career == selected_gap_career:

            st.subheader(
                f"Your Skill Gap Report: {selected_gap_career}"
            )

            matched = gap_results.get("matched_skills", [])
            missing = gap_results.get("missing_skills", [])
            percentage = gap_results.get("match_percentage", 0)

            col1, col2, col3 = st.columns(3)

            col1.metric("Skills Matched", len(matched))
            col2.metric("Skills to Learn", len(missing))
            col3.metric("Skill Match", f"{percentage}%")

            st.progress(
                max(0.0, min(1.0, float(percentage) / 100))
            )

            with st.container(border=True):

                st.markdown("#### ✅ Skills You Already Have")

                if matched:
                    for skill in matched:
                        st.write(f"✅ {str(skill).title()}")
                else:
                    st.info(
                        "No required skills matched yet. "
                        "This is your starting point."
                    )

            with st.container(border=True):

                st.markdown("#### 📚 Skills You Need to Learn")

                if missing:
                    for skill in missing:
                        st.write(f"🎯 {str(skill).title()}")

                    st.caption(
                        "Prioritize these skills when building "
                        "your learning roadmap."
                    )

                else:
                    st.success(
                        "All skills listed in this career's "
                        "dataset are covered by your profile."
                    )

            st.caption(
                "This score measures skill overlap with the "
                "career dataset. It is not a job placement "
                "probability or a guarantee of employability."
            )

    else:
        st.warning("No target careers are available in the dataset.")

    
# --------------------------------------------------
# CareerNova AI — Personalized Learning Roadmap
# --------------------------------------------------

st.divider()

st.markdown(
    '<div id="learning-roadmap"></div>',
    unsafe_allow_html=True,
)

st.header("🗺️ Personalized Learning Roadmap")

st.write(
    "Turn your skill gaps into an actionable learning plan "
    "based on your selected target career."
)

roadmap_careers = (
    careers_df["career"]
    .dropna()
    .astype(str)
    .drop_duplicates()
    .tolist()
)

if not st.session_state.get("student_name"):

    st.info(
        "Create your student profile first to generate "
        "a personalized learning roadmap."
    )

elif not roadmap_careers:

    st.warning("No careers are available in the dataset.")

else:

    previous_gap_career = st.session_state.get(
        "dedicated_gap_career"
    )

    default_roadmap_career = (
        previous_gap_career
        if previous_gap_career in roadmap_careers
        else roadmap_careers[0]
    )

    roadmap_career = st.selectbox(
        "Choose a career for your roadmap",
        options=roadmap_careers,
        index=roadmap_careers.index(default_roadmap_career),
        key="independent_roadmap_career",
    )

    if st.button(
        "🚀 Generate My Learning Roadmap",
        key="independent_roadmap_button",
        use_container_width=True,
    ):

        roadmap_row = careers_df[
            careers_df["career"] == roadmap_career
        ].iloc[0]

        roadmap_required_skills = split_items(
            roadmap_row["skills"]
        )

        roadmap_current_skills = st.session_state.get(
            "student_skills", []
        )

        roadmap_analysis = analyze_skill_gap(
            roadmap_current_skills,
            roadmap_required_skills,
        )

        roadmap_missing_skills = roadmap_analysis.get(
            "missing_skills", []
        )

        st.session_state["independent_roadmap_data"] = {
            "career": roadmap_career,
            "missing_skills": roadmap_missing_skills,
        }

    roadmap_data = st.session_state.get(
        "independent_roadmap_data"
    )

    if roadmap_data and roadmap_data["career"] == roadmap_career:

        missing_for_roadmap = roadmap_data["missing_skills"]

        if missing_for_roadmap:

            learning_plan = generate_learning_roadmap(
                missing_for_roadmap
            )

            st.subheader(
                f"Your Roadmap for {roadmap_career}"
            )

            st.caption(
                f"Focus areas: {len(missing_for_roadmap)} "
                "skills identified from your profile."
            )

            st.markdown("#### 🎯 Skills to Focus On")

            for skill in missing_for_roadmap:
                st.write(f"📌 {str(skill).title()}")

            st.markdown("#### 📅 Your Learning Plan")

            if isinstance(learning_plan, dict):

                for topic, details in learning_plan.items():

                    with st.expander(str(topic), expanded=True):

                        if isinstance(details, dict):

                            for label, value in details.items():
                                st.markdown(
                                    f"**{str(label).replace('_', ' ').title()}:** "
                                    f"{value}"
                                )

                        elif isinstance(details, list):

                            for item in details:
                                st.write(f"• {item}")

                        else:
                            st.write(details)

            elif isinstance(learning_plan, list):

                for index, item in enumerate(learning_plan, start=1):

                    with st.container(border=True):

                        st.markdown(f"**Step {index}**")

                        if isinstance(item, dict):

                            for label, value in item.items():
                                st.markdown(
                                    f"**{str(label).replace('_', ' ').title()}:** "
                                    f"{value}"
                                )

                        else:
                            st.write(item)

            else:
                st.write(learning_plan)

        else:

            st.success(
                "Your profile already covers all the skills "
                "listed for this career in the dataset. "
                "Consider advanced topics and practical projects."
            )


# --------------------------------------------------
# CareerNova AI — Adaptive Skill Growth
# --------------------------------------------------

st.divider()

st.markdown(
    '<div id="adaptive-skill-growth"></div>',
    unsafe_allow_html=True,
)

st.header("📈 Adaptive Skill Growth")

st.write(
    "Track your learning journey, update the status of each "
    "career skill, and identify your next learning priority."
)

if not st.session_state.get("student_name"):

    st.info(
        "Create your student profile first to track your "
        "personalized skill growth."
    )

else:

    adaptive_careers = (
        careers_df["career"]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .tolist()
    )

    if not adaptive_careers:

        st.warning("No careers are available in the dataset.")

    else:

        previous_adaptive_career = st.session_state.get(
            "dedicated_gap_career"
        )

        if previous_adaptive_career not in adaptive_careers:
            previous_adaptive_career = st.session_state.get(
                "independent_roadmap_career"
            )

        if previous_adaptive_career not in adaptive_careers:
            previous_adaptive_career = adaptive_careers[0]

        selected_adaptive_career = st.selectbox(
            "Choose your target career",
            options=adaptive_careers,
            index=adaptive_careers.index(
                previous_adaptive_career
            ),
            key="adaptive_growth_career",
        )

        adaptive_row = careers_df[
            careers_df["career"] == selected_adaptive_career
        ].iloc[0]

        adaptive_required_skills = split_items(
            adaptive_row["skills"]
        )

        adaptive_progress = st.session_state.setdefault(
            "adaptive_skill_progress", {}
        )

        career_progress = adaptive_progress.setdefault(
            selected_adaptive_career, {}
        )

        # Recognize skills already listed in the student profile.
        initial_analysis = analyze_skill_gap(
            st.session_state.get("student_skills", []),
            adaptive_required_skills,
        )

        initially_matched = {
            str(skill).casefold()
            for skill in initial_analysis.get("matched_skills", [])
        }

        if adaptive_required_skills:

            st.markdown("### 🎯 Your Skill Development Tracker")

            st.caption(
                "Update each status as you learn. Skills already "
                "listed in your profile start as Completed unless "
                "you have previously tracked them."
            )

            for index, skill in enumerate(adaptive_required_skills):

                skill_name = str(skill)
                skill_key = (
                    f"adaptive_status_{selected_adaptive_career}_{index}"
                )

                if skill_name not in career_progress:
                    career_progress[skill_name] = (
                        "Completed"
                        if skill_name.casefold() in initially_matched
                        else "Not Started"
                    )

                if skill_key not in st.session_state:
                    st.session_state[skill_key] = career_progress[
                        skill_name
                    ]

                with st.container(border=True):

                    skill_col, status_col = st.columns(
                        [2, 1]
                    )

                    with skill_col:
                        st.markdown(
                            f"**{index + 1}. {skill_name.title()}**"
                        )

                    with status_col:
                        updated_status = st.selectbox(
                            "Learning status",
                            options=[
                                "Not Started",
                                "In Progress",
                                "Completed",
                            ],
                            key=skill_key,
                            label_visibility="collapsed",
                        )

                    career_progress[skill_name] = updated_status

            # Save progress for this career in the current session.
            adaptive_progress[
                selected_adaptive_career
            ] = career_progress

            total_skills = len(adaptive_required_skills)

            completed_count = sum(
                1
                for skill in adaptive_required_skills
                if career_progress.get(str(skill)) == "Completed"
            )

            in_progress_count = sum(
                1
                for skill in adaptive_required_skills
                if career_progress.get(str(skill)) == "In Progress"
            )

            progress_percentage = round(
                completed_count / total_skills * 100
            )

            st.markdown("### 📊 Your Learning Progress")

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Completed",
                f"{completed_count}/{total_skills}",
            )

            metric2.metric(
                "In Progress",
                in_progress_count,
            )

            metric3.metric(
                "Progress",
                f"{progress_percentage}%",
            )

            st.progress(progress_percentage / 100)

            in_progress_skill = next(
                (
                    str(skill)
                    for skill in adaptive_required_skills
                    if career_progress.get(str(skill)) == "In Progress"
                ),
                None,
            )

            next_skill = in_progress_skill or next(
                (
                    str(skill)
                    for skill in adaptive_required_skills
                    if career_progress.get(str(skill)) == "Not Started"
                ),
                None,
            )

            st.markdown("### 🚀 Your Next Priority")

            if next_skill:

                st.info(
                    f"Focus on **{next_skill.title()}** next. "
                    "Study the topic, practise with exercises, "
                    "and update its status when you make progress."
                )

            else:

                st.success(
                    "Excellent! All listed skills are marked "
                    "Completed. Consider advanced topics and "
                    "practical projects to strengthen your skills."
                )

            st.caption(
                "Progress is tracked separately for each career "
                "in the current Streamlit session. It is not yet "
                "saved permanently to the database."
            )

        else:

            st.info(
                "No required skills are listed for this career "
                "in the current dataset."
            )


st.divider()

st.markdown('<div id="resume-analyzer"></div>', unsafe_allow_html=True)
st.header("📄 AI Resume Analyzer")

st.write(
    "Upload your resume to discover your existing skills, "
    "compare them with a career, and identify skills to learn."
)

uploaded_resume = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
    key="resume_upload",
)


if uploaded_resume is not None:

    try:
        pdf_bytes = uploaded_resume.getvalue()

        with pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf",
        ) as pdf:

            resume_text = "\n".join(
                page.get_text()
                for page in pdf
            )

        if not resume_text.strip():

            st.warning(
                "No readable text was found. "
                "Scanned resumes require OCR support."
            )

        else:
            resume_skills = extract_skills(resume_text)
            st.session_state["resume_detected_skills"] = resume_skills
            st.session_state["resume_detected_skills"] = resume_skills

            st.subheader("Skills Found in Your Resume")

            if resume_skills:
                st.success(
                    f"Detected {len(resume_skills)} recognized skills."
                )
                st.write(", ".join(resume_skills))
            else:
                st.info(
                    "No recognized skills were found. "
                    "Check whether your resume lists technical skills."
                )

            career_names = careers_df["career"].tolist()

            selected_career = st.selectbox(
                "Choose a career to analyze",
                career_names,
                key="resume_career",
            )

            selected_row = careers_df[
                careers_df["career"] == selected_career
            ].iloc[0]

            required_skills = split_items(
                selected_row["skills"]
            )

            if st.button(
                "Analyze My Skill Gap",
                use_container_width=True,
                key="analyze_resume",
            ):

                analysis = analyze_skill_gap(
                    resume_skills,
                    required_skills,
                )

                st.session_state["resume_analysis"] = analysis
                st.session_state["resume_analysis_career"] = (
                    selected_career
                )
                st.session_state["resume_detected_count"] = (
                    len(resume_skills)
                )
                st.session_state["resume_file_name"] = (
                    uploaded_resume.name
                )

            analysis = st.session_state.get("resume_analysis")

            same_resume = (
                st.session_state.get("resume_file_name")
                == uploaded_resume.name
            )

            same_career = (
                st.session_state.get("resume_analysis_career")
                == selected_career
            )

            if analysis is not None and same_resume and same_career:

                st.divider()

                st.subheader(f"Results for {selected_career}")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Skill Match",
                        f"{analysis['match_percentage']}%",
                    )

                with col2:
                    st.metric(
                        "Skills Detected",
                        st.session_state["resume_detected_count"],
                    )

                st.progress(
                    max(
                        0.0,
                        min(
                            1.0,
                            analysis["match_percentage"] / 100,
                        ),
                    )
                )

                st.markdown("### ✅ Matching Skills")

                if analysis["matched_skills"]:
                    for skill in analysis["matched_skills"]:
                        st.write(f"✅ {skill.title()}")
                else:
                    st.info("No matching skills found.")

                st.markdown("### 📚 Missing Skills to Learn")

                if analysis["missing_skills"]:
                    for skill in analysis["missing_skills"]:
                        st.write(f"❌ {skill.title()}")
                else:
                    st.success(
                        "All required skills in this sample "
                        "career profile were found!"
                    )

                st.caption(
                    "The score measures overlap with skills listed "
                    "in the sample career dataset. It is not an ATS "
                    "score or a guarantee of employability."
                )


    except Exception as error:
        st.error(
            f"Could not analyze this resume: {error}"
        )


# --------------------------------------------------
# 10. Personalized CareerCompass AI Chatbot
# --------------------------------------------------

# --------------------------------------------------
# CareerNova AI — Job Readiness & Simulation
# --------------------------------------------------

st.markdown('<div id="job-readiness-simulation"></div>', unsafe_allow_html=True)

st.markdown("## 🧪 Job Readiness & Simulation")
st.markdown(
    "Evaluate your skill coverage, identify job requirements you need to learn, "
    "and practise interview questions with AI feedback."
)

# Get available career options
career_options = careers_df["career"].dropna().unique().tolist()

if career_options:
    target_career = st.selectbox(
        "🎯 Select your target career",
        career_options,
        key="job_simulation_career",
    )

    # Collect skills from the profile and uploaded resume
    profile_skills = st.session_state.get("student_skills", [])
    resume_skills = st.session_state.get("resume_detected_skills", [])

    if isinstance(profile_skills, str):
        profile_skills = split_items(profile_skills)

    if isinstance(resume_skills, str):
        resume_skills = split_items(resume_skills)

    candidate_skill_map = {}

    for skill in list(profile_skills) + list(resume_skills):
        skill = str(skill).strip()
        if skill:
            candidate_skill_map[skill.lower()] = skill

    candidate_skills = list(candidate_skill_map.values())

    st.markdown("### 1. Job Description Skill Match")

    job_description = st.text_area(
        "Paste a job description (optional)",
        placeholder=(
            "Paste the responsibilities and required skills from a job posting. "
            "Leave blank to assess skills against your selected career."
        ),
        height=150,
        key="job_simulation_description",
    )

    if st.button("🔍 Analyse Job Readiness", key="analyse_job_readiness"):
        if not candidate_skills:
            st.warning(
                "Please add skills to My Profile or upload a resume "
                "in Resume Analysis before running the assessment."
            )
        else:
            if job_description.strip():
                required_skills = extract_skills(job_description)

                if not required_skills:
                    st.warning(
                        "No recognised skills were detected in that job description. "
                        "Try including its technical skills, or leave the description "
                        "blank to assess against the selected career."
                    )
                    st.stop()
            else:
                career_rows = careers_df[
                    careers_df["career"] == target_career
                ]

                if career_rows.empty:
                    required_skills = []
                else:
                    required_skills = split_items(
                        career_rows.iloc[0]["skills"]
                    )

            if not required_skills:
                st.warning(
                    "No required skills were found for this assessment. "
                    "Please choose another career or provide a job description."
                )
            else:
                result = analyze_skill_gap(
                    candidate_skills,
                    required_skills,
                )

                st.session_state["job_readiness_match"] = result
                st.session_state["job_readiness_career"] = target_career
                st.session_state["job_readiness_required_skills"] = required_skills
                st.session_state["job_readiness_candidate_skills"] = candidate_skills
                st.session_state["job_readiness_description"] = job_description

    # Display the most recent skill-match result
    result = st.session_state.get("job_readiness_match")

    if (
        result
        and st.session_state.get("job_readiness_career") == target_career
    ):
        st.markdown("#### Your Skill Match Results")

        match_score = result.get("match_percentage", 0)
        matched_skills = result.get("matched_skills", [])
        missing_skills = result.get("missing_skills", [])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Skill Match", f"{match_score}%")

        with col2:
            st.metric("Matched Skills", len(matched_skills))

        with col3:
            st.metric("Skills to Develop", len(missing_skills))

        st.progress(max(0, min(100, int(match_score))) / 100)

        st.caption(
            "This percentage measures skill coverage against the selected "
            "requirements. It is not a prediction of hiring success."
        )

        with st.expander("✅ Skills You Already Have", expanded=True):
            if matched_skills:
                st.write(", ".join(matched_skills))
            else:
                st.write("No matching skills detected yet.")

        with st.expander("📚 Skills to Improve"):
            if missing_skills:
                st.write(", ".join(missing_skills))
                st.info(
                    "Use the Learning Roadmap and Adaptive Skill Growth "
                    "sections to plan your next learning steps."
                )
            else:
                st.success("All recognised skills in this assessment matched!")

    st.divider()
    st.markdown("### 2. AI Mock Interview")

    interview_mode = st.selectbox(
        "Choose an interview type",
        ["Technical", "HR", "Behavioural"],
        key="job_simulation_interview_mode",
    )

    career_lower = target_career.lower()

    if interview_mode == "HR":
        questions = [
            "Tell me about yourself and your career goals.",
            "What are your strengths, and how do they help you in a team?",
            "Describe a challenge you faced in a project and how you handled it.",
        ]
    elif interview_mode == "Behavioural":
        questions = [
            "Describe a time you solved a difficult problem. What was your approach?",
            "Tell me about a time you received feedback. How did you respond?",
            "Describe a situation where you worked with a team to achieve a goal.",
        ]
    elif any(word in career_lower for word in ["data", "machine learning", "analyst"]):
        questions = [
            "How would you handle missing values in a dataset?",
            "Explain a data or machine-learning project you have worked on.",
            "How would you evaluate a machine-learning model and check for overfitting?",
        ]
    elif any(word in career_lower for word in ["cyber", "security"]):
        questions = [
            "How would you investigate a suspicious login attempt?",
            "What is phishing, and how can an organisation reduce phishing risks?",
            "Explain the principle of least privilege with an example.",
        ]
    elif any(word in career_lower for word in ["developer", "software", "java", "python", "engineer"]):
        questions = [
            "Explain object-oriented programming and give a practical example.",
            "How would you debug a program that produces an unexpected result?",
            "Describe an API and explain how an application can use one.",
        ]
    else:
        questions = [
            f"What core skills are important for a {target_career}?",
            "Describe a project or task that demonstrates your problem-solving ability.",
            "How would you approach learning an unfamiliar tool or technology?",
        ]

    interview_question = st.selectbox(
        "Select a practice question",
        questions,
        key="job_simulation_question",
    )

    interview_answer = st.text_area(
        "Write your answer",
        placeholder="Type your answer as if you were in a real interview...",
        height=160,
        key="job_simulation_answer",
    )

    if st.button("🤖 Evaluate My Answer", key="evaluate_interview_answer"):
        if not interview_answer.strip():
            st.warning("Please write an answer before requesting feedback.")
        else:
            feedback_prompt = f"""
You are a supportive but honest technical interviewer for CareerNova AI.

Target career: {target_career}
Interview type: {interview_mode}
Interview question: {interview_question}

Candidate's answer:
{interview_answer}

Evaluate the answer using this structure:
1. What the candidate did well
2. Missing points or inaccuracies
3. Specific suggestions to improve
4. A sample improved answer

Be beginner-friendly, constructive, accurate, and specific to the target career.
Do not claim the candidate has experience or skills that they did not mention.
"""

            try:
                with st.spinner("AI is reviewing your answer..."):
                    feedback = get_career_response(
                        feedback_prompt,
                        conversation_history=[],
                    )

                st.session_state["job_interview_feedback"] = feedback
                st.session_state["job_interview_question"] = interview_question
                st.session_state["job_interview_answer"] = interview_answer
                st.session_state["job_interview_career"] = target_career
                st.session_state["job_interview_mode"] = interview_mode

            except Exception as error:
                st.error(
                    "Unable to generate interview feedback right now. "
                    "Please check your AI configuration and try again."
                )
                st.caption(str(error))

    feedback = st.session_state.get("job_interview_feedback")

    if (
        feedback
        and st.session_state.get("job_interview_career") == target_career
    ):
        st.markdown("#### 📝 AI Interview Feedback")
        st.markdown(feedback)

    st.divider()
    st.markdown("### 3. Download Your Readiness Report")

    if (
        st.session_state.get("job_readiness_match")
        and st.session_state.get("job_readiness_career") == target_career
    ):
        result = st.session_state["job_readiness_match"]

        report_lines = [
            "CareerNova AI — Job Readiness Report",
            "=" * 42,
            f"Target career: {target_career}",
            f"Skill match: {result.get('match_percentage', 0)}%",
            "",
            "Matched skills:",
            ", ".join(result.get("matched_skills", [])) or "None detected",
            "",
            "Skills to develop:",
            ", ".join(result.get("missing_skills", [])) or "None detected",
        ]

        if (
            st.session_state.get("job_interview_feedback")
            and st.session_state.get("job_interview_career") == target_career
        ):
            report_lines.extend([
                "",
                "Mock Interview",
                "-" * 20,
                f"Interview type: {st.session_state.get('job_interview_mode', '')}",
                f"Question: {st.session_state.get('job_interview_question', '')}",
                f"Your answer: {st.session_state.get('job_interview_answer', '')}",
                "",
                "AI feedback:",
                str(st.session_state["job_interview_feedback"]),
            ])

        st.download_button(
            "⬇️ Download Readiness Report",
            data="\n".join(report_lines),
            file_name="careernova_job_readiness_report.txt",
            mime="text/plain",
            key="download_job_readiness_report",
        )
    else:
        st.caption(
            "Run the skill-match assessment first to create your report."
        )

else:
    st.warning("No career options were found in the career dataset.")


st.divider()

st.markdown('<div id="career-chatbot"></div>', unsafe_allow_html=True)
st.header("🤖 CareerNova AI Chatbot")

st.write(
    "Ask about career paths, missing skills, internships, projects, "
    "placements, interview preparation, or learning roadmaps. "
    "The chatbot can use your saved profile and career results."
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Display previous messages
for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
if prompt := st.chat_input("Ask your career question..."):

    st.session_state["chat_history"].append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build profile context
    profile_context = ""

    if "student_name" in st.session_state:

        student_name = st.session_state.get(
            "student_name",
            "Student",
        )

        education = st.session_state.get(
            "student_education",
            "Not provided",
        )

        skills = st.session_state.get(
            "student_skills",
            [],
        )

        interests = st.session_state.get(
            "student_interests",
            [],
        )

        career_results = st.session_state.get(
            "career_results",
            [],
        )

        profile_context = (
            "\n\nSTUDENT PROFILE — use when relevant:\n"
            f"Name: {student_name}\n"
            f"Education: {education}\n"
            f"Current skills: {', '.join(skills) or 'Not provided'}\n"
            f"Interests: {', '.join(interests) or 'Not provided'}\n"
        )

        if career_results:
            profile_context += "\nCAREER RECOMMENDATIONS:\n"

            for result in career_results:

                career_name = result.get(
                    "career",
                    "Unknown career",
                )

                match_score = result.get(
                    "match_score",
                    0,
                )

                readiness = calculate_career_readiness(
                    skills,
                    career_name,
                )

                profile_context += (
                    f"\nCareer: {career_name}\n"
                    f"Career match score: {match_score}%\n"
                )

                if readiness:

                    profile_context += (
                        f"Readiness score: "
                        f"{readiness['readiness_score']}%\n"
                        f"Matched skills: "
                        f"{', '.join(readiness['matched_skills']) or 'None'}\n"
                        f"Missing skills: "
                        f"{', '.join(readiness['missing_skills']) or 'None'}\n"
                    )

    # Include the most recent resume analysis when available
    resume_analysis = st.session_state.get("resume_analysis")

    if resume_analysis:
        profile_context += (
            "\nLATEST RESUME ANALYSIS:\n"
            f"Career analyzed: "
            f"{st.session_state.get('resume_analysis_career', 'Unknown')}\n"
            f"Resume skill match: "
            f"{resume_analysis.get('match_percentage', 0)}%\n"
            f"Skills found: "
            f"{', '.join(resume_analysis.get('matched_skills', [])) or 'None'}\n"
            f"Resume skill gaps: "
            f"{', '.join(resume_analysis.get('missing_skills', [])) or 'None'}\n"
        )

    # Combine the question with factual profile context
    question_with_context = (
        f"STUDENT QUESTION:\n{prompt}\n"
        f"{profile_context}\n\n"
        "CAREER GUIDANCE INSTRUCTIONS:\n"
        "- Personalize your answer using the supplied profile and "
        "career recommendations when relevant.\n"
        "- Use the provided scores and skill lists accurately.\n"
        "- Explain the difference between career match and readiness "
        "if the student asks about scores.\n"
        "- Prioritize missing skills and give realistic next steps.\n"
        "- For a learning plan, organize suggestions into weeks "
        "with practical tasks.\n"
        "- Use simple English and clear headings or bullet points.\n"
        "- Do not invent student details, scores, skills, or resources.\n"
        "- Do not guarantee jobs, salaries, internships, or placements.\n"
        "- If no profile is available, explain that the advice is "
        "general and suggest creating a profile."
    )

    with st.chat_message("assistant"):

        with st.spinner("CareerCompass AI is thinking..."):

            answer = get_career_response(
                question_with_context,
                conversation_history=(
                    st.session_state["chat_history"][:-1]
                ),
            )

        st.markdown(answer)

    st.session_state["chat_history"].append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


if st.button("🗑️ Clear Chat", key="clear_career_chat"):

    st.session_state["chat_history"] = []
    st.rerun()


# --------------------------------------------------
# 11. Footer
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="footer">✦ CareerNova AI &nbsp;·&nbsp; '
    'Personalized Career Recommendation Agent<br>'
    'Discover your direction. Develop your potential.</div>',
    unsafe_allow_html=True,
)
