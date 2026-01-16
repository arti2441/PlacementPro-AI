import streamlit as st

from utils.config import settings


def configure_page() -> None:
    """Configure base Streamlit page settings and global styles."""
    st.set_page_config(
        page_title=settings.app_name,
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Global styling
    with open("assets/styles.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main() -> None:
    """Landing page for PlacementPro AI."""
    configure_page()

    st.title("PlacementPro AI")
    st.caption("Intelligent Training & Placement Ecosystem · ProGen-X")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Welcome to your Data Science placement co-pilot 👩‍💻👨‍💻")
        st.markdown(
            """
            PlacementPro AI is an **AI-driven Training & Placement Support System** focused on
            **Data Science** roles.

            - Intelligent **student dashboards** with skill-gap insights  
            - **Mock interviews** with AI-style feedback  
            - Personalized **training paths & recommendations**  
            - Rich **analytics** for TPOs and faculty  
            """
        )

        st.markdown("### Quick Start")
        st.markdown(
            """
            1. Navigate to **Student Dashboard** from the sidebar  
            2. Explore **Mock Interview** for AI-powered simulations  
            3. Use **TPO Analytics** and **Faculty View** for cohort insights  
            """
        )

    with col2:
        st.markdown(
            """
            <div class="hero-card">
                <h3>System Snapshot</h3>
                <ul>
                    <li>🎯 Data Science role focused</li>
                    <li>🤖 AI-driven interview engine</li>
                    <li>📊 Cohort & placement analytics</li>
                    <li>👨‍🏫 Faculty oversight tools</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        "Use the **left sidebar** to switch between student, TPO, and faculty views."
    )


if __name__ == "__main__":
    main()
