import streamlit as st
import pandas as pd
import os
from backend.core.teacher_profiles import TeacherProfileService
from backend.core.recommendations_engine import RecommendationsEngine

st.set_page_config(page_title="Multimodal Attendance & Engagement Agent", layout="wide")

st.title("Multimodal Attendance & Engagement Dashboard")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Class Monitoring & Attendance")
    st.info("Webcam Feed Active: Face Tracking & Emotion Detection Running")

    # Show Attendance Records
    if os.path.exists("attendance.csv"):
        st.write("### Attendance Log")
        df = pd.read_csv("attendance.csv")
        st.dataframe(df.tail(10), use_container_width=True)
    else:
        st.write("No attendance logs found yet.")

with col2:
    st.subheader("Teacher Profile & Class Metrics")
    teacher_svc = TeacherProfileService()
    profile = teacher_svc.get_profile("teacher_01")

    st.metric("Effectiveness Score", f"{profile['effectiveness_score']}%", f"+{profile['trend']}%")

    st.write("### Student Trends")
    for item in profile["student_trends"]:
        st.write(f"- **{item['name']}**: {item['status']} ({item['change']}%)")

    st.write("### Live Recommendations")
    rec_engine = RecommendationsEngine()
    recs = rec_engine.generate_realtime_recommendations({
        "people": [{"id": "Student_01", "attention": 85}, {"id": "Student_02", "attention": 45}]
    })
    for r in recs:
        st.warning(f"[{r['type'].upper()}] {r['message']}")
        