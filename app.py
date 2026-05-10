import streamlit as st
import pandas as pd

# --- LUXURY STYLING ---
st.set_page_config(page_title="Premium MCQ Portal", layout="wide")

st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    /* Luxury Header */
    .main-title {
        font-size: 50px;
        font-weight: 700;
        color: #FFD700; /* Gold color */
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px #000000;
    }
    /* Custom Card Style for Questions */
    .question-card {
        background-color: #1e2130;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #FFD700;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #FFD700 !important;
        color: #000 !important;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #e6c200 !important;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'mcqs' not in st.session_state: st.session_state.mcqs = []
if 'results' not in st.session_state: st.session_state.results = []

st.markdown('<h1 class="main-title">EXAM PORTAL PRO</h1>', unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.image("https://flaticon.com", width=100)
    st.title("Navigation")
    choice = st.radio("Go to:", ["Student: Take Test", "Teacher: Upload Quiz", "Admin: View Results"])
    st.info("System Status: Online")

# --- TEACHER: UPLOAD QUIZ (With Password) ---
if choice == "Teacher: Upload Quiz":
    st.subheader("🔑 Secure Upload Panel")
    upload_pass = st.text_input("Enter Upload Password", type="password")
    
    # MASTER PASSWORD FOR UPLOADING
    if upload_pass == "teacher2024": 
        st.success("Access Granted")
        uploaded_file = st.file_uploader("Upload MCQ CSV", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.session_state.mcqs = df.to_dict('records')
            st.balloons()
            st.success(f"Loaded {len(df)} questions successfully!")
    elif upload_pass:
        st.error("Incorrect Password. You cannot upload files.")

# --- STUDENT: TAKE TEST ---
elif choice == "Student: Take Test":
    if not st.session_state.mcqs:
        st.warning("No quiz is currently live. Please wait for the teacher.")
    else:
        with st.form("quiz_form"):
            st.markdown("### 📝 Examination Form")
            name = st.text_input("Student Full Name")
            student_answers = {}
            
            for i, q in enumerate(st.session_state.mcqs):
                st.markdown(f'<div class="question-card"><b>Q{i+1}: {q["Question"]}</b></div>', unsafe_allow_html=True)
                opts = [str(q['Option A']), str(q['Option B']), str(q['Option C']), str(q['Option D'])]
                student_answers[i] = st.radio(f"Select your answer for Q{i+1}", opts, key=f"q_{i}", label_visibility="collapsed")
            
            if st.form_submit_button("FINISH & SUBMIT"):
                if not name:
                    st.error("Name is required to submit.")
                else:
                    score = sum(1 for i, q in enumerate(st.session_state.mcqs) if student_answers[i] == str(q['Answer']))
                    st.session_state.results.append({"Student": name, "Score": f"{score}/{len(st.session_state.mcqs)}"})
                    st.success(f"Submission Successful! Well done, {name}.")

# --- ADMIN: VIEW RESULTS ---
elif choice == "Admin: View Results":
    st.subheader("📊 Performance Analytics")
    admin_pass = st.text_input("Admin View Password", type="password")
    
    if admin_pass == "admin123":
        if st.session_state.results:
            st.table(pd.DataFrame(st.session_state.results))
            if st.button("Clear All Results"):
                st.session_state.results = []
                st.experimental_rerun()
        else:
            st.info("Waiting for students to submit...")
    elif admin_pass:
        st.error("Invalid Credentials.")
