import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.scrape_job import scrape_job
from tools.score_fit import score_fit

st.set_page_config(page_title="Job Hunter Agent", page_icon="🎯", layout="wide")
st.title("🎯 Job Hunter Agent")
st.markdown("Paste a job URL and let the agent analyze your fit, tailor your resume, and generate application materials.")

# Session state init
if "stage" not in st.session_state:
    st.session_state.stage = "input"
if "score_result" not in st.session_state:
    st.session_state.score_result = None
if "job_description" not in st.session_state:
    st.session_state.job_description = None
if "final_result" not in st.session_state:
    st.session_state.final_result = None

# ── Stage 1: Input ─────────────────────────────────────────────
if st.session_state.stage == "input":
    job_url = st.text_input("Job URL", placeholder="https://www.welcometothejungle.com/...")
    run_button = st.button("Run Agent", type="primary")

    if run_button and job_url:
        with st.spinner("Scraping job page..."):
            scrape_result = scrape_job(job_url)

        if scrape_result["error"]:
            st.error(f"Failed to scrape job page: {scrape_result['error']}")
            st.stop()

        jd = scrape_result["raw_text"]

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(BASE_DIR, "data", "master_resume.md"), "r") as f:
            resume = f.read()

        with st.spinner("Analyzing fit..."):
            score_result = score_fit(jd, resume)

        st.session_state.score_result = score_result
        st.session_state.job_description = jd
        st.session_state.job_url = job_url

        if score_result["fit_score"] >= 70:
            st.session_state.stage = "generate"
        elif score_result["fit_score"] >= 40:
            st.session_state.stage = "ask_user"
        else:
            st.session_state.stage = "skipped"

        st.rerun()

# ── Stage 2: Ask user (medium fit) ────────────────────────────
elif st.session_state.stage == "ask_user":
    score = st.session_state.score_result
    st.warning(f"⚠️ Fit Score: {score['fit_score']}/100 — Medium match")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Company", score.get("company") or "N/A")
    with col2:
        st.metric("Role", score.get("job_title") or "N/A")

    with st.expander("📊 Fit Analysis", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Matching Strengths**")
            for s in score.get("matching_strengths", []):
                st.write(f"✅ {s}")
        with c2:
            st.markdown("**Gaps**")
            for g in score.get("gaps", []):
                st.write(f"⚠️ {g}")

    st.markdown("### This is a medium fit. Do you want to apply anyway?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, generate materials", type="primary"):
            st.session_state.stage = "generate"
            st.rerun()
    with col2:
        if st.button("❌ No, skip this role"):
            st.session_state.stage = "skipped"
            st.rerun()

# ── Stage 3: Skipped ──────────────────────────────────────────
elif st.session_state.stage == "skipped":
    score = st.session_state.score_result
    st.error(f"❌ Role skipped — Fit score: {score['fit_score']}/100")
    st.markdown("**Gaps identified:**")
    for g in score.get("gaps", []):
        st.write(f"- {g}")
    if st.button("🔄 Try another role"):
        st.session_state.stage = "input"
        st.session_state.score_result = None
        st.session_state.job_description = None
        st.rerun()

# ── Stage 4: Generate materials ───────────────────────────────
elif st.session_state.stage == "generate":
    if st.session_state.final_result is None:
        from nodes.writer import writer_node
        from nodes.tracker import tracker_node

        score = st.session_state.score_result
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        state = {
            "job_url": st.session_state.job_url,
            "job_title": score.get("job_title"),
            "company": score.get("company"),
            "job_description": st.session_state.job_description,
            "required_skills": None,
            "nice_to_have": None,
            "fit_score": score["fit_score"],
            "matching_strengths": score.get("matching_strengths", []),
            "gaps": score.get("gaps", []),
            "recommendation": score.get("recommendation"),
            "tailored_resume": None,
            "cover_letter": None,
            "outreach_message": None,
            "application_stage": None,
            "steps_log": ["Job scraped", f"Fit scored: {score['fit_score']}/100"],
            "errors": []
        }

        with st.spinner("Writing tailored resume..."):
            state = writer_node(state)
        with st.spinner("Saving to tracker..."):
            state = tracker_node(state)

        st.session_state.final_result = state

    result = st.session_state.final_result
    score = st.session_state.score_result

    # Fit score banner
    fit = result.get("fit_score", 0)
    if fit >= 70:
        st.success(f"✅ Fit Score: {fit}/100 — Strong match")
    else:
        st.warning(f"⚠️ Fit Score: {fit}/100 — Medium match")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Company", result.get("company") or "N/A")
    with col2:
        st.metric("Role", result.get("job_title") or "N/A")

    with st.expander("📊 Fit Analysis", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Matching Strengths**")
            for s in result.get("matching_strengths", []):
                st.write(f"✅ {s}")
        with c2:
            st.markdown("**Gaps**")
            for g in result.get("gaps", []):
                st.write(f"⚠️ {g}")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📄 Resume", "✉️ Cover Letter", "💬 Outreach"])
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(BASE_DIR, "output")

    with tab1:
        st.text_area("Tailored Resume", result.get("tailored_resume", ""), height=500)
        if os.path.exists(output_dir):
            pdfs = [f for f in os.listdir(output_dir) if f.startswith("resume_")]
            pdfs = sorted(pdfs, key=lambda f: os.path.getmtime(os.path.join(output_dir, f)), reverse=True)
            if pdfs:
                latest = os.path.join(output_dir, pdfs[0])
                pdf_bytes = open(latest, "rb").read()
                st.download_button(
                    label="⬇️ Download Resume PDF",
                    data=pdf_bytes,
                    file_name=pdfs[0],
                    mime="application/pdf"
                )
            else:
                st.warning("No resume PDF found.")

    with tab2:
        st.text_area("Cover Letter", result.get("cover_letter", ""), height=400)
        if os.path.exists(output_dir):
            pdfs = [f for f in os.listdir(output_dir) if f.startswith("cover_letter_")]
            pdfs = sorted(pdfs, key=lambda f: os.path.getmtime(os.path.join(output_dir, f)), reverse=True)
            if pdfs:
                latest = os.path.join(output_dir, pdfs[0])
                pdf_bytes = open(latest, "rb").read()
                st.download_button(
                    label="⬇️ Download Cover Letter PDF",
                    data=pdf_bytes,
                    file_name=pdfs[0],
                    mime="application/pdf"
                )
            else:
                st.warning("No cover letter PDF found.")

    with tab3:
        st.text_area("LinkedIn Outreach Message", result.get("outreach_message", ""), height=200)

    with st.expander("🔍 Agent Steps Log"):
        for step in result.get("steps_log", []):
            st.write(f"→ {step}")

    if result.get("errors"):
        with st.expander("⚠️ Errors"):
            for e in result["errors"]:
                st.error(e)

    if st.button("🔄 Analyze another role"):
        st.session_state.stage = "input"
        st.session_state.score_result = None
        st.session_state.job_description = None
        st.session_state.final_result = None
        st.rerun()