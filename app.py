import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

# ------------------------------------------------------------------
# CONFIGURATION & INITIALIZATION
# ------------------------------------------------------------------
load_dotenv()

LOGO_URL = "https://i.ibb.co/99kLMQJb/IMG-20260801-WA0001.jpg"

supabase_url = os.getenv("SUPABASE_URL", "")
supabase_key = os.getenv("SUPABASE_KEY", "")

# Initialize Supabase client
supabase = create_client(supabase_url, supabase_key) if (supabase_url and supabase_key) else None

# Safe imports for LangGraph workflows and actions
try:
    from graphs.screening_graph import screening_graph
    from graphs.decision_graph import decision_graph
    from nodes.book_interview import book_interview_slot
except ImportError:
    screening_graph = None
    decision_graph = None
    book_interview_slot = None

st.set_page_config(
    page_title="Agentick Employees - Custom AI Agents & Hiring Portal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------
# BRANDING & LIGHT THEME OVERRIDES (CUSTOM SIDEBAR & CARDS)
# ------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* 0. FORCE SANS-SERIF ON HEADINGS & MARKDOWN TEXT
       Streamlit's default theme sets an explicit font (often a serif) on
       heading tags and markdown containers with high specificity, which
       overrides the inherited font-family from html/body/.stApp below.
       These selectors target those elements directly so nothing falls
       back to Streamlit's default font. */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    [data-testid="stHeading"], [data-testid="stHeading"] *,
    .stMarkdown p, .stMarkdown li, .stMarkdown span, .stMarkdown div,
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] *,
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    /* 1. GLOBAL LIGHT THEME FORCE */
    html, body, [class*="css"], .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }}

    /* Hide Default Streamlit Headers */
    header, #MainMenu, footer, .stDeployButton, div[data-testid="stHeader"] {{
        display: none !important;
        visibility: hidden !important;
    }}

    /* 2. FORM LABELS */
    label, [data-testid="stWidgetLabel"], label p, label span {{
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    /* 3. DROPDOWNS & SELECTBOXES */
    div[data-testid="stSelectbox"] > div > div,
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        color: #0F172A !important;
    }}

    div[data-baseweb="select"] * {{
        color: #0F172A !important;
        background-color: transparent !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    div[data-baseweb="select"] svg {{
        fill: #0284C7 !important;
        color: #0284C7 !important;
    }}

    /* 4. BUTTON STYLING (IMAGE 2 DESIGN MATCH) */
    /* Primary Button: Solid Brand Blue with Pure White Text */
    div[data-testid="stFormSubmitButton"] > button,
    .stButton > button[kind="primary"],
    div[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
        border: 1.5px solid #0284C7 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 14.5px !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        padding: 12px 18px !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.22) !important;
        transition: all 0.2s ease-in-out !important;
    }}

    /* Secondary Button / Unselected Nav: White Box with Blue Border & Blue Text */
    .stButton > button[kind="secondary"], 
    .stButton > button:not([kind="primary"]),
    div[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {{
        background-color: #FFFFFF !important;
        color: #0284C7 !important;
        border: 1.5px solid #0284C7 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 14.5px !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        padding: 12px 18px !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.2s ease-in-out !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
    }}

    /* 5. EXPANDERS & HEADERS */
    div[data-testid="stExpander"] {{
        border: 1px solid #BAE6FD !important;
        border-radius: 12px !important;
        background-color: #FFFFFF !important;
        overflow: hidden !important;
    }}

    div[data-testid="stExpander"] summary {{
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
        padding: 12px 18px !important;
        border-radius: 10px !important;
    }}

    div[data-testid="stExpander"] summary p,
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary svg {{
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-weight: 700 !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    /* 6. CODE BACKTICKS & BADGES */
    code, .stMarkdown code {{
        background-color: #E0F2FE !important;
        color: #0369A1 !important;
        border: 1px solid #BAE6FD !important;
        border-radius: 8px !important;
        padding: 3px 8px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }}

    /* 7. INPUT FIELDS */
    input, textarea, 
    div[data-baseweb="input"] input, 
    div[data-baseweb="textarea"] textarea {{
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    div[data-baseweb="input"], 
    div[data-baseweb="textarea"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }}

    /* 8. CARDS & BADGES (IMAGE 4 BOXED STYLE) */
    .ae-card {{
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }}

    .ae-inner-box {{
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 14px;
        color: #334155;
        font-size: 14px;
        line-height: 1.6;
    }}

    .badge-blue {{
        display: inline-flex;
        align-items: center;
        background-color: #E0F2FE;
        color: #0369A1;
        border: 1px solid #BAE6FD;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 12.5px;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }}

    .badge-score {{
        display: inline-flex;
        align-items: center;
        background-color: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 12.5px;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }}

    .badge-status-declined {{
        background-color: #FFE4E6;
        color: #BE123C;
        border: 1px solid #FECDD3;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 700;
    }}

    .badge-status-booked {{
        background-color: #FEF3C7;
        color: #B45309;
        border: 1px solid #FDE68A;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 700;
    }}

    .badge-status-hired {{
        background-color: #DCFCE7;
        color: #15803D;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 700;
    }}

    .brand-navbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0px 18px 0px;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 28px;
    }}
    
    .brand-logo-img {{
        height: 40px;
        width: auto;
        border-radius: 8px;
        object-fit: contain;
    }}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SESSION STATE MANAGEMENT
# ------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "public_view" not in st.session_state:
    st.session_state["public_view"] = "portal"

if "hr_menu" not in st.session_state:
    st.session_state["hr_menu"] = "Candidate Evaluation Dashboard"


# ==================================================================
# 1. PUBLIC CANDIDATE PORTAL (FRONT PAGE)
# ==================================================================
if not st.session_state["authenticated"]:
    st.markdown("<style>section[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)

    nav_col1, nav_col2 = st.columns([5, 1])
    
    with nav_col1:
        st.markdown(f"""
            <div class="brand-navbar">
                <div style="display:flex; align-items:center; gap:12px;">
                    <img src="{LOGO_URL}" class="brand-logo-img" alt="Agentick Logo" />
                    <span style="font-size:20px; font-weight:800; color:#0F172A; letter-spacing:-0.4px;">Agentick Employees</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with nav_col2:
        st.write("")
        if st.session_state["public_view"] == "portal":
            if st.button("🔐 HR Login", key="top_login_btn", type="secondary", use_container_width=True):
                st.session_state["public_view"] = "login"
                st.rerun()
        else:
            if st.button("⬅️ Careers", key="top_back_btn", type="secondary", use_container_width=True):
                st.session_state["public_view"] = "portal"
                st.rerun()

    # CANDIDATE CAREERS PAGE
    if st.session_state["public_view"] == "portal":
        st.markdown('<div class="badge-blue"><span style="margin-right:6px; color:#0284C7;">•</span> AI Automation Agency</div>', unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 38px; font-weight: 800; color: #0F172A; margin-bottom: 8px; letter-spacing: -0.5px;'>Hire AI employees that run your business operations</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 15px; color: #64748B; margin-bottom: 32px;'>We build custom AI agents and automations. Apply for open positions below for automated AI evaluation.</p>", unsafe_allow_html=True)

        jobs = []
        if supabase:
            try:
                jobs_res = supabase.table("jobs").select("id, title, description").order("created_at", desc=True).execute()
                jobs = jobs_res.data or []
            except Exception as e:
                st.error(f"Error fetching jobs: {e}")

        if not jobs:
            st.info("No active position postings currently open. Please check back soon.")
        else:
            job_options = {f"{j['title']}": j for j in jobs}
            selected_job_label = st.selectbox("🎯 Target Position:", list(job_options.keys()))
            selected_job = job_options[selected_job_label]

            with st.expander("📄 Position Details & Requirements", expanded=True):
                st.write(selected_job["description"])

            st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-weight: 700; color: #0F172A;'>📝 Submit Your Application</h3>", unsafe_allow_html=True)

            with st.form("candidate_apply_form", clear_on_submit=True):
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    cand_name = st.text_input("Full Name", placeholder="e.g. Alex Morgan")
                with col_f2:
                    cand_email = st.text_input("Email Address", placeholder="e.g. alex.morgan@gmail.com")
                
                resume_link = st.text_input("Resume URL / Google Drive Link", placeholder="https://drive.google.com/your-resume-link")
                
                submit_app = st.form_submit_button("Submit Application →", use_container_width=True)

                if submit_app:
                    if cand_name and cand_email and resume_link:
                        with st.spinner("Processing application through AI evaluation agent..."):
                            if screening_graph:
                                screening_input = {
                                    "job_id": selected_job["id"],
                                    "job_title": selected_job["title"],
                                    "job_description": selected_job["description"],
                                    "candidate_name": cand_name,
                                    "candidate_email": cand_email,
                                    "resume_paths": [resume_link],
                                    "candidate_ids": [],
                                    "ranked_candidates": []
                                }
                                screening_graph.invoke(screening_input)
                                st.success("🎉 Application submitted! Our AI screening agent has processed your resume.")
                            else:
                                st.warning("Screening workflow engine not attached. Resume stored.")
                    else:
                        st.error("Please fill in all required fields before submitting.")

    # DEDICATED HR LOGIN PAGE
    elif st.session_state["public_view"] == "login":
        col_s1, col_form, col_s2 = st.columns([1, 2, 1])
        
        with col_form:
            st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:28px; text-align: center; margin-top: 20px;">
                    <img src="{LOGO_URL}" class="brand-logo-img" style="height: 52px; margin-bottom: 12px;" alt="Agentick Logo" />
                    <h2 style="margin: 0 0 4px 0; color: #0F172A; font-weight: 800;">HR Admin Portal</h2>
                    <p style="color: #64748B; font-size: 13px; margin-bottom: 20px;">Sign in to review candidate scores and manage roles.</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("hr_login_form"):
                username = st.text_input("Username", placeholder="Enter admin username")
                password = st.text_input("Password", type="password", placeholder="Enter admin password")
                submit_login = st.form_submit_button("Sign In to Portal", use_container_width=True)

                if submit_login:
                    admin_user = os.getenv("HR_USERNAME", "admin")
                    admin_pass = os.getenv("HR_PASSWORD", "admin123")

                    if username == admin_user and password == admin_pass:
                        st.session_state["authenticated"] = True
                        st.session_state["public_view"] = "portal"
                        st.success("Authenticated successfully.")
                        st.rerun()
                    else:
                        st.error("Invalid credentials entered.")


# ==================================================================
# 2. AUTHENTICATED HR MANAGEMENT PORTAL
# ==================================================================
else:
    # SIDEBAR HEADER MATCHING WEBSITE
    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 6px 0 16px 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 16px;">
            <img src="{LOGO_URL}" class="brand-logo-img" style="height: 38px;" alt="Agentick Logo" />
            <div>
                <strong style="font-size: 16px; color: #0F172A; display: block; line-height: 1.2;">Agentick HR</strong>
                <span style="font-size: 11px; color: #0284C7; font-weight: 700;">Internal Operations</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<p style='font-size:12px; font-weight:700; color:#64748B; text-transform:uppercase; margin-bottom:12px;'>NAVIGATION</p>", unsafe_allow_html=True)

    # DYNAMIC BUTTON NAVIGATION (MATCHES IMAGE 2 BLUE / WHITE BOX BUTTONS)
    nav1_type = "primary" if st.session_state["hr_menu"] == "Candidate Evaluation Dashboard" else "secondary"
    nav2_type = "primary" if st.session_state["hr_menu"] == "Job Position Management" else "secondary"

    if st.sidebar.button("📊 Candidate Evaluation Dashboard", key="nav_cand_btn", type=nav1_type, use_container_width=True):
        st.session_state["hr_menu"] = "Candidate Evaluation Dashboard"
        st.rerun()

    st.sidebar.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    if st.sidebar.button("⚙️ Job Position Management", key="nav_jobs_btn", type=nav2_type, use_container_width=True):
        st.session_state["hr_menu"] = "Job Position Management"
        st.rerun()

    hr_menu = st.session_state["hr_menu"]

    st.sidebar.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
    st.sidebar.caption("Active Session: **Administrator**")
    if st.sidebar.button("🔒 Sign Out", key="sidebar_signout", type="secondary", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["public_view"] = "portal"
        st.rerun()

    # --------------------------------------------------------------
    # DASHBOARD 1: HR CANDIDATE DASHBOARD
    # --------------------------------------------------------------
    if hr_menu == "Candidate Evaluation Dashboard":
        st.markdown("<h2 style='font-weight: 800; color: #0F172A; letter-spacing: -0.5px;'>📊 Candidate Evaluation Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 14px; margin-bottom: 24px;'>Review automated candidate match scores, AI rationales, and trigger offer letters or rejections.</p>", unsafe_allow_html=True)

        candidates = []
        if supabase:
            try:
                candidates_res = supabase.table("candidates").select("*, jobs(id, title)").order("created_at", desc=True).execute()
                candidates = candidates_res.data or []
            except Exception as e:
                st.error(f"Error fetching candidates: {e}")

        # Metrics calculation
        m_total = len(candidates)
        m_booked = len([c for c in candidates if c.get("status") == "booked"])
        m_hired = len([c for c in candidates if c.get("status") == "hired"])
        m_declined = len([c for c in candidates if c.get("status") in ["declined", "rejected"]])

        # BRANDED HTML KPI METRIC CARDS
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 28px;">
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <span style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">Total Applicants</span>
                <div style="font-size: 32px; font-weight: 800; color: #0F172A; margin-top: 4px;">{m_total}</div>
            </div>
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <span style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">Interviews Booked</span>
                <div style="font-size: 32px; font-weight: 800; color: #0284C7; margin-top: 4px;">{m_booked}</div>
            </div>
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <span style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">Offers Extended</span>
                <div style="font-size: 32px; font-weight: 800; color: #16A34A; margin-top: 4px;">{m_hired}</div>
            </div>
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <span style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">Screened Out</span>
                <div style="font-size: 32px; font-weight: 800; color: #E11D48; margin-top: 4px;">{m_declined}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Filters
        jobs_list = []
        if supabase:
            try:
                jobs_res = supabase.table("jobs").select("id, title").order("created_at", desc=True).execute()
                jobs_list = jobs_res.data or []
            except Exception:
                pass
        
        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            job_filter_options = ["All Positions"] + [f"{j['title']}" for j in jobs_list]
            selected_job_filter = st.selectbox("Filter By Job Title:", job_filter_options)

        with filter_col2:
            filter_status = st.selectbox(
                "Filter By Candidate Status:",
                ["All Candidates", "Interviews Booked (Pending Decision)", "Screened Out by AI", "Hired", "Rejected"]
            )

        # Filter Logic
        filtered_cands = candidates
        if selected_job_filter != "All Positions":
            filtered_cands = [c for c in filtered_cands if c.get("jobs") and c["jobs"].get("title") == selected_job_filter]

        if filter_status == "Interviews Booked (Pending Decision)":
            filtered_cands = [c for c in filtered_cands if c.get("status") == "booked"]
        elif filter_status == "Screened Out by AI":
            filtered_cands = [c for c in filtered_cands if c.get("status") == "declined"]
        elif filter_status == "Hired":
            filtered_cands = [c for c in filtered_cands if c.get("status") == "hired"]
        elif filter_status == "Rejected":
            filtered_cands = [c for c in filtered_cands if c.get("status") == "rejected"]

        st.caption(f"Showing {len(filtered_cands)} candidate record(s)")
        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        if not filtered_cands:
            st.info("No candidates found matching the selected criteria.")
        else:
            for cand in filtered_cands:
                cand_id = cand["id"]
                cand_name = cand.get("name", "N/A")
                cand_email = cand.get("email", "N/A")
                cand_status = str(cand.get("status", "parsed")).lower()
                cand_score = cand.get("score", "N/A")
                cand_rationale = cand.get("rationale", "No AI assessment rationale recorded.")
                job_title = cand.get("jobs", {}).get("title", "Unassigned Position") if cand.get("jobs") else "Unassigned Position"

                # Status Badge HTML
                if cand_status in ["declined", "rejected"]:
                    status_badge_html = f'<span class="badge-status-declined">{cand_status.upper()}</span>'
                elif cand_status == "booked":
                    status_badge_html = f'<span class="badge-status-booked">BOOKED</span>'
                elif cand_status == "hired":
                    status_badge_html = f'<span class="badge-status-hired">HIRED</span>'
                else:
                    status_badge_html = f'<span class="badge-score">{cand_status.upper()}</span>'

                with st.container():
                    col1, col2 = st.columns([3.2, 1])

                    with col1:
                        st.markdown(f"""
                        <div class="ae-card">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                                <h3 style="margin:0; font-weight:800; color:#0F172A; font-size:18px;">👤 {cand_name}</h3>
                                {status_badge_html}
                            </div>
                            <div style="margin-bottom: 12px;">
                                <span class="badge-blue">📧 Email: {cand_email}</span>
                                <span class="badge-blue">💼 Role: {job_title}</span>
                                <span class="badge-score">Match Score: {cand_score}/100</span>
                            </div>
                            <div class="ae-inner-box">
                                <strong style="color:#0284C7; display:block; margin-bottom:4px; font-size:12px; text-transform:uppercase;">AI Evaluation Rationale:</strong>
                                "{cand_rationale}"
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.write("")
                        if cand_status == "booked":
                            st.caption("Post-Interview Action:")
                            if st.button("✅ HIRE", key=f"hire_{cand_id}", type="primary", use_container_width=True):
                                with st.spinner("Dispatching offer letter..."):
                                    if decision_graph:
                                        decision_graph.invoke({
                                            "candidate_id": cand_id,
                                            "decision": "hire",
                                            "result": None
                                        })
                                st.success(f"Hired {cand_name}!")
                                st.rerun()

                            if st.button("❌ REJECT", key=f"reject_{cand_id}", use_container_width=True):
                                with st.spinner("Sending rejection notice..."):
                                    if decision_graph:
                                        decision_graph.invoke({
                                            "candidate_id": cand_id,
                                            "decision": "reject",
                                            "result": None
                                        })
                                st.info(f"Rejected {cand_name}.")
                                st.rerun()

                        elif cand_status in ["rejected", "declined"]:
                            st.caption("Manual Action:")
                            if st.button("📅 BOOK MEETING", key=f"override_{cand_id}", use_container_width=True):
                                with st.spinner("Sending interview invitation..."):
                                    if book_interview_slot:
                                        book_interview_slot(
                                            candidate_id=cand_id,
                                            candidate_name=cand_name,
                                            candidate_email=cand_email,
                                            job_title=job_title,
                                            supabase=supabase
                                        )
                                st.success(f"Meeting booked for {cand_name}!")
                                st.rerun()

                        elif cand_status == "hired":
                            st.success("🎉 Offer Extended")

    # --------------------------------------------------------------
    # DASHBOARD 2: JOB POSITION MANAGEMENT
    # --------------------------------------------------------------
    elif hr_menu == "Job Position Management":
        st.markdown("<h2 style='font-weight: 800; color: #0F172A; letter-spacing: -0.5px;'>⚙️ Job Position Management</h2>", unsafe_allow_html=True)
        st.write("Publish new open positions or manage existing roles.")

        tab1, tab2 = st.tabs(["📋 Published Roles", "➕ Create New Position"])

        with tab1:
            jobs = []
            if supabase:
                try:
                    jobs_res = supabase.table("jobs").select("*").order("created_at", desc=True).execute()
                    jobs = jobs_res.data or []
                except Exception as e:
                    st.error(f"Error loading jobs: {e}")

            if not jobs:
                st.info("No active position listings found.")
            else:
                for job in jobs:
                    job_id = job["id"]
                    job_title = job["title"]
                    job_desc = job["description"]
                    created_at = job.get("created_at", "N/A")[:10]

                    candidate_count = 0
                    if supabase:
                        try:
                            cand_count_res = supabase.table("candidates").select("id", count="exact").eq("job_id", job_id).execute()
                            candidate_count = cand_count_res.count if cand_count_res.count is not None else 0
                        except Exception:
                            pass

                    # IMAGE 4 BOXED CARD STRUCTURE
                    with st.container():
                        st.markdown(f"""
                        <div class="ae-card">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                                <div>
                                    <h2 style="margin:0 0 10px 0; font-weight:800; color:#0F172A; font-size:20px;">💼 {job_title}</h2>
                                    <div>
                                        <span class="badge-blue">ID: {job_id}</span>
                                        <span class="badge-blue">Published: {created_at}</span>
                                        <span class="badge-score">Applicants: {candidate_count}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="ae-inner-box">
                                <strong style="color:#0284C7; display:block; margin-bottom:6px; font-size:12px; text-transform:uppercase;">Role Specifications & Details:</strong>
                                <div style="white-space: pre-wrap; font-size: 13.5px; color: #334155; line-height: 1.6;">{job_desc}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Action button row inside container
                        btn_col1, btn_col2 = st.columns([4, 1])
                        with btn_col2:
                            if st.button("🗑️ Delete Position", key=f"del_job_{job_id}", type="secondary", use_container_width=True):
                                if supabase:
                                    try:
                                        supabase.table("candidates").delete().eq("job_id", job_id).execute()
                                        supabase.table("jobs").delete().eq("id", job_id).execute()
                                        st.success(f"Deleted '{job_title}'")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error deleting job position: {e}")
                        st.markdown("<div style='margin-bottom: 18px;'></div>", unsafe_allow_html=True)

        with tab2:
            st.subheader("Publish a New Open Position")
            with st.form("create_job_form", clear_on_submit=True):
                new_title = st.text_input("Job Title", placeholder="e.g. AI Workflow Specialist")
                new_desc = st.text_area("Job Description & Skill Requirements", height=180, placeholder="Describe candidate role expectations, tech stack, and evaluation criteria...")
                submit_job = st.form_submit_button("🚀 Publish Position", type="primary", use_container_width=True)

                if submit_job:
                    if new_title and new_desc:
                        if supabase:
                            try:
                                supabase.table("jobs").insert({
                                    "title": new_title,
                                    "description": new_desc
                                }).execute()
                                st.success(f"Successfully published position: '{new_title}'!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error publishing job: {e}")
                    else:
                        st.error("Please enter both a title and description before publishing.")
