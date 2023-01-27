import pandas as pd
import streamlit as st


URL_BASE = "https://drivendata-competition-meta-vsc-data-us.s3.us-west-2.amazonaws.com"
URL_GROUND_TRUTH_FILE = f"{URL_BASE}/train/train_descriptor_ground_truth.csv"
URL_QUERY_BASE = f"{URL_BASE}/train/query/"
URL_REF_BASE = f"{URL_BASE}/train/reference/"


@st.cache
def load_data():
    df = pd.read_csv(URL_GROUND_TRUTH_FILE)
    query_ids = df.query_id.unique().tolist()
    ref_ids = df.ref_id.unique().tolist()

    query_to_refs = {x: [] for x in query_ids}
    ref_to_queries = {x: [] for x in ref_ids}
    for _, row in df.iterrows():
        query_to_refs[row.query_id].append(row.ref_id)
        ref_to_queries[row.ref_id].append(row.query_id)
    return query_to_refs, ref_to_queries


st.title("Video Similarity Challenge Ground Truth Visualizer")

q_to_r, r_to_q = load_data()

with st.sidebar:
    search_by = st.selectbox("Search By:", ["query", "reference"])
    chosen_val = st.selectbox("Select ID:", q_to_r.keys() if search_by == "query" else r_to_q.keys())

results_by = "reference" if search_by == "query" else "query"
search_url = URL_QUERY_BASE if search_by == "query" else URL_REF_BASE
results_url = URL_REF_BASE if search_by == "query" else URL_QUERY_BASE

col1, col2 = st.columns(2)

with col1:
    st.write(f"{search_by.title()} ID: {chosen_val}")
    st.video(f"{search_url}{chosen_val}.mp4")

with col2:
    for i, vid in enumerate(q_to_r[chosen_val] if search_by == "query" else r_to_q[chosen_val]):
        st.write(f"{results_by.title()} ID: {vid}")
        st.video(f"{results_url}{vid}.mp4")
