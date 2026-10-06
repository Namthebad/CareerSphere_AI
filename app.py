
import streamlit as st
import sqlite3
import requests
from pypdf import PdfReader

st.set_page_config(
    page_title="CareerSphere AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_NAME = "careersphere.db"

CAREERS = {
    "Data Scientist": {
        "skills": ["python","sql","pandas","numpy","machine learning","statistics","data visualization"],
        "description": "Analyze data, build machine learning models and generate useful business insights.",
        "next_step": "Build a machine learning project using Python."
    },
    "Data Analyst": {
        "skills": ["python","sql","excel","power bi","tableau","statistics","data visualization"],
        "description": "Analyze datasets and create reports and dashboards to support business decisions.",
        "next_step": "Build an interactive dashboard using Power BI."
    },
    "Machine Learning Engineer": {
        "skills": ["python","machine learning","numpy","pandas","scikit-learn","tensorflow","deep learning"],
        "description": "Develop, train and deploy machine learning models for real-world applications.",
        "next_step": "Build and deploy a machine learning model."
    },
    "AI Engineer": {
        "skills": ["python","machine learning","deep learning","tensorflow","pytorch","nlp","generative ai"],
        "description": "Build intelligent applications using AI, machine learning and deep learning.",
        "next_step": "Build an AI application using an LLM."
    },
    "Software Developer": {
        "skills": ["python","java","c","data structures","algorithms","git","sql"],
        "description": "Design and develop software applications using programming and problem-solving skills.",
        "next_step": "Practice DSA and build a software project."
    },
    "Full Stack Developer": {
        "skills": ["html","css","javascript","python","react","sql","git"],
        "description": "Build complete web applications using frontend and backend technologies.",
        "next_step": "Build a complete full-stack web application."
    }
}

ROADMAPS = {
    "Data Scientist": [
        ("1", "Python Fundamentals", "2–3 Weeks", ["Python syntax", "Functions", "OOP basics", "NumPy"]),
        ("2", "SQL & Databases", "2 Weeks", ["SQL queries", "Joins", "Aggregation", "Database basics"]),
        ("3", "Data Analysis", "3 Weeks", ["Pandas", "Data cleaning", "EDA", "Matplotlib"]),
        ("4", "Statistics", "2 Weeks", ["Probability", "Distributions", "Hypothesis testing", "Correlation"]),
        ("5", "Machine Learning", "4 Weeks", ["Regression", "Classification", "Clustering", "Scikit-learn"]),
        ("6", "Portfolio Projects", "3–4 Weeks", ["EDA project", "ML project", "Dashboard", "GitHub portfolio"]),
        ("7", "Interview Preparation", "2–3 Weeks", ["SQL practice", "Python problems", "ML questions", "Mock interviews"]),
    ],
    "Data Analyst": [
        ("1", "Excel", "2 Weeks", ["Formulas", "Pivot tables", "Charts"]),
        ("2", "SQL", "2–3 Weeks", ["SELECT", "JOIN", "GROUP BY", "Subqueries"]),
        ("3", "Python", "3 Weeks", ["Python", "Pandas", "NumPy"]),
        ("4", "Visualization", "2–3 Weeks", ["Power BI", "Tableau", "Dashboards"]),
        ("5", "Statistics", "2 Weeks", ["Descriptive statistics", "Probability", "Testing"]),
        ("6", "Projects", "3 Weeks", ["Sales dashboard", "Customer analysis", "Business report"]),
        ("7", "Placements", "2 Weeks", ["SQL interview", "Case studies", "Resume", "Mock interview"]),
    ],
    "Machine Learning Engineer": [
        ("1", "Python", "3 Weeks", ["Python", "OOP", "NumPy", "Pandas"]),
        ("2", "ML Fundamentals", "4 Weeks", ["Regression", "Classification", "Clustering"]),
        ("3", "Deep Learning", "4 Weeks", ["Neural networks", "TensorFlow", "PyTorch"]),
        ("4", "Deployment", "3 Weeks", ["FastAPI", "Docker basics", "REST APIs"]),
        ("5", "MLOps Basics", "2 Weeks", ["Model serving", "Monitoring", "Versioning"]),
        ("6", "Projects", "4 Weeks", ["Prediction API", "Image classifier", "ML deployment"]),
        ("7", "Interview", "2 Weeks", ["ML theory", "Coding", "System basics"]),
    ],
    "AI Engineer": [
        ("1", "Python", "3 Weeks", ["Python", "OOP", "APIs"]),
        ("2", "Machine Learning", "4 Weeks", ["ML", "Scikit-learn", "Evaluation"]),
        ("3", "Deep Learning", "4 Weeks", ["Neural networks", "CNN", "Transformers"]),
        ("4", "NLP & LLMs", "4 Weeks", ["NLP", "Embeddings", "RAG", "LLMs"]),
        ("5", "Generative AI", "3 Weeks", ["Prompt engineering", "Ollama", "AI APIs"]),
        ("6", "AI Projects", "4 Weeks", ["Chatbot", "RAG app", "AI assistant"]),
        ("7", "Interview", "2 Weeks", ["AI concepts", "Projects", "System design"]),
    ],
    "Software Developer": [
        ("1", "Programming", "3 Weeks", ["Python", "Java", "C basics"]),
        ("2", "DSA", "6 Weeks", ["Arrays", "Strings", "Linked lists", "Trees", "Graphs"]),
        ("3", "OOP", "2 Weeks", ["Classes", "Inheritance", "Polymorphism"]),
        ("4", "Databases", "2 Weeks", ["SQL", "Normalization", "Transactions"]),
        ("5", "Git & Development", "2 Weeks", ["Git", "GitHub", "Debugging"]),
        ("6", "Projects", "4 Weeks", ["Web app", "Java project", "Python project"]),
        ("7", "Placements", "3 Weeks", ["Coding", "Aptitude", "Resume", "Interviews"]),
    ],
    "Full Stack Developer": [
        ("1", "HTML & CSS", "2 Weeks", ["HTML", "CSS", "Responsive design"]),
        ("2", "JavaScript", "3 Weeks", ["JS basics", "DOM", "Async programming"]),
        ("3", "Frontend", "3 Weeks", ["React", "Components", "State"]),
        ("4", "Backend", "3 Weeks", ["Python", "FastAPI", "REST APIs"]),
        ("5", "Database", "2 Weeks", ["SQL", "SQLite", "Database design"]),
        ("6", "Full Stack Projects", "4 Weeks", ["Authentication", "CRUD app", "Deployment"]),
        ("7", "Interview", "2 Weeks", ["JavaScript", "APIs", "SQL", "Projects"]),
    ],
}

def db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, college TEXT, branch TEXT, year TEXT,
        career_goal TEXT, skills TEXT, projects INTEGER, experience TEXT
    )""")
    conn.commit()
    return conn

def get_profile():
    conn = db()
    row = conn.execute("SELECT * FROM profile ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    return row

def save_profile(values):
    conn = db()
    conn.execute("DELETE FROM profile")
    conn.execute("""INSERT INTO profile
        (name,college,branch,year,career_goal,skills,projects,experience)
        VALUES (?,?,?,?,?,?,?,?)""", values)
    conn.commit()
    conn.close()

def skills(profile):
    if not profile or not profile[6]:
        return []
    return [x.strip().lower() for x in profile[6].split(",") if x.strip()]

def matches(a, b):
    a, b = a.lower().strip(), b.lower().strip()
    return a == b or a in b or b in a

def gap(profile):
    career = profile[5] if profile and profile[5] in CAREERS else "Data Scientist"
    required = CAREERS[career]["skills"]
    user = skills(profile)
    found = [x for x in required if any(matches(u, x) for u in user)]
    missing = [x for x in required if x not in found]
    pct = round(len(found) / len(required) * 100) if required else 0
    return career, required, found, missing, pct

def ollama(prompt):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=120,
        )
        if r.status_code != 200:
            return f"❌ Ollama error: status code {r.status_code}"
        return r.json().get("response", "No response generated.")
    except requests.exceptions.ConnectionError:
        return "❌ Ollama is not running. Open Command Prompt and run: ollama serve"
    except requests.exceptions.Timeout:
        return "⏳ Ollama took too long. Try a shorter question."
    except Exception as e:
        return f"❌ Error: {e}"

def resume_text(uploaded):
    reader = PdfReader(uploaded)
    return "\n".join((p.extract_text() or "") for p in reader.pages)

def resume_score(text, career):
    req = CAREERS.get(career, CAREERS["Data Scientist"])["skills"]
    low = text.lower()
    found = [s for s in req if s.lower() in low]
    missing = [s for s in req if s not in found]
    score = round(len(found) / len(req) * 100) if req else 0
    return score, found, missing

# ---------- UI ----------
st.markdown("""
<style>
/* Main page */
.stApp {
    background: #f4f7fb !important;
    color: #182033 !important;
}
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}
[data-testid="stHeader"] {
    background: #f4f7fb !important;
}
/* Keep headings and normal text dark on the light main page */
.main h1, .main h2, .main h3, .main h4,
.main p {
    color: #182033 !important;
}

