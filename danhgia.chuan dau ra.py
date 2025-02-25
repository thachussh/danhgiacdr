import streamlit as st
import pandas as pd

# Định nghĩa các cấp độ đánh giá theo chuẩn ABET
THRESHOLDS = {
    "CLO": 70,  # Ngưỡng đạt của CLO
    "PI": 75,   # Ngưỡng đạt của PI
    "PLO": 80   # Ngưỡng đạt của PLO
}

# Cấu trúc dữ liệu
program_data = {
    "PLOs": {"PLO1": ["PI1", "PI2"]},
    "PIs": {"PI1": ["CLO1", "CLO2"], "PI2": ["CLO3"]},
    "CLOs": {
        "CLO1": {"Exam": 75, "Project": 80},
        "CLO2": {"Quiz": 70, "Assignment": 78},
        "CLO3": {"Final Exam": 85, "Presentation": 88}
    }
}

# Tính điểm CLO
def evaluate_CLO(clo_name):
    scores = list(program_data["CLOs"].get(clo_name, {}).values())
    return sum(scores) / len(scores) if scores else 0

# Tính điểm PI từ CLOs
def evaluate_PI(pi_name):
    related_CLOs = program_data["PIs"].get(pi_name, [])
    total_score = sum(evaluate_CLO(clo) for clo in related_CLOs)
    return total_score / len(related_CLOs) if related_CLOs else 0

# Tính điểm PLO từ PIs
def evaluate_PLO():
    results = {}
    for plo, pis in program_data["PLOs"].items():
        total_score = sum(evaluate_PI(pi) for pi in pis)
        average_score = total_score / len(pis) if pis else 0
        results[plo] = "Pass" if average_score >= THRESHOLDS["PLO"] else "Fail"
    return results

# Giao diện Streamlit
st.title("ABET Outcome Evaluation System")

# Hiển thị kết quả đánh giá
st.header("Evaluation Results")
plo_results = evaluate_PLO()
pi_results = {pi: evaluate_PI(pi) for pi in program_data["PIs"].keys()}
clo_results = {clo: evaluate_CLO(clo) for clo in program_data["CLOs"].keys()}

st.subheader("CLO Results")
st.write(pd.DataFrame.from_dict(clo_results, orient='index', columns=['CLO Score']))

st.subheader("PI Results")
st.write(pd.DataFrame.from_dict(pi_results, orient='index', columns=['PI Score']))

st.subheader("PLO Results")
st.write(pd.DataFrame.from_dict(plo_results, orient='index', columns=['PLO Result']))

# Form nhập dữ liệu mới
st.header("Add New CLO")
with st.form("clo_form"):
    clo_name = st.text_input("CLO Name")
    exam_score = st.number_input("Exam Score", min_value=0.0, max_value=100.0, value=75.0)
    project_score = st.number_input("Project Score", min_value=0.0, max_value=100.0, value=80.0)
    submit_button = st.form_submit_button("Add CLO")
    
    if submit_button and clo_name:
        program_data["CLOs"][clo_name] = {"Exam": exam_score, "Project": project_score}
        st.success(f"Added CLO {clo_name} successfully!")
        st.experimental_rerun()