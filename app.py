import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="AI Training & Placement System", layout="wide")

# -------------------- DATA --------------------
industry_skills = {
    "Data Scientist": [
        "Python", "SQL", "Statistics",
        "Machine Learning", "Data Visualization", "Pandas"
    ]
}

project_mapping = {
    "Statistics": "Statistical Analysis Project",
    "Machine Learning": "House Price Prediction",
    "Data Visualization": "Sales Dashboard",
    "Pandas": "Data Cleaning Project"
}

# -------------------- TITLE --------------------
st.title("🎓 AI Driven Training & Placement Support System")
st.subheader("Hackathon MVP – Skill Gap & Placement Readiness")

# -------------------- ROLE SELECTION --------------------
role = st.sidebar.selectbox(
    "Login As",
    ["Student", "TPO", "Faculty"]
)

# =====================================================
# ==================== STUDENT ========================
# =====================================================
if role == "Student":

    st.header("👩‍🎓 Student Dashboard")

    name = st.text_input("Enter your name")
    job_role = st.selectbox("Select Job Role", ["Data Scientist"])

    skills_input = st.text_input(
        "Enter your skills (comma separated)",
        placeholder="Python, SQL, Pandas"
    )

    if st.button("Analyze My Skills"):

        student_skills = [s.strip() for s in skills_input.split(",")]
        required_skills = industry_skills[job_role]

        matched = list(set(student_skills) & set(required_skills))
        missing = list(set(required_skills) - set(student_skills))

        # -------------------- RESULTS --------------------
        st.subheader("📊 Skill Gap Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.success("Matched Skills")
            for s in matched:
                st.write("✔", s)

        with col2:
            st.error("Missing Skills")
            for s in missing:
                st.write("❌", s)

        # -------------------- GRAPH --------------------
        st.subheader("📈 Skill Comparison")

        skill_level = []
        for skill in required_skills:
            skill_level.append(1 if skill in student_skills else 0)

        df = pd.DataFrame({
            "Skill": required_skills,
            "Status": skill_level
        })

        fig, ax = plt.subplots()
        ax.bar(df["Skill"], df["Status"])
        ax.set_ylabel("1 = Present, 0 = Missing")
        ax.set_xticklabels(df["Skill"], rotation=45)
        st.pyplot(fig)

        # -------------------- READINESS SCORE --------------------
        readiness = int((len(matched) / len(required_skills)) * 100)

        st.subheader("🎯 Placement Readiness")
        st.metric("Readiness Score", f"{readiness}%")

        if readiness >= 70:
            st.success("✅ Ready for Placement")
        else:
            st.warning("⚠ Needs Improvement")

        # -------------------- PROJECT RECOMMENDATION --------------------
        st.subheader("🛠 Recommended Projects")
        for skill in missing:
            if skill in project_mapping:
                st.write("📌", project_mapping[skill])

# =====================================================
# ====================== TPO ==========================
# =====================================================
elif role == "TPO":

    st.header("🏢 TPO Dashboard")

    data = {
        "Branch": ["AI & DS", "CSE", "IT"],
        "Ready": [12, 8, 10],
        "Almost Ready": [18, 14, 9],
        "Not Ready": [10, 6, 5]
    }

    df = pd.DataFrame(data)
    st.dataframe(df)

    st.subheader("📊 Placement Readiness Overview")

    fig, ax = plt.subplots()
    ax.bar(df["Branch"], df["Ready"])
    ax.set_ylabel("Ready Students")
    st.pyplot(fig)

# =====================================================
# ==================== FACULTY ========================
# =====================================================
elif role == "Faculty":

    st.header("👩‍🏫 Faculty Dashboard")

    student_progress = {
        "Student": ["Aarti", "Riya", "Ankit"],
        "Progress": ["Improving", "Needs Work", "Good"],
        "Weak Areas": ["ML", "Statistics", "None"]
    }

    df = pd.DataFrame(student_progress)
    st.table(df)

    st.info("Faculty can monitor student progress and guide improvements.")