/* IMPORTANT: Streamlit form labels were previously too light.
   Make every input label clearly visible. */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stTextArea"] label,
[data-testid="stFileUploader"] label,
[data-testid="stSelectSlider"] label {
    color: #182033 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

[data-testid="stTextInput"] label p,
[data-testid="stNumberInput"] label p,
[data-testid="stSelectbox"] label p,
[data-testid="stTextArea"] label p,
[data-testid="stFileUploader"] label p {
    color: #182033 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* Help/description text */
[data-testid="stTextInput"] small,
[data-testid="stNumberInput"] small,
[data-testid="stSelectbox"] small,
[data-testid="stTextArea"] small {
    color: #667085 !important;
}

/* Form labels inside forms */
[data-testid="stForm"] label,
[data-testid="stForm"] label p {
    color: #182033 !important;
    opacity: 1 !important;
    font-weight: 700 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #15122d 0%, #28204d 100%) !important;
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
section[data-testid="stSidebar"] .stRadio label {
    color: #ffffff !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
}

/* Form fields - white and readable */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
textarea {
    background: #ffffff !important;
    color: #182033 !important;
    border: 1px solid #d7dce7 !important;
    border-radius: 10px !important;
}
div[data-baseweb="input"] input,
div[data-baseweb="select"] input,
textarea {
    color: #182033 !important;
    background: #ffffff !important;
}
div[data-baseweb="select"] svg {
    color: #4b5563 !important;
}
[data-testid="stNumberInput"] input {
    color: #182033 !important;
    background: #ffffff !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    border-radius: 10px !important;
    border: 0 !important;
    background: linear-gradient(90deg, #6c5ce7, #8e44ad) !important;
    color: white !important;
    font-weight: 700 !important;
    min-height: 44px;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    opacity: .92;
}

/* Cards */
.cs-card {
    background: #ffffff;
    border: 1px solid #e4e8f0;
    border-radius: 18px;
    padding: 24px;
    margin: 12px 0;
    box-shadow: 0 7px 22px rgba(31, 41, 55, .07);
}
.cs-hero {
    background: linear-gradient(135deg, #5f4bd8, #8e44ad);
    color: white !important;
    border-radius: 22px;
    padding: 30px;
    margin-bottom: 24px;
    box-shadow: 0 10px 28px rgba(95,75,216,.22);
}
.cs-hero h1, .cs-hero h2, .cs-hero p {
    color: white !important;
    margin: 0 0 7px 0;
}
.cs-label {
    font-weight: 700;
    color: #344054 !important;
    margin-bottom: 6px;
}
.metric-card {
    background: white;
    border: 1px solid #e4e8f0;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
}
.metric-title { color: #667085 !important; font-size: 14px; }
.metric-value { color: #182033 !important; font-size: 28px; font-weight: 800; }

/* File uploader */
[data-testid="stFileUploader"] {
    background: white !important;
    border-radius: 14px !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "interview_question" not in st.session_state:
    st.session_state.interview_question = ""
if "interview_evaluation" not in st.session_state:
    st.session_state.interview_evaluation = ""

profile = get_profile()

# Sidebar
with st.sidebar:
    st.markdown("## 🎓 CareerSphere AI")
    st.markdown("**Intelligent Career & Employability Assistant**")
    st.markdown("---")
    nav = {
        "🏠 Dashboard": "Dashboard",
        "👤 My Profile": "My Profile",
        "🎯 Career Recommendations": "Career Recommendations",
        "📊 Skill Gap Analyzer": "Skill Gap Analyzer",
        "📄 Resume Analyzer": "Resume Analyzer",
        "🗺️ Learning Roadmap": "Learning Roadmap",
        "🤖 AI Career Assistant": "AI Career Assistant",
        "🎤 Interview Practice": "Interview Practice",
    }
    selected = st.radio("Navigation", list(nav.keys()), index=list(nav.values()).index(st.session_state.page))
    st.session_state.page = nav[selected]
    st.markdown("---")
    st.caption("Streamlit • SQLite • Ollama")

page = st.session_state.page

# Dashboard
if page == "Dashboard":
    if not profile:
        st.markdown("""
        <div class="cs-hero">
            <h1>Welcome to CareerSphere AI 🚀</h1>
            <p>Your intelligent career and employability assistant.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="cs-card"><h3>👋 Let’s build your career plan</h3><p>Create your student profile to unlock career recommendations, skill analysis, resume analysis, learning roadmap, AI guidance and mock interviews.</p></div>', unsafe_allow_html=True)
        if st.button("👤 Create My Profile", use_container_width=True):
            st.session_state.page = "My Profile"
            st.rerun()
    else:
        career, req, found, missing, pct = gap(profile)
        st.markdown(f"""
        <div class="cs-hero">
            <h1>Welcome back, {profile[1]}! 👋</h1>
            <p>Target Career: <b>{career}</b></p>
        </div>
        """, unsafe_allow_html=True)
        cols = st.columns(4)
        vals = [(f"{pct}%", "Career Match"), (str(profile[7]), "Projects"),
                (str(len(skills(profile))), "Skills"), (profile[8], "Experience")]
        for c, (v, t) in zip(cols, vals):
            c.markdown(f'<div class="metric-card"><div class="metric-title">{t}</div><div class="metric-value">{v}</div></div>', unsafe_allow_html=True)
        st.markdown("### 🎯 Recommended Next Step")
        st.success(CAREERS[career]["next_step"])

# Profile
elif page == "My Profile":
    st.markdown('<div class="cs-hero"><h1>👤 My Profile</h1><p>Enter your details to personalize CareerSphere AI.</p></div>', unsafe_allow_html=True)
    e = profile
    branches = ["Data Science","Computer Science","Artificial Intelligence","Information Technology","Electronics","Other"]
    years = ["1st Year","2nd Year","3rd Year","4th Year"]
    careers = list(CAREERS.keys()) + ["Other"]
    exps = ["Beginner","Intermediate","Advanced"]

    with st.form("profile_form"):
        st.markdown('<div class="cs-card">', unsafe_allow_html=True)
        st.markdown('<div class="cs-label">👤 Full Name</div>', unsafe_allow_html=True)
        name = st.text_input("Name", value=e[1] if e else "", placeholder="Enter your full name", label_visibility="collapsed")
        st.markdown('<div class="cs-label">🏫 College Name</div>', unsafe_allow_html=True)
        college = st.text_input("College", value=e[2] if e else "", placeholder="Enter your college name", label_visibility="collapsed")
        st.markdown('<div class="cs-label">🎓 Branch</div>', unsafe_allow_html=True)
        branch = st.selectbox("Branch", branches, index=branches.index(e[3]) if e and e[3] in branches else 0, label_visibility="collapsed")
        st.markdown('<div class="cs-label">📅 Year</div>', unsafe_allow_html=True)
        year = st.selectbox("Year", years, index=years.index(e[4]) if e and e[4] in years else 1, label_visibility="collapsed")
        st.markdown('<div class="cs-label">🎯 Target Career</div>', unsafe_allow_html=True)
        career = st.selectbox("Target Career", careers, index=careers.index(e[5]) if e and e[5] in careers else 0, label_visibility="collapsed")
        st.markdown('<div class="cs-label">💻 Your Skills</div>', unsafe_allow_html=True)
        st.caption("Enter skills separated by commas. Example: Python, SQL, Pandas")
        user_skills = st.text_input("Skills", value=e[6] if e else "Python, C, SQL", placeholder="Python, SQL, Pandas", label_visibility="collapsed")
        st.markdown('<div class="cs-label">📁 Number of Projects</div>', unsafe_allow_html=True)
        projects = st.number_input("Projects", min_value=0, max_value=100, value=int(e[7]) if e else 0, label_visibility="collapsed")
        st.markdown('<div class="cs-label">⭐ Experience Level</div>', unsafe_allow_html=True)
        experience = st.selectbox("Experience", exps, index=exps.index(e[8]) if e and e[8] in exps else 0, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
        elif not college.strip():
            st.error("Please enter your college.")
        else:
            save_profile((name.strip(), college.strip(), branch, year, career, user_skills, projects, experience))
            st.success("✅ Profile saved successfully!")
            st.rerun()

# Career Recommendations
elif page == "Career Recommendations":
    st.markdown('<div class="cs-hero"><h1>🎯 Career Recommendations</h1><p>Find careers that match your current skills.</p></div>', unsafe_allow_html=True)
    if not profile:
        st.warning("Create your profile first.")
    else:
        user = skills(profile)
        results = []
        for career, info in CAREERS.items():
            found = [s for s in info["skills"] if any(matches(u, s) for u in user)]
            score = round(len(found) / len(info["skills"]) * 100)
            results.append((career, score, found, info))
        results.sort(key=lambda x: x[1], reverse=True)
        for i, (career, score, found, info) in enumerate(results[:5], 1):
            with st.container(border=True):
                st.subheader(f"{i}. {career}")
                st.progress(score / 100)
                st.write(f"**Match: {score}%**")
                st.write(info["description"])
                st.write("**Matched skills:** " + (", ".join(found) if found else "None"))

# Skill Gap
elif page == "Skill Gap Analyzer":
    st.markdown('<div class="cs-hero"><h1>📊 Skill Gap Analyzer</h1><p>See what you already know and what to learn next.</p></div>', unsafe_allow_html=True)
    if not profile:
        st.warning("Create your profile first.")
    else:
        career, req, found, missing, pct = gap(profile)
        st.subheader(f"Target Career: {career}")
        st.progress(pct / 100)
        st.metric("Skill Match", f"{pct}%")
        a, b = st.columns(2)
        with a:
            st.markdown("### ✅ Skills You Have")
            for x in found:
                st.success(x)
        with b:
            st.markdown("### 📚 Skills to Learn")
            for x in missing:
                st.warning(x)

# Resume
elif page == "Resume Analyzer":
    st.markdown('<div class="cs-hero"><h1>📄 Resume Analyzer</h1><p>Upload your PDF resume and check its match with your target career.</p></div>', unsafe_allow_html=True)
    if not profile:
        st.warning("Create your profile first.")
    else:
        career = profile[5] if profile[5] in CAREERS else "Data Scientist"
        uploaded = st.file_uploader("Upload Resume PDF", type=["pdf"])
        if uploaded:
            text = resume_text(uploaded)
            score, found, missing = resume_score(text, career)
            a,b,c = st.columns(3)
            a.metric("Career Match", f"{score}%")
            b.metric("Skills Found", len(found))
            c.metric("Skills Missing", len(missing))
            st.progress(score / 100)
            st.markdown("### ✅ Skills Found")
            st.write(", ".join(found) if found else "No matching skills detected.")
            st.markdown("### ❌ Skills Missing")
            st.write(", ".join(missing) if missing else "Excellent! Required skills detected.")
            with st.expander("View Extracted Resume Text"):
                st.text(text[:20000])

# Roadmap
elif page == "Learning Roadmap":
    st.markdown('<div class="cs-hero"><h1>🗺️ Learning Roadmap</h1><p>Your step-by-step path toward your target career.</p></div>', unsafe_allow_html=True)
    if not profile:
        st.warning("Create your profile first.")
    else:
        career = profile[5] if profile[5] in ROADMAPS else "Data Scientist"
        for number, title, duration, topics in ROADMAPS[career]:
            with st.container(border=True):
                st.markdown(f"### {number}. {title}")
                st.caption(f"Duration: {duration}")
                st.write(" • ".join(topics))

# AI Assistant
elif page == "AI Career Assistant":
    st.markdown('<div class="cs-hero"><h1>🤖 AI Career Assistant</h1><p>Ask personalized career questions powered by Ollama.</p></div>', unsafe_allow_html=True)
    if not profile:
        st.warning("Create your profile first.")
    else:
        q = st.chat_input("Ask CareerSphere AI...")
        if q:
            st.chat_message("user").write(q)
            prompt = f"""You are CareerSphere AI.
Student: {profile[1]}
Branch: {profile[3]}
Year: {profile[4]}
Target career: {profile[5]}
Skills: {profile[6]}
Projects: {profile[7]}
Experience: {profile[8]}

Give practical, beginner-friendly advice for this question:
{q}
"""
            with st.spinner("AI is thinking..."):
                answer = ollama(prompt)
            st.chat_message("assistant").write(answer)

# Interview
elif page == "Interview Practice":
    st.markdown('<div class="cs-hero"><h1>🎤 AI Interview Practice</h1><p>Practice technical and HR interview questions.</p></div>', unsafe_allow_html=True)
    if not profile:
        st.warning("Create your profile first.")
    else:
        mode = st.selectbox("Interview Type", ["Technical Interview", "HR Interview"])
        if not st.session_state.interview_started:
            st.info("Click Start Interview to generate your first personalized question.")
            if st.button("🚀 Start Interview", use_container_width=True):
                prompt = f"""Act as an interviewer for a college student.
Target career: {profile[5]}
Skills: {profile[6]}
Experience: {profile[8]}
Interview type: {mode}
Ask one realistic interview question. Return only the question."""
                with st.spinner("Generating question..."):
                    st.session_state.interview_question = ollama(prompt)
                st.session_state.interview_started = True
                st.rerun()
        else:
            st.info(f"Interview type: {mode}")
            st.markdown(f"### ❓ {st.session_state.interview_question}")
            answer = st.text_area("Your Answer", height=180, placeholder="Type your answer here...")
            if st.button("✅ Evaluate My Answer", use_container_width=True):
                if not answer.strip():
                    st.warning("Please enter your answer.")
                else:
                    prompt = f"""You are an expert interview evaluator.
Career: {profile[5]}
Interview type: {mode}
Question: {st.session_state.interview_question}
Candidate answer: {answer}

Evaluate with:
SCORE: X/10
STRENGTHS:
- point
WEAKNESSES:
- point
IMPROVEMENTS:
- point
IDEAL ANSWER:
Give a short ideal answer."""
                    with st.spinner("Evaluating..."):
                        st.session_state.interview_evaluation = ollama(prompt)
                    st.rerun()

            if st.session_state.interview_evaluation:
                st.markdown("### 📋 AI Evaluation")
                st.markdown(st.session_state.interview_evaluation)

            if st.button("➡️ Next Question", use_container_width=True):
                prompt = f"""Act as an interviewer for a college student.
Target career: {profile[5]}
Skills: {profile[6]}
Interview type: {mode}
Generate a different interview question from the previous one:
{st.session_state.interview_question}
Return only the new question."""
                with st.spinner("Generating next question..."):
                    st.session_state.interview_question = ollama(prompt)
                st.session_state.interview_evaluation = ""
                st.rerun()

            if st.button("🔄 Reset Interview"):
                st.session_state.interview_started = False
                st.session_state.interview_question = ""
                st.session_state.interview_evaluation = ""
                st.rerun()
